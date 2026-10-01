from django.core.cache import cache

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Service
from .serializers import ServiceSerializer


class IsOwnerOrAdmin(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.author == request.user


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().order_by('-created_at')
    serializer_class = ServiceSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = ['category', 'is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'top']:
            return [AllowAny()]

        return [IsOwnerOrAdmin()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        cache.delete('top_services')

    @action(detail=False, methods=['get'], url_path='top')
    def top(self, request):
        data = cache.get('top_services')

        if data is None:
            services = Service.objects.filter(
                is_active=True
            ).order_by(
                '-order_count',
                '-created_at'
            )[:5]

            data = ServiceSerializer(
                services,
                many=True
            ).data

            cache.set(
                'top_services',
                data,
                300
            )

        return Response(data)