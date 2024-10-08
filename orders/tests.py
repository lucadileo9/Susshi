
import unittest
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.models import User
from menu.models import Dish
from tables.models import Table
from .models import Order, OrderDetail

class OrderDetailTestCase(TestCase):
    """
    Test case for the OrderDetail model.
    """

    def setUp(self):
        """
        Set up the necessary objects for testing.

        This method creates a table, a dish, an order, and an order detail
        to be used in the test cases.
        """
        user = User.objects.create(username='test_user', password='test_password')
        table = Table.objects.create(table_number=1, user=user)
        
        self.dish = Dish.objects.create(name='Sushi', price=10, profit=5)
        self.order = Order.objects.create(table=table)
        self.order_detail = OrderDetail.objects.create(order=self.order, dish=self.dish, quantity=2)


    def test_order_detail_creation(self):
        """
        Test case for creating an order detail.

        This test verifies that the order detail is created correctly by checking the following assertions:
        - The order detail's order is equal to the expected order.
        - The order detail's dish is equal to the expected dish.
        - The order detail's quantity is equal to the expected quantity.
        - The order detail's status is equal to the expected status.
        """
        self.assertEqual(self.order_detail.order, self.order)
        self.assertEqual(self.order_detail.dish, self.dish)
        self.assertEqual(self.order_detail.quantity, 2)
        self.assertEqual(self.order_detail.status, 'In attesa')
    
    
    def test_order_detail_validate_positive_nonzero_with_zero(self):
        """
        Test case to validate that an OrderDetail object with a quantity of zero raises a ValidationError.
        """
        with self.assertRaises(ValidationError):
            order_detail = OrderDetail.objects.create(order=self.order, dish=self.dish, quantity=0)
            order_detail.full_clean()

    def test_order_detail_validate_positive_nonzero_with_a_negative_number(self):
        """
        Test case to validate that an OrderDetail object with a negative quantity raises a IntegrityError.
        """
        with self.assertRaises(IntegrityError):
            order_detail = OrderDetail.objects.create(order=self.order, dish=self.dish, quantity=-1)
            order_detail.full_clean()


    def test_order_detail_total_price(self):
        """
        Test case to verify the total price of an order detail.

        This test ensures that the `total_price` attribute of the `order_detail` object
        is equal to the expected value of 20.

        """
        self.assertEqual(self.order_detail.total_price, 20)

    def test_order_detail_total_earned(self):
        """
        Test case to verify the correctness of the `total_earned` property in the `OrderDetail` class.

        This test asserts that the `total_earned` property of the `OrderDetail` instance is equal to 10.
        """
        self.assertEqual(self.order_detail.total_earned, 10)

    def test_order_detail_move_to_next_status(self):
        """
        Test case to verify the behavior of the move_to_next_status method in the OrderDetail class.
        """
        self.order_detail.move_to_next_status
        self.assertEqual(self.order_detail.status, 'In preparazione')
        self.order_detail.move_to_next_status
        self.assertEqual(self.order_detail.status, 'Pronto')
        self.order_detail.move_to_next_status
        self.assertEqual(self.order_detail.status, 'In attesa')
