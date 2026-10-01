from django.db.models import F

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .models import Order
from .serializers import OrderSerializer


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        order = serializer.save()

        order.service.__class__.objects.filter(
            id=order.service.id
        ).update(
            order_count=F('order_count') + 1
        )


class MyOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            service__author=self.request.user
        ).order_by('-created_at')


class OrderDeleteView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]