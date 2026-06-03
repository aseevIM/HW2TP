import pytest
from ingredient import Ingredient
from recipe import Recipe
from ShoppingList import ShoppingList
from DietaryRecipe import DietaryRecipe

class TestIngredient:
    def test_creation(self):
        ing = Ingredient("Мука", 500.0, "г")
        assert ing.name == "Мука"
        assert ing.quantity == 500.0
        assert ing.unit == "г"

    def test_str(self):
        ing = Ingredient("Мука", 500.0, "г")
        assert str(ing) == "Мука: 500.0 г"

    def test_eq_same_name_unit(self):
        ing1 = Ingredient("Мука", 500.0, "г")
        ing2 = Ingredient("Мука", 1000.0, "г")
        assert ing1 == ing2

    def test_eq_different_name(self):
        ing1 = Ingredient("Мука", 500.0, "г")
        ing2 = Ingredient("Сахар", 500.0, "г")
        assert ing1 != ing2

    def test_eq_different_unit(self):
        ing1 = Ingredient("Мука", 500.0, "г")
        ing2 = Ingredient("Мука", 500.0, "кг")
        assert ing1 != ing2

    def test_quantity_positive(self):
        ing = Ingredient("Мука", 500.0, "г")
        with pytest.raises(ValueError, match="Количество должно быть положительным"):
            ing.quantity = -10

class TestRecipe:
    def test_creation(self):
        ing = Ingredient("Мука", 500.0, "г")
        recipe = Recipe("Пицца", [ing])
        assert recipe.title == "Пицца"
        assert len(recipe.ingredients) == 1

    def test_add_ingredient_new(self):
        recipe = Recipe("Пицца")
        ing = Ingredient("Мука", 500.0, "г")
        recipe.add_ingredient(ing)
        assert len(recipe.ingredients) == 1
        assert recipe.ingredients[0].quantity == 500.0

    def test_add_ingredient_existing(self):
        recipe = Recipe("Пицца")
        ing1 = Ingredient("Мука", 500.0, "г")
        ing2 = Ingredient("Мука", 300.0, "г")
        recipe.add_ingredient(ing1)
        recipe.add_ingredient(ing2)
        assert len(recipe.ingredients) == 1
        assert recipe.ingredients[0].quantity == 800.0

    def test_scale(self):
        ing = Ingredient("Мука", 500.0, "г")
        recipe = Recipe("Пицца", [ing])
        scaled = recipe.scale(2)
        assert scaled.ingredients[0].quantity == 1000.0
        assert recipe.ingredients[0].quantity == 500.0

    def test_scale_invalid_ratio(self):
        ing = Ingredient("Мука", 500.0, "г")
        recipe = Recipe("Пицца", [ing])
        with pytest.raises(ValueError):
            recipe.scale(-1)

    def test_len(self):
        ing1 = Ingredient("Мука", 500.0, "г")
        ing2 = Ingredient("Сахар", 100.0, "г")
        recipe = Recipe("Пицца", [ing1, ing2])
        assert len(recipe) == 2

class TestShoppingList:
    def test_add_recipe(self):
        ing = Ingredient("Мука", 500.0, "г")
        recipe = Recipe("Пицца", [ing])
        sl = ShoppingList()
        sl.add_recipe(recipe, 2)
        assert len(sl._items) == 1
        assert sl._items[0][0].quantity == 1000.0

    def test_add_recipe_invalid_portions(self):
        ing = Ingredient("Мука", 500.0, "г")
        recipe = Recipe("Пицца", [ing])
        sl = ShoppingList()
        with pytest.raises(ValueError, match="Количество порций должно быть положительным"):
            sl.add_recipe(recipe, -1)

    def test_remove_recipe(self):
        ing = Ingredient("Мука", 500.0, "г")
        recipe = Recipe("Пицца", [ing])
        sl = ShoppingList()
        sl.add_recipe(recipe, 1)
        sl.remove_recipe("Пицца")
        assert len(sl._items) == 0

    def test_remove_recipe_not_exists(self):
        sl = ShoppingList()
        sl.remove_recipe("Несуществующий")

    def test_get_list_merge(self):
        ing1 = Ingredient("Мука", 500.0, "г")
        ing2 = Ingredient("Мука", 300.0, "г")
        recipe1 = Recipe("Пицца", [ing1])
        recipe2 = Recipe("Хлеб", [ing2])
        sl = ShoppingList()
        sl.add_recipe(recipe1, 1)
        sl.add_recipe(recipe2, 1)
        result = sl.get_list()
        assert len(result) == 1
        assert result[0].quantity == 800.0

    def test_get_list_sorted(self):
        ing1 = Ingredient("Яйца", 2, "шт")
        ing2 = Ingredient("Мука", 500.0, "г")
        recipe = Recipe("Блины", [ing1, ing2])
        sl = ShoppingList()
        sl.add_recipe(recipe, 1)
        result = sl.get_list()
        assert result[0].name == "Мука"
        assert result[1].name == "Яйца"

    def test_add(self):
        ing1 = Ingredient("Мука", 500.0, "г")
        ing2 = Ingredient("Яйца", 2, "шт")
        recipe1 = Recipe("Пицца", [ing1])
        recipe2 = Recipe("Омлет", [ing2])
        sl1 = ShoppingList()
        sl2 = ShoppingList()
        sl1.add_recipe(recipe1, 1)
        sl2.add_recipe(recipe2, 1)
        sl3 = sl1 + sl2
        assert len(sl3._items) == 2
        assert len(sl1._items) == 1
        assert len(sl2._items) == 1
