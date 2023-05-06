from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from api.models import Stock
from api.serializers import StockSerializer
from api.permissions import IsInvestor
from api.models import UserProfile


class StockViewSetTestCase(TestCase):
    def setUp(self):
        self.permission = IsInvestor()
        self.client = APIClient()
        self.stock1 = Stock.objects.create(stock_id=1, stock_name='Stock 1', price=10, short_code='STK1', quantity=10)
        self.stock2 = Stock.objects.create(stock_id=2, stock_name='Stock 2', price=20, short_code='STK2', quantity=10)

        # Create a user with 'investor' user type
        self.investor_user = User.objects.create_user(username='investor', password='password')
        self.investor_profile = UserProfile.objects.create(user=self.investor_user, user_type='investor')

        # Authenticate the client with the investor user
        self.client.force_authenticate(user=self.investor_user)

    def test_list_stocks(self):
        response = self.client.get('/stock-api/investor/stocks/')
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_search_stocks_by_name(self):
        search_term = 'Stock 1'
        response = self.client.get(f'/stock-api/investor/stocks/?search={search_term}')
        stocks = Stock.objects.filter(stock_name__icontains=search_term)
        serializer = StockSerializer(stocks, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_search_stocks_by_short_code(self):
        search_term = 'STK1'
        response = self.client.get(f'/stock-api/investor/stocks/?search={search_term}')
        stocks = Stock.objects.filter(short_code__icontains=search_term)
        serializer = StockSerializer(stocks, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)
