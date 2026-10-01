from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'service',
            'client_name',
            'phone',
            'comment',
            'created_at',
        ]
        read_only_fields = ['created_at']

    def validate_service(self, value):
        if not value.is_active:
            raise serializers.ValidationError(
                'Эта услуга сейчас не принимает заказы.'
            )

        return value