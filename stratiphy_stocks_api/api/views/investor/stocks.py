from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from api.models import Stock
from api.permissions import IsInvestor
from api.serializers import StockSerializer


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['stock_name', 'short_code']
    permission_classes = [IsInvestor]

