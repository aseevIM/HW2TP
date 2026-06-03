from ingredient import Ingredient

class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled = recipe.scale(portions)
        for ing in scaled.ingredients:
            self._items.append((ing, recipe.title))

    def remove_recipe(self, title: str):
        self._items = [item for item in self._items if item[1] != title]

    def get_list(self):
        merged = {}
        for ing, _ in self._items:
            key = (ing.name, ing.unit)
            if key in merged:
                merged[key] += ing.quantity
            else:
                merged[key] = ing.quantity
        res = [Ingredient(name, qty, unit) for (name, unit), qty in merged.items()]
        res.sort(key=lambda x: x.name)
        return res

    def __add__(self, other):
        new_list = ShoppingList()
        new_list._items = self._items.copy() + other._items.copy()
        return new_list