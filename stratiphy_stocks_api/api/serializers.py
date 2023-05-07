from rest_framework import serializers
from .models import Stock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['stock_id', 'stock_name', 'short_code', 'price', 'quantity']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation


class StockTransactionSerializer(serializers.Serializer):
    stockId = serializers.IntegerField()
    quantity = serializers.IntegerField()


class HoldingsSerializer(serializers.Serializer):
    stockId = serializers.CharField()
    quantity = serializers.IntegerField()
    currentStockPrice = serializers.DecimalField(max_digits=10, decimal_places=2)
    totalHoldingValue = serializers.DecimalField(max_digits=10, decimal_places=2)
