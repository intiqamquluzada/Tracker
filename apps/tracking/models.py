from django.db import models
from services.mixin import DateMixin
from services.choices import FREQUENCY_CHOICES
from apps.users.models import User


class Stock(DateMixin):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    expected_price = models.DecimalField(max_digits=10, decimal_places=2,
                                         null=True)

    def __str__(self):
        return self.symbol


class Subscription(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=3, choices=FREQUENCY_CHOICES)

    def __str__(self):
        return f"{self.user.full_name} - {self.stock.symbol}"


class Alert(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    threshold_price = models.DecimalField(max_digits=10, decimal_places=2)
    triggered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.full_name} - {self.stock.symbol} - {self.threshold_price}"


class PriceHistory(DateMixin):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('stock', 'date')

    def __str__(self):
        return f"{self.stock.symbol} - {self.date} - {self.price}"