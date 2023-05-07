from rest_framework.viewsets import ModelViewSet

from api.models import Stock
from api.permissions import IsAdmin
from api.serializers import StockSerializer


class StockAdminViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAdmin]


