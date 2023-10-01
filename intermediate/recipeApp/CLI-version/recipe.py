class Recipe:
    def __init__(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        
    def display_recipe(self):
        print(f'Recipe Name: {self.name}')
        if self.ingredients:
            print('Ingredients:')
            for ingredient in self.ingredients:
                print(f"-> {ingredient}")
        else:
            print("Ingredients unknown.")
        if self.instructions:
            print("Instructions:")
            for i, instruction in enumerate(self.instructions, start=1):
                print(f"{i}. {instruction}")
        else:
            print("No instructions available.")
            
    def edit_recipe(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions