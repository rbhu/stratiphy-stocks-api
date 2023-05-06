from rest_framework.viewsets import ModelViewSet
from .models import Stock
from .serializers import StockSerializer


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
