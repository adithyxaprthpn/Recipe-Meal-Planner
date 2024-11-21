import json

def load_recipes():
    try:
        with open('recipes.json', 'r') as file:
            recipes = json.load(file)
        return recipes
    except FileNotFoundError:
        print("Error: The 'recipes.json' file was not found.")
        return []
    except json.JSONDecodeError:
        print("Error: There was a problem reading the 'recipes.json' file.")
        return []

def save_recipes(recipes):
    try:
        with open('recipes.json', 'w') as file:
            json.dump(recipes, file, indent=4)
    except Exception as e:
        print(f"Error saving recipes: {e}")

def find_recipes_by_ingredient(recipes, ingredient):
    found_recipes = [recipe for recipe in recipes if ingredient.lower() in [ing.lower() for ing in recipe['ingredients']]]
    return found_recipes

def filter_recipes(recipes, meal_type=None, max_time=None, is_vegetarian=None):
    filtered_recipes = recipes
    if meal_type:
        filtered_recipes = [recipe for recipe in filtered_recipes if recipe.get("meal_type") == meal_type]
    if max_time:
        filtered_recipes = [recipe for recipe in filtered_recipes if recipe.get("prep_time", float('inf')) <= max_time]
    if is_vegetarian is not None:
        filtered_recipes = [recipe for recipe in filtered_recipes if recipe.get("is_vegetarian") == is_vegetarian]
    return filtered_recipes

def display_recipes_and_instructions(recipes):
    if recipes:
        print("\nRecipes found:")
        for idx, recipe in enumerate(recipes, 1):
            print(f"{idx}. {recipe['name']} (Meal: {recipe.get('meal_type', 'General')}, Time: {recipe.get('prep_time', 'N/A')} min)")
            print("   Ingredients:")
            for ingredient in recipe['ingredients']:
                print(f"     - {ingredient}")
        
        try:
            choice = int(input("\nEnter the number of the recipe you want to view instructions for (or type '0' to go back): "))
            if choice == 0:
                return None
            else:
                selected_recipe = recipes[choice - 1]
                print("\nInstructions for", selected_recipe['name'] + ":")
                for step in selected_recipe['instructions']:
                    print(f"  {step}")
        except (ValueError, IndexError):
            print("Invalid choice, please try again.")
    else:
        print("No recipes found with the given criteria.")
    
    return True

def add_new_recipe(recipes):
    print("\nAdd a new recipe:")
    name = input("Recipe name: ").strip()
    ingredients = input("Ingredients (comma-separated): ").strip().split(',')
    instructions = input("Instructions (separate steps by ';'): ").strip().split(';')
    meal_type = input("Meal type (e.g., Breakfast, Lunch, Dinner, Snack): ").strip()
    prep_time = int(input("Preparation time (in minutes): ").strip())
    is_vegetarian = input("Is the recipe vegetarian? (yes/no): ").strip().lower() == 'yes'
    affordability = int(input("Affordability score (1 to 5, 1 = very cheap, 5 = very expensive): ").strip())
    
    new_recipe = {
        "name": name,
        "ingredients": [ingredient.strip() for ingredient in ingredients],
        "instructions": [instruction.strip() for instruction in instructions],
        "meal_type": meal_type,
        "prep_time": prep_time,
        "is_vegetarian": is_vegetarian,
        "affordability": affordability
    }
    recipes.append(new_recipe)
    save_recipes(recipes)
    print(f"Recipe '{name}' added successfully!")

def main():
    recipes = load_recipes()
    
    if not recipes:
        print("No recipes available to search.")
        return
    
    while True:
        print("\nRecipe Finder Menu:")
        print("1. Search recipes by ingredient")
        print("2. Filter recipes (by meal type, time, or vegetarian option)")
        print("3. Add a new recipe")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            ingredient = input("Enter an ingredient to search for: ").strip()
            found_recipes = find_recipes_by_ingredient(recipes, ingredient)
            display_recipes_and_instructions(found_recipes)
        elif choice == '2':
            meal_type = input("Meal type (e.g., Breakfast, Lunch, Dinner) or leave blank: ").strip() or None
            max_time = input("Maximum preparation time (in minutes) or leave blank: ").strip()
            max_time = int(max_time) if max_time else None
            vegetarian_input = input("Vegetarian only? (yes/no or leave blank): ").strip().lower()
            is_vegetarian = None if not vegetarian_input else vegetarian_input == 'yes'
            filtered_recipes = filter_recipes(recipes, meal_type, max_time, is_vegetarian)
            display_recipes_and_instructions(filtered_recipes)
        elif choice == '3':
            add_new_recipe(recipes)
        elif choice == '4':
            print("Exiting the recipe finder. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
