from _decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from api.models import Stock, UserProfile, UserStock
from api.permissions import IsInvestor


class BuyStockTransactionViewSetTestCase(TestCase):
    def setUp(self):
        self.permission = IsInvestor()
        self.client = APIClient()
        self.stock = Stock.objects.create(stock_name='Apple', short_code='AAPL', price='10.20', quantity=100)
        self.url = '/stock-api/investor/buy/'

        # Create a user with 'investor' user type and authenticate
        self.investor_user = User.objects.create_user(username='investor', password='password')
        self.investor_profile = UserProfile.objects.create(user=self.investor_user, user_type='investor')
        self.client.force_authenticate(user=self.investor_user)

    def test_buy_stock(self):
        request_data = {
            'stockId': self.stock.pk,
            'quantity': 50
        }
        response = self.client.post(self.url, request_data)

        expected_response_body = {
            'stockId': str(self.stock.pk),
            'quantity': 50,
            'totalCost': Decimal('510.00')
        }

        self.stock.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response_body)

        self.assertEqual(UserStock.objects.count(), 1)
        self.assertEqual(UserStock.objects.first().quantity, 50)
        self.assertEqual(self.stock.quantity, 50)

    def test_buy_stock_insufficient_quantity(self):
        request_data = {
            'stockId': self.stock.pk,
            'quantity': 150
        }
        response = self.client.post(self.url, request_data)
        self.stock.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'There is not enough stock to purchase this quantity.')
        self.assertEqual(UserStock.objects.count(), 0)
        self.assertEqual(self.stock.quantity, 100)

    def test_buy_stock_which_doesnt_exist(self):
        request_data = {
            'stockId': 999,
            'quantity': 150
        }
        response = self.client.post(self.url, request_data)
        self.stock.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Stock not found')
        self.assertEqual(UserStock.objects.count(), 0)
        self.assertEqual(self.stock.quantity, 100)


class SellStockTransactionViewSetTestCase(TestCase):
    def setUp(self):
        self.permission = IsInvestor()
        self.client = APIClient()
        self.url = '/stock-api/investor/sell/'

        # Create a user with 'investor' user type and authenticate
        self.investor_user = User.objects.create_user(username='investor', password='password')
        self.investor_profile = UserProfile.objects.create(user=self.investor_user, user_type='investor')
        self.client.force_authenticate(user=self.investor_user)

        self.stock = Stock.objects.create(stock_name='Apple', short_code='AAPL', price='10.20', quantity=50)
        self.user_stock = UserStock.objects.create(stock=self.stock, user=self.investor_user, quantity=100)

    def test_sell_stock(self):
        request_data = {
            'stockId': self.stock.pk,
            'quantity': 50
        }

        response = self.client.post(self.url, request_data)

        expected_response_body = {
            'stockId': str(self.stock.pk),
            'quantity': 50,
            'totalProfit': Decimal('510.00')
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response_body)

        # Assert updated stock and user_stock quantities
        self.stock.refresh_from_db()
        self.user_stock.refresh_from_db()

        self.assertEqual(self.stock.quantity, 100)  # Quantity increased by 50
        self.assertEqual(self.user_stock.quantity, 50)  # Quantity decreased by 50

    def test_sell_stock_insufficient_quantity(self):
        request_data = {
            'stockId': self.stock.pk,
            'quantity': 200
        }

        response = self.client.post(self.url, request_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['error'],
            'Cannot sell more stock than the user holds'
        )

        # Assert stock and user_stock quantities remain unchanged
        self.stock.refresh_from_db()
        self.user_stock.refresh_from_db()

        self.assertEqual(self.stock.quantity, 50)  # no changes
        self.assertEqual(self.user_stock.quantity, 100)  # no changes

    def test_sell_stock_invalid_stock_id(self):
        request_data = {
            'stockId': 999,
            'quantity': 200
        }

        response = self.client.post(self.url, request_data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Stock not found')

        # Assert stock and user_stock quantities remain unchanged
        self.stock.refresh_from_db()
        self.user_stock.refresh_from_db()

        self.assertEqual(self.stock.quantity, 50)  # no changes
        self.assertEqual(self.user_stock.quantity, 100)  # no changes

    def test_user_does_not_hold_stock(self):
        request_data = {
            'stockId': self.stock.stock_id,
            'quantity': 20
        }

        # Delete user_stock before making the request
        self.user_stock.delete()

        response = self.client.post(self.url, request_data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'User does not hold this stock')

        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 50)  # no changes
