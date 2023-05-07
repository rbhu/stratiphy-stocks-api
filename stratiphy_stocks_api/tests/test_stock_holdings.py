from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from api.models import UserProfile, Stock, UserStock
from api.permissions import IsInvestor


class HoldingsViewSetTestCase(TestCase):
    def setUp(self):
        self.permission = IsInvestor()
        self.client = APIClient()
        self.url = '/stock-api/investor/holdings/'

        # Create a user with 'investor' user type and authenticate
        self.investor_user = User.objects.create_user(username='investor', password='password')
        self.investor_profile = UserProfile.objects.create(user=self.investor_user, user_type='investor')
        self.client.force_authenticate(user=self.investor_user)

        self.stock1 = Stock.objects.create(stock_name='Apple', short_code='AAPL', price='2', quantity=50)
        self.user_stock1 = UserStock.objects.create(stock=self.stock1, user=self.investor_user, quantity=10)
        self.stock2 = Stock.objects.create(stock_name='Google', short_code='GOOG', price='3', quantity=50)
        self.user_stock2 = UserStock.objects.create(stock=self.stock2, user=self.investor_user, quantity=20)

    def test_list_holdings(self):
        # Make a GET request to the holdings endpoint
        response = self.client.get(self.url)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.maxDiff = None
        # Assert the response data
        expected_data = {
            'holdings': [
                {
                    'stockId': self.stock1.pk,
                    'quantity': 10,
                    'currentStockPrice': 2.0,
                    'totalHoldingValue': 20.0
                },
                {
                    'stockId': self.stock2.pk,
                    'quantity': 20,
                    'currentStockPrice': 3.0,
                    'totalHoldingValue': 60.0
                }
            ]
        }

        self.assertEqual(response.json(), expected_data)
