from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'client_name',
        'phone',
        'service',
        'created_at',
    )
    search_fields = (
        'client_name',
        'phone',
        'comment',
    )
    list_filter = ('created_at',)