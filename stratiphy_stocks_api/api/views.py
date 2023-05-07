from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, status
from .models import Stock, UserStock
from .serializers import StockSerializer, StockTransactionSerializer
from .permissions import IsInvestor


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['stock_name', 'short_code']
    permission_classes = [IsInvestor]


class StockTransactionViewSet(ModelViewSet):
    serializer_class = StockTransactionSerializer
    permission_classes = [IsInvestor]

    def create(self, request):
        stock_id = request.data.get('stockId')
        quantity = int(request.data.get('quantity'))

        try:
            stock = Stock.objects.get(pk=stock_id)
        except Stock.DoesNotExist:
            return Response({'error': 'Stock not found'}, status=status.HTTP_404_NOT_FOUND)

        if stock.quantity < quantity:
            return Response({'error': 'There is not enough stock to purchase this quantity.'}, status=status.HTTP_400_BAD_REQUEST)

        user_stock, created = UserStock.objects.get_or_create(user=request.user, stock=stock)
        user_stock.quantity += quantity
        user_stock.save()

        stock.quantity -= quantity
        stock.save()

        return Response({'message': 'Stock bought successfully'}, status=status.HTTP_201_CREATED)