from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views.investor.stock_holdings import StockHoldingsViewSet
from api.views.investor.stock_transaction import BuyStockTransactionViewSet, \
    SellStockTransactionViewSet
from api.views.investor.stocks import StockViewSet

router = DefaultRouter()

router.register(r'stocks', StockViewSet, basename='stock-list')
router.register(r'buy', BuyStockTransactionViewSet, basename='stock-buy')
router.register(r'sell', SellStockTransactionViewSet, basename='stock-sell')
router.register(r'holdings', StockHoldingsViewSet, basename='stock-holdings')


urlpatterns = [
    path('stock-api/investor/', include(router.urls)),
]
