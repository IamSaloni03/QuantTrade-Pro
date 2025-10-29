from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import SentimentAnalysis, StrategyPerformance
from .serializers import SentimentAnalysisSerializer, StrategyPerformanceSerializer

class SentimentAnalysisViewSet(viewsets.ModelViewSet):
    queryset = SentimentAnalysis.objects.all()
    serializer_class = SentimentAnalysisSerializer

class StrategyPerformanceViewSet(viewsets.ModelViewSet):
    queryset = StrategyPerformance.objects.all()
    serializer_class = StrategyPerformanceSerializer

