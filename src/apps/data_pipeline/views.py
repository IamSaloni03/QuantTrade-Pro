from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import MarketData, NewsFeed
from .serializers import MarketDataSerializer, NewsFeedSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


class MarketDataViewSet(viewsets.ModelViewSet):
    queryset = MarketData.objects.all()
    serializer_class = MarketDataSerializer

class NewsFeedViewSet(viewsets.ModelViewSet):
    queryset = NewsFeed.objects.all()
    serializer_class = NewsFeedSerializer

@api_view(["GET"])
def get_market_data(request):
    data = [
        {"timestamp": "2024-01-01", "close_price": 100},
        {"timestamp": "2024-01-02", "close_price": 105},
        {"timestamp": "2024-01-03", "close_price": 102},
        {"timestamp": "2024-01-04", "close_price": 110},
    ]
    return Response(data)
