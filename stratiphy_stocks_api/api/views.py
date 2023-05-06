from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from .models import Stock
from .serializers import StockSerializer
from .permissions import IsInvestor


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['stock_name', 'short_code']
    permission_classes = [IsInvestor]
