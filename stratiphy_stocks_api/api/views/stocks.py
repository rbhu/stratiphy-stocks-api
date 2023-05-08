from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from api.models import Stock
from api.permissions import IsInvestor, IsAdmin
from api.serializers import StockSerializer


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['stock_name', 'short_code']
    permission_classes = [IsInvestor, IsAdmin]

    def get_permissions(self):
        if (self.action == 'list') | (self.action == 'retrieve'):
            # Investors can ony list or retrieve stock info, but not create / modify / delete
            permission_classes = [IsInvestor | IsAdmin]
        else:
            permission_classes = [IsAdmin]

        return [permission() for permission in permission_classes]

