from rest_framework import serializers
from .models import SentimentAnalysis, StrategyPerformance

class SentimentAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentimentAnalysis
        fields = '__all__'

class StrategyPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategyPerformance
        fields = '__all__'
