from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class SentimentAnalysis(models.Model):
    asset_symbol = models.CharField(max_length=10)
    date = models.DateField()
    sentiment_score = models.FloatField()
    news_source = models.CharField(max_length=100)
    analyzed_text = models.TextField()

    def __str__(self):
        return f"{self.asset_symbol} - {self.date} - {self.sentiment_score}"

class StrategyPerformance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    strategy_name = models.CharField(max_length=100)
    date = models.DateField()
    return_pct = models.FloatField()
    sharpe_ratio = models.FloatField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.strategy_name} - {self.date} - {self.return_pct}%"

