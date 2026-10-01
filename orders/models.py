from django.db import models
from services.models import Service


class Order(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    client_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client_name} — {self.service.title}'
