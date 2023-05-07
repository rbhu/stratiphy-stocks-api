from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from api.models import Stock, UserProfile
from api.permissions import IsInvestor
from api.serializers import StockSerializer


class AdminStockViewSetTestCase(TestCase):
    def setUp(self):
        self.permission = IsInvestor()
        self.client = APIClient()
        self.stock1 = Stock.objects.create(stock_id=1, stock_name='Stock 1', price=10, short_code='STK1', quantity=10)
        self.stock2 = Stock.objects.create(stock_id=2, stock_name='Stock 2', price=20, short_code='STK2', quantity=10)

        # Create a user with 'admin' user type
        self.admin_user = User.objects.create_user(username='admin', password='password')
        self.admin_profile = UserProfile.objects.create(user=self.admin_user, user_type='admin')

        # Authenticate the client with the admin user
        self.client.force_authenticate(user=self.admin_user)

    def test_list_stocks(self):
        response = self.client.get('/stock-api/admin/stocks/')
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_stock_by_id(self):
        response = self.client.get('/stock-api/admin/stocks/1', {}, True)
        stock = Stock.objects.get(stock_id=1)
        serializer = StockSerializer(stock)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)
