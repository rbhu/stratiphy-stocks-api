import unittest

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from api.models import Stock, UserProfile
from api.permissions import IsInvestor
from api.serializers import StockSerializer


class AdminStockViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin_user = User.objects.create_user(username='admin', password='password')
        self.admin_profile = UserProfile.objects.create(user=self.admin_user, user_type='admin')
        self.client.force_authenticate(user=self.admin_user)

    def test_list_stocks(self):
        Stock.objects.create(stock_id=1, stock_name='Stock 1', price=10, short_code='STK1', quantity=10)
        Stock.objects.create(stock_id=2, stock_name='Stock 2', price=20, short_code='STK2', quantity=10)
        response = self.client.get('/stock-api/stocks/')
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_stock_by_id(self):
        Stock.objects.create(stock_id=1, stock_name='Stock 1', price=10, short_code='STK1', quantity=10)
        response = self.client.get('/stock-api/stocks/1', {}, True)
        stock = Stock.objects.get(stock_id=1)
        serializer = StockSerializer(stock)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_create_stock(self):
        data = {
            'stock_name': 'Stock',
            'short_code': 'STK',
            'price': 10.0,
            'quantity': 100
        }
        response = self.client.post('/stock-api/stocks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Stock.objects.count(), 1)
        stock = Stock.objects.get(short_code='STK')
        self.assertEqual(stock.stock_name, data['stock_name'])
        self.assertEqual(stock.short_code, data['short_code'])
        self.assertEqual(stock.price, data['price'])
        self.assertEqual(stock.quantity, data['quantity'])

    def test_update_stock(self):
        stock = Stock.objects.create(stock_name='Stock', short_code='STK', price=10.0, quantity=100)

        data = {
            'stock_name': 'New Stock Name',
            'short_code': 'NSTK',
            'price': 15.0,
            'quantity': 200
        }

        response = self.client.put(f'/stock-api/stocks/{stock.stock_id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        stock.refresh_from_db()
        self.assertEqual(stock.stock_name, data['stock_name'])
        self.assertEqual(stock.price, data['price'])
        self.assertEqual(stock.quantity, data['quantity'])

    def test_partial_update_stock(self):
        stock = Stock.objects.create(stock_name='Stock', short_code='STK', price=10.0, quantity=100)

        data = {
            'price': 15.0,
            'quantity': 200
        }

        response = self.client.patch(f'/stock-api/stocks/{stock.stock_id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        stock.refresh_from_db()
        self.assertEqual(stock.price, data['price'])
        self.assertEqual(stock.quantity, data['quantity'])

    def test_delete_stock(self):
        stock = Stock.objects.create(stock_name='Stock', short_code='STK', price=10.0, quantity=100)

        response = self.client.delete(f'/stock-api/stocks/{stock.stock_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Stock.objects.count(), 0)


class InvestorStockViewSetTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.stock1 = Stock.objects.create(stock_id=1, stock_name='Stock 1', price=10, short_code='STK1', quantity=10)
        self.stock2 = Stock.objects.create(stock_id=2, stock_name='Stock 2', price=20, short_code='STK2', quantity=10)

        # Create a user with 'investor' user type
        self.investor_user = User.objects.create_user(username='investor', password='password')
        self.investor_profile = UserProfile.objects.create(user=self.investor_user, user_type='investor')

        # Authenticate the client with the investor user
        self.client.force_authenticate(user=self.investor_user)

    def test_list_stocks(self):
        response = self.client.get('/stock-api/stocks/')
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_stock_by_id(self):
        response = self.client.get('/stock-api/stocks/1', {}, True)
        stock = Stock.objects.get(stock_id=1)
        serializer = StockSerializer(stock)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_search_stocks_by_name(self):
        search_term = 'Stock 1'
        response = self.client.get(f'/stock-api/stocks/?search={search_term}')
        stocks = Stock.objects.filter(stock_name__icontains=search_term)
        serializer = StockSerializer(stocks, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_search_stocks_by_short_code(self):
        search_term = 'STK1'
        response = self.client.get(f'/stock-api/stocks/?search={search_term}')
        stocks = Stock.objects.filter(short_code__icontains=search_term)
        serializer = StockSerializer(stocks, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_create_stock_forbidden(self):
        data = {
            'stock_name': 'Stock',
            'short_code': 'STK',
            'price': 10.0,
            'quantity': 100
        }
        response = self.client.post('/stock-api/stocks/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_stock_forbidden(self):
        stock = Stock.objects.create(stock_name='Stock', short_code='STK', price=10.0, quantity=100)

        data = {
            'stock_name': 'New Stock Name',
            'short_code': 'NSTK',
            'price': 15.0,
            'quantity': 200
        }

        response = self.client.put(f'/stock-api/stocks/{stock.stock_id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_stock_forbidden(self):
        stock = Stock.objects.create(stock_name='Stock', short_code='STK', price=10.0, quantity=100)

        data = {
            'price': 15.0,
            'quantity': 200
        }

        response = self.client.patch(f'/stock-api/stocks/{stock.stock_id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_stock_forbidden(self):
        stock = Stock.objects.create(stock_name='Stock', short_code='STK', price=10.0, quantity=100)

        response = self.client.delete(f'/stock-api/stocks/{stock.stock_id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UnauthorisedUserStockViewSetTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.stock1 = Stock.objects.create(stock_id=1, stock_name='Stock 1', price=10, short_code='STK1', quantity=10)
        self.stock2 = Stock.objects.create(stock_id=2, stock_name='Stock 2', price=20, short_code='STK2', quantity=10)

    def test_list_stocks_forbidden(self):
        response = self.client.get('/stock-api/stocks/')
        self.assertEqual(response.status_code, 401)
