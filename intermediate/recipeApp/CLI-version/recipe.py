class Recipe:
    def __init__(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        # \033[1;36mCurrency Converter\033[0m
    def display_recipe(self):
        print(f'\n\033[1;36mRecipe Name\033[0m: {self.name}')
        if self.ingredients:
            print('\n\033[1;36mIngredients\033[0m:')
            for ingredient in self.ingredients:
                print(f"-> {ingredient}")
        else:
            print("\n\033[1;31mIngredients unknown.\033[0m")
        if self.instructions:
            print("\n\033[1;36mInstructions\033[0m:")
            for i, instruction in enumerate(self.instructions, start=1):
                print(f"{i}. {instruction}")
        else:
            print("\n\033[1;31mNo instructions available.\033[0m")
            
    def edit_recipe(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions