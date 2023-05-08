from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views.stock_holdings import StockHoldingsViewSet
from api.views.stock_transaction import BuyStockTransactionViewSet, \
    SellStockTransactionViewSet
from api.views.stocks import StockViewSet

router = DefaultRouter()
router.register(r'stocks', StockViewSet, basename='stock')
router.register(r'buy', BuyStockTransactionViewSet, basename='stock-buy')
router.register(r'sell', SellStockTransactionViewSet, basename='stock-sell')
router.register(r'holdings', StockHoldingsViewSet, basename='stock-holdings')

urlpatterns = [
    path('stock-api/', include(router.urls))]
