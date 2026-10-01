from django.conf import settings
from django.core.validators import (
    MinLengthValidator,
    MinValueValidator,
    MaxValueValidator,
)
from django.db import models
from decimal import Decimal


class Service(models.Model):
    CATEGORY_CHOICES = [
        ('repair', 'Ремонт'),
        ('cleaning', 'Уборка'),
        ('education', 'Обучение'),
        ('beauty', 'Красота'),
        ('it', 'IT'),
        ('other', 'Другое'),
    ]

    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(5)]
    )

    description = models.TextField()

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(90)
        ]
    )

    is_active = models.BooleanField(default=True)

    order_count = models.PositiveIntegerField(default=0)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='services'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def final_price(self):
        return (
            self.price
            * (Decimal('1') - self.discount / Decimal('100'))
        ).quantize(Decimal('0.01'))

    def __str__(self):
        return self.title