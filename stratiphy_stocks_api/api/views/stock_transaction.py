from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.models import Stock, UserStock
from api.permissions import IsInvestor
from api.serializers import StockTransactionSerializer


class BuyStockTransactionViewSet(ViewSet):
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
            return Response({'error': 'There is not enough stock to purchase this quantity.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user_stock, created = UserStock.objects.get_or_create(user=request.user, stock=stock)
        user_stock.quantity += quantity
        user_stock.save()

        stock.quantity -= quantity
        stock.save()

        data = {
            'stockId': stock_id,
            'quantity': quantity,
            'totalCost': stock.price * quantity
        }

        return Response(data, status=status.HTTP_201_CREATED)


class SellStockTransactionViewSet(ViewSet):
    serializer_class = StockTransactionSerializer
    permission_classes = [IsInvestor]

    def create(self, request):
        stock_id = request.data.get('stockId')
        quantity = int(request.data.get('quantity'))

        try:
            stock = Stock.objects.get(pk=stock_id)
        except Stock.DoesNotExist:
            return Response({'error': 'Stock not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            user_stock = UserStock.objects.get(user=request.user, stock=stock)
        except UserStock.DoesNotExist:
            return Response({'error': 'User does not hold this stock'}, status=status.HTTP_404_NOT_FOUND)

        if quantity > user_stock.quantity:
            return Response({'error': 'Cannot sell more stock than the user holds'}, status=status.HTTP_400_BAD_REQUEST)

        user_stock.quantity -= quantity
        user_stock.save()

        stock.quantity += quantity
        stock.save()

        data = {
            'stockId': stock_id,
            'quantity': quantity,
            'totalProfit': stock.price * quantity
        }

        return Response(data, status=status.HTTP_201_CREATED)
