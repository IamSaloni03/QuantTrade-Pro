from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import MarketData, NewsFeed
from .serializers import MarketDataSerializer, NewsFeedSerializer

class MarketDataViewSet(viewsets.ModelViewSet):
    queryset = MarketData.objects.all()
    serializer_class = MarketDataSerializer

class NewsFeedViewSet(viewsets.ModelViewSet):
    queryset = NewsFeed.objects.all()
    serializer_class = NewsFeedSerializer

