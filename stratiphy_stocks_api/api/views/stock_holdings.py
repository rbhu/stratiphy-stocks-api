from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.models import UserStock
from api.permissions import IsInvestor
from api.serializers import HoldingsSerializer


class StockHoldingsViewSet(ViewSet):
    serializer_class = HoldingsSerializer
    queryset = UserStock.objects.all()
    permission_classes = [IsInvestor]

    def list(self, request):
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
