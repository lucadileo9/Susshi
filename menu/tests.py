from django.test import TestCase
from .models import Dish, Ingredient
from django.core.exceptions import ValidationError
from django.urls import reverse

class DishModelTest(TestCase):
    """
    Test case for the Dish model.

    """

    def setUp(self):
        """
        Set up the test environment by creating necessary objects and data.

        This method is called before each test case is executed.

        - Creates two Ingredient objects with names 'Ingredient 1' and 'Ingredient 2'.
        - Creates two Dish objects with names 'Dish 1' and 'Dish 2', descriptions 'Description 1' and 'Description 2',
            prices 10.99 and 15.99, and profits 5.99 and 8.99 respectively.
        - Sets the ingredients for Dish 1 as 'Ingredient 1' and 'Ingredient 2'.
        - Sets the ingredient for Dish 2 as 'Ingredient 2'.
        """
        ingredient1 = Ingredient.objects.create(name='Ingredient 1')
        ingredient2 = Ingredient.objects.create(name='Ingredient 2')
        Dish.objects.create(name='Dish 1', description='Description 1', price=10.99, profit=5.99)
        Dish.objects.create(name='Dish 2', description='Description 2', price=15.99, profit=8.99)
        Dish.objects.get(pk=1).ingredients.set([ingredient1, ingredient2])
        Dish.objects.get(pk=2).ingredients.set([ingredient2])

    def test_dish_creation(self):
        """
        Test case for creating a dish.
        This test verifies that the dish is created correctly by checking the following assertions:
        - The dish's name is equal to the expected name.
        - The dish's description is equal to the expected description.
        - The dish's price is equal to the expected price.
        - The dish's profit is equal to the expected profit.
        """
        dish = Dish.objects.get(pk=1)
        self.assertEqual(dish.name, 'Dish 1')
        self.assertEqual(dish.description, 'Description 1')
        self.assertEqual(dish.price, 10.99)
        self.assertEqual(dish.profit, 5.99)

    def test_name_unique(self):
        """
        Test case to check if the name of a dish is unique.

        This test creates a new Dish object with a name that already exists in the database.
        It then asserts that an exception is raised when trying to save the dish.
        """
        dish = Dish(name='Dish 1', description='Description', price=9.99, profit=4.99)
        with self.assertRaises(Exception):
            dish.save()

    def test_price_validator_with_zero(self):
        """
        Test case to validate the price field with zero value.

        This test creates a new Dish object with a price of zero.
        It then asserts that a ValidationError is raised when trying to clean the dish.
        """
        dish = Dish(name='Dish 3', description='Description', price=0, profit=10)
        with self.assertRaises(ValidationError):
            dish.full_clean()

    def test_price_validator_with_negative_number(self):
        """
        Test case to validate the price field with a negative number.

        This test creates a new Dish object with a negative price.
        It then asserts that a ValidationError is raised when trying to clean the dish.
        """
        dish = Dish(name='Dish 3', description='Description', price=-1, profit=10)
        with self.assertRaises(ValidationError):
            dish.full_clean()

    def test_profit_validator_with_zero(self):
        """
        Test case to validate the profit field with zero value.

        This test creates a new Dish object with a profit of zero.
        It then asserts that a ValidationError is raised when trying to clean the dish.
        """
        dish = Dish(name='Dish 3', description='Description', price=10, profit=0)
        with self.assertRaises(ValidationError):
            dish.full_clean()

    def test_profit_validator_with_negative_number(self):
        """
        Test case to validate the profit field with a negative number.

        This test creates a new Dish object with a negative profit.
        It then asserts that a ValidationError is raised when trying to clean the dish.
        """
        dish = Dish(name='Dish 3', description='Description', price=10, profit=-1)
        with self.assertRaises(ValidationError):
            dish.full_clean()

class SearchResultsListTestCase(TestCase):
    
    def setUp(self):
        self.url = reverse('menu:search_results')
        self.ingredient1 = Ingredient.objects.create(name='Ingredient 1')
        self.ingredient2 = Ingredient.objects.create(name='Ingredient 2')

        self.dish1 = Dish.objects.create(name='abc', price=10, profit=5)
        self.dish2 = Dish.objects.create(name='cde', price=8, profit=4)
        self.dish3 = Dish.objects.create(name='xyz', price=6, profit=3)
        self.dish4 = Dish.objects.create(name='ccc', price=4, profit=2)
        
        self.dish1.ingredients.add(self.ingredient1, self.ingredient2)
        self.dish2.ingredients.add(self.ingredient1)
        self.dish3.ingredients.add(self.ingredient2)
        self.dish4.ingredients.add(self.ingredient1, self.ingredient2)


    def test_search_with_no_query_params(self):
        """
        Test case to verify the behavior when no query parameters are provided.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['object_list'],
            [])
        self.assertContains(response, "Piatti non trovati.")

    def test_search_with_name(self):
        response = self.client.get(self.url, {'name': 'xyz'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['object_list'],
            [ self.dish3])

    def test_search_with_ingredient(self):
        response = self.client.get(self.url, {'ingredients': str(self.ingredient1.id)})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['object_list'],
            [self.dish1, self.dish2, self.dish4],
            ordered=False)
        
    def test_search_with_ingredients(self):
        response = self.client.get(self.url, {'ingredients': f"{str(self.ingredient1.id)},{str(self.ingredient2.id)}"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['object_list'],
            [self.dish1, self.dish4],
            ordered=False)



    def test_search_with_max_price(self):
        response = self.client.get(self.url, {'max_price': 7})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['object_list'],
            [self.dish3, self.dish4], 
            ordered=False)
        
    def test_search_with_name_and_max_price(self):
        response = self.client.get(self.url, {'name': 'c', 'max_price': 9.00})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['object_list'],
            [self.dish2, self.dish4],
            ordered=False)

    def test_search_with_name_and_ingredients(self):
        response = self.client.get(self.url, {'name': 'c',  'ingredients': str(self.ingredient2.id)})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['object_list'],
            [self.dish1, self.dish4],
            ordered=False
        )
    
    def test_search_with_ingredients_and_max_price(self):
        response = self.client.get(self.url, {'ingredients': str(self.ingredient1.id), 'max_price': 8.00})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['object_list'],
            [self.dish2, self.dish4],
            ordered=False
        )
        
    def test_search_with_all_parameters(self):
        response = self.client.get(self.url, {'name': 'c', 'ingredients': str(self.ingredient2.id), 'max_price': 9.00})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['object_list'], [(self.dish4)])
