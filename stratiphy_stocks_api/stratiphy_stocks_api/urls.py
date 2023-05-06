from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import StockViewSet

router = DefaultRouter()

router.register(r'stock-api/investor/stocks', StockViewSet, basename='stock')

urlpatterns = [
    path('', include(router.urls)),
]
