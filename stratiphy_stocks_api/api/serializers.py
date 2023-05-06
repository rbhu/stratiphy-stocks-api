from rest_framework import serializers
from .models import Stock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['stock_id', 'stock_name', 'short_code', 'price', 'quantity']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

