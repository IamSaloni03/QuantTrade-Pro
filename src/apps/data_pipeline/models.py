from django.db import models

# Create your models here.
from src.apps.data_pipeline.constants import VALID_SYMBOLS, is_valid_symbol
SYMBOL_CHOICES = [(symbol, symbol) for symbol in VALID_SYMBOLS]
class MarketData(models.Model):
    asset_symbol = models.CharField(
        max_length=20,
        choices=SYMBOL_CHOICES
    )
    timestamp = models.DateTimeField()
    open_price = models.DecimalField(max_digits=12, decimal_places=2)
    high_price = models.DecimalField(max_digits=12, decimal_places=2)
    low_price = models.DecimalField(max_digits=12, decimal_places=2)
    close_price = models.DecimalField(max_digits=12, decimal_places=2)
    volume = models.PositiveBigIntegerField()

    def __str__(self):
        return f"{self.asset_symbol} @ {self.timestamp}"

    class Meta:
        unique_together = ('asset_symbol', 'timestamp')
class NewsFeed(models.Model):
    asset_symbol = models.CharField(max_length=10)
    headline = models.CharField(max_length=255)
    source = models.CharField(max_length=100)
    published_at = models.DateTimeField()
    url = models.URLField()
    content = models.TextField(blank=True)

    def __str__(self):
        return f"{self.headline} ({self.source})"

