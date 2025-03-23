from order.models import Order
from rest_framework import serializers

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['table_number', 'items']
        
    def create(self, validated_data):
        items = validated_data.get('items', '')
        total_price = 0
        
        for item in items.split(','):
            if '/' in item:
                try:
                    _, price = item.split('/')
                    total_price += int(price)
                except ValueError:
                    pass
        validated_data['total_price'] = total_price
        validated_data['status'] = 'В ожидании'
        
        return super().create(validated_data)
