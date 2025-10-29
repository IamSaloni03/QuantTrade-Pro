from django.contrib import admin

# Register your models here.

from .models import SentimentAnalysis, StrategyPerformance

admin.site.register(SentimentAnalysis)
admin.site.register(StrategyPerformance)

