from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, status
from .models import Stock, UserStock
from .serializers import StockSerializer, StockTransactionSerializer, HoldingsSerializer
from .permissions import IsInvestor


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['stock_name', 'short_code']
    permission_classes = [IsInvestor]


class BuyStockTransactionViewSet(ModelViewSet):
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


class SellStockTransactionViewSet(ModelViewSet):
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


class StockHoldingsViewSet(ModelViewSet):
    serializer_class = HoldingsSerializer
    queryset = UserStock.objects.all()

    def list(self, request, *args, **kwargs):
        user = request.user
        user_stocks = UserStock.objects.filter(user=user)

        holdings = []
        for user_stock in user_stocks:
            stock = user_stock.stock
            current_stock_price = stock.price
            total_holding_value = current_stock_price * user_stock.quantity

            holding_data = {
                'stockId': user_stock.stock_id,
                'quantity': user_stock.quantity,
                'currentStockPrice': current_stock_price,
                'totalHoldingValue': total_holding_value
            }
            holdings.append(holding_data)

        response_data = {'holdings': holdings}
        return Response(response_data)
