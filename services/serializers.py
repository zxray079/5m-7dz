from rest_framework import serializers
from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    final_price = serializers.ReadOnlyField()

    class Meta:
        model = Service
        fields = [
            'id',
            'title',
            'description',
            'category',
            'price',
            'discount',
            'final_price',
            'is_active',
            'author',
            'created_at',
        ]
        read_only_fields = ['author', 'created_at', 'final_price']