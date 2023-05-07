from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import StockViewSet, StockTransactionViewSet

router = DefaultRouter()

router.register(r'stocks', StockViewSet, basename='stock-list')
router.register(r'buy', StockTransactionViewSet, basename='stock-buy')

urlpatterns = [
    path('stock-api/investor/', include(router.urls)),
]
