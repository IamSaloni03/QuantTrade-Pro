from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Asset, Portfolio, Trade
from .serializers import AssetSerializer, PortfolioSerializer, TradeSerializer

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    


class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    
    @action(detail=True, methods=["get"])
    def summary(self, request, pk=None):
        """
        Return portfolio valuation summary (historical and live).
        """
        portfolio = self.get_object()

        data = {
            "id": portfolio.id,
            "name": portfolio.name,
            "user": portfolio.user.username,
            "historical_value": portfolio.historical_value(),
            "current_value": portfolio.current_value(),
        }
        return Response(data)
    

class TradeViewSet(viewsets.ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer

