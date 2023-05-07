from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views.admin.stocks import StockAdminViewSet
from api.views.investor.stock_holdings import StockHoldingsViewSet
from api.views.investor.stock_transaction import BuyStockTransactionViewSet, \
    SellStockTransactionViewSet
from api.views.investor.stocks import StockViewSet

investor_router = DefaultRouter()
investor_router.register(r'stocks', StockViewSet, basename='stock-list')
investor_router.register(r'buy', BuyStockTransactionViewSet, basename='stock-buy')
investor_router.register(r'sell', SellStockTransactionViewSet, basename='stock-sell')
investor_router.register(r'holdings', StockHoldingsViewSet, basename='stock-holdings')

admin_router = DefaultRouter()
admin_router.register(r'stocks', StockAdminViewSet, basename='stock-admin')

urlpatterns = [
    path('stock-api/investor/', include(investor_router.urls)),
    path('stock-api/admin/', include(admin_router.urls)),
]
