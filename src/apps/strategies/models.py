from django.db import models
from src.apps.trading.models import Asset


class Signal(models.Model):

    SIGNAL_CHOICES = [
        ("BUY", "Buy"),
        ("SELL", "Sell"),
        ("HOLD", "Hold"),
    ]

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    strategy = models.CharField(max_length=100)

    signal_type = models.CharField(max_length=10, choices=SIGNAL_CHOICES)

    price = models.DecimalField(max_digits=12, decimal_places=2)

    confidence = models.FloatField(default=1.0)

    timestamp = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.strategy} - {self.asset.symbol} - {self.signal_type}"