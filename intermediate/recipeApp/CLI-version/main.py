import json
from recipe import Recipe
import sys

def load_recipes():
    try:
        with open('recipes.json', 'r') as file:
            recipes = json.load(file)
            return [Recipe(**data) for data in recipes]
    except FileNotFoundError:
        return []

def view_recipe(recipes_data):
    if not recipes_data:
        print("\nYour recipe book is empty.")
        return
    
    print("\nSelect a recipe to view:")
    for idx, recipe in enumerate(recipes_data, start=1):
        print(f"{idx}. {recipe.name}")
    
    try:
        choice = int(input("Enter the number of the recipe to view: "))
        
        if 1 <= choice <= len(recipes_data):
            selected_recipe = recipes_data[choice - 1]
            selected_recipe.display_recipe()
        else:
            print("Invalid choice. Please enter a valid number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def add_recipe(recipes_data):
    recipe_name = input("Enter the name of the recipe: ")
    ingredients = input("Enter the ingredients (comma-separated): ").split(",")
    instructions = []
    print("Enter the instructions one per line (press Enter on a new line to finish):")
    # Accept input till user enters nothing and press enter
    while True:
        instruction = input(">")
        if not instruction:
            break
        instructions.append(instruction)
    new_recipe = Recipe(recipe_name.strip(), [ingredient.strip() for ingredient in ingredients], instructions)
    recipes_data.append(new_recipe)
    print(f"{recipe_name} has been added to your recipe book.")
    
def edit_recipe(recipes_data):
    if not recipes_data:
        print("Your recipe book is empty.")
        return
    
    print("Select a recipe to edit:")
    for idx, recipe in enumerate(recipes_data, start=1):
        print(f"{idx}. {recipe.name}")
    
    try:
        choice = int(input("Enter the number of the recipe to edit: "))
        
        if 1 <= choice <= len(recipes_data):
            selected_recipe = recipes_data[choice - 1]
            
            # Prompt the user for new information and update the recipe
            name = input(f"Enter the new name for {selected_recipe.name}: ")
            ingredients = input(f"Enter the new ingredients (comma-separated) for {selected_recipe.name}: ").split(",")
            instructions = []
            print(f"Enter the new instructions for {selected_recipe.name} (one per line, press Enter to finish):")
            while True:
                instruction = input()
                if not instruction:
                    break
                instructions.append(instruction)
            
            selected_recipe.edit_recipe(name.strip(), [ingredient.strip() for ingredient in ingredients], instructions)
            print(f"{name} has been updated.")
        else:
            print("Invalid choice. Please enter a valid number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def delete_recipe(recipes_data):
    if not recipes_data:
        print("Your recipe book is empty.")
        return
    
    print("Select a recipe to delete:")
    for idx, recipe in enumerate(recipes_data, start=1):
        print(f"{idx}. {recipe.name}")
    
    try:
        choice = int(input("Enter the number of the recipe to delete: "))
        
        if 1 <= choice <= len(recipes_data):
            deleted_recipe = recipes_data.pop(choice - 1)
            print(f"\033[1;31m{deleted_recipe.name} has been deleted from your recipe book.\033[0m")
        else:
            print("Invalid choice. Please enter a valid number.")
    except ValueError:
        print("Invalid input. Please enter a number.")


def save_recipes(recipes):
    with open('recipes.json', 'w') as file:
        recipes_data = [{"name": recipe.name, "ingredients": recipe.ingredients, "instructions": recipe.instructions} for recipe in recipes]
        json.dump(recipes_data, file, indent=4)
    print("\033[1;32mSaved successfully!\033[0m")

def exit_program(recipes_data):
    print("1. Save and exit\n2. Exit without saving")
    choice = int(input('>'))
    if choice == 1:
        save_recipes(recipes_data)
        print("Ending the program..")
        sys.exit(0)
    else:
        print("Ending the program..")
        sys.exit(0)
        

def main():
    recipes_data = load_recipes()
    title = "Cook's HandBook"
    print(f"\n\x1b[1;33;44m{title}\x1b[0m")
    
    while True:
        print("\n1. Add Recipe")
        print("2. View Recipe")
        print("3. Edit Recipe")
        print("4. Delete Recipe")
        print("5. Exit")
        
        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                add_recipe(recipes_data)
            elif choice == 2:
                view_recipe(recipes_data)
            elif choice == 3:
                edit_recipe(recipes_data)
            elif choice == 4:
                delete_recipe(recipes_data)
            elif choice == 5:
                exit_program(recipes_data)
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print('Invalid input! Try again')
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEnding the script...")