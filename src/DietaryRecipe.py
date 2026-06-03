# dietary_recipe.py
from recipe import Recipe

class DietaryRecipe(Recipe):
    def __init__(self, title: str, diet_type: str, ingredients=None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio: float):
        scaled = super().scale(ratio)
        return DietaryRecipe(scaled.title, self.diet_type, scaled.ingredients)

    def __str__(self):
        return f"[{self.diet_type}] {self.title}:\n" + "\n".join(f"  - {ing}" for ing in self.ingredients)