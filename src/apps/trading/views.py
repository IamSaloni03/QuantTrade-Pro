from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Asset, Portfolio, Trade
from .serializers import AssetSerializer, PortfolioSerializer, TradeSerializer

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

class TradeViewSet(viewsets.ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer

