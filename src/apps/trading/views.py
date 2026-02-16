from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Asset, Portfolio, Trade
from .serializers import AssetSerializer, PortfolioSerializer, TradeSerializer
from src.apps.data_pipeline.models import MarketData


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['symbol', 'name']

    @action(detail=True, methods=["get"])
    def latest_price(self, request, pk=None):
        asset = self.get_object()
        try:
            latest_md = (
                MarketData.objects
                .filter(asset_symbol=asset.symbol)
                .latest("timestamp")
            )
            return Response({
                "symbol": asset.symbol,
                "price": latest_md.close_price
            })
        except MarketData.DoesNotExist:
            return Response({
                "error": "No market data available"
            }, status=404)


class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

    @action(detail=True, methods=["get"])
    def summary(self, request, pk=None):
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
