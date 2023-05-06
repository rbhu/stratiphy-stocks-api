from django.test import TestCase
from rest_framework.test import APIClient
from api.models import Stock
from api.serializers import StockSerializer


class StockViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.stock1 = Stock.objects.create(stock_id=1, stock_name='Stock 1', price=10, short_code='STK1')
        self.stock2 = Stock.objects.create(stock_id=2, stock_name='Stock 2', price=20, short_code='STK2')

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
