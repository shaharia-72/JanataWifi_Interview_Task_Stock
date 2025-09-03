from rest_framework import serializers

from .models import stockModel


class StockSerializer(serializers.ModelSerializer):

  class Meta:
    model = stockModel
    fields = '__all__'

  def validate(self, data):
        if data['high_trade'] < data['low_trade']:
            raise serializers.ValidationError({
                "high_trade": "High trade must be greater than or equal to low trade."
            })
        if data['open_trade'] < 0 or data['close_trade'] < 0:
            raise serializers.ValidationError({
                "open_trade/close_trade": "Open and close trades must be non-negative."
            })
        if data['volume'] < 0:
            raise serializers.ValidationError({
                "volume": "Volume must be non-negative."
            })
        return data

  
