from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import StockViewSet, BuyStockTransactionViewSet, SellStockTransactionViewSet

router = DefaultRouter()

router.register(r'stocks', StockViewSet, basename='stock-list')
router.register(r'buy', BuyStockTransactionViewSet, basename='stock-buy')
router.register(r'sell', SellStockTransactionViewSet, basename='stock-sell')

urlpatterns = [
    path('stock-api/investor/', include(router.urls)),
]
