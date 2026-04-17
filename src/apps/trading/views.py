from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db.models import Max
from django.db.models import OuterRef, Subquery
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
                "price": float(latest_md.close_price)  # ✅ FIX: ensure number
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


# ✅ GLOBAL MARKET API (CLEANED)
def latest_prices(request):

    VALID_SYMBOLS = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "NIFTY50"]

    # Subquery to get latest price per symbol
    latest_price_subquery = MarketData.objects.filter(
        asset_symbol=OuterRef('asset_symbol')
    ).order_by('-timestamp')

    # Main query
    queryset = (
        MarketData.objects
        .filter(asset_symbol__in=VALID_SYMBOLS)
        .values('asset_symbol')
        .distinct()
        .annotate(
            price=Subquery(latest_price_subquery.values('close_price')[:1])
        )
    )

    data = [
        {
            "symbol": item["asset_symbol"],
            "price": round(float(item["price"]), 2)
        }
        for item in queryset
    ]

    return JsonResponse(data, safe=False)
def historical_prices(request, symbol):

    VALID_SYMBOLS = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "NIFTY50"]

    # Validate symbol
    if symbol not in VALID_SYMBOLS:
        return JsonResponse({"error": "Invalid symbol"}, status=400)

    # Fetch historical data
    queryset = (
        MarketData.objects
        .filter(asset_symbol=symbol)
        .order_by('timestamp')
        .values('timestamp', 'close_price')
    )

    data = [
        {
            "timestamp": item["timestamp"].strftime("%Y-%m-%d"),
            "price": round(float(item["close_price"]), 2)
        }
        for item in queryset
    ]

    return JsonResponse(data, safe=False)
@csrf_exempt
def buy_asset(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    data = json.loads(request.body)

    symbol = data.get("symbol")
    quantity = int(data.get("quantity"))
    portfolio_id = data.get("portfolio_id")

    try:
        asset = Asset.objects.get(symbol=symbol)
        portfolio = Portfolio.objects.get(id=portfolio_id)

        # Get latest market price
        latest_md = (
            MarketData.objects
            .filter(asset_symbol=symbol)
            .latest("timestamp")
        )

        price = latest_md.close_price

        # Create trade
        trade = Trade(
            portfolio=portfolio,
            asset=asset,
            trade_type="buy",
            quantity=quantity,
            price=price
        )

        trade.full_clean()  # ✅ triggers validation
        trade.save()

        return JsonResponse({
            "message": "Buy successful",
            "symbol": symbol,
            "quantity": quantity,
            "price": float(price)
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def sell_asset(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    data = json.loads(request.body)

    symbol = data.get("symbol")
    quantity = int(data.get("quantity"))
    portfolio_id = data.get("portfolio_id")

    try:
        asset = Asset.objects.get(symbol=symbol)
        portfolio = Portfolio.objects.get(id=portfolio_id)

        # Get latest market price
        latest_md = (
            MarketData.objects
            .filter(asset_symbol=symbol)
            .latest("timestamp")
        )

        price = latest_md.close_price

        # Create sell trade
        trade = Trade(
            portfolio=portfolio,
            asset=asset,
            trade_type="sell",
            quantity=quantity,
            price=price
        )

        trade.full_clean()  # ✅ validates quantity
        trade.save()

        return JsonResponse({
            "message": "Sell successful",
            "symbol": symbol,
            "quantity": quantity,
            "price": float(price)
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def portfolio_detail(request, portfolio_id):

    try:
        portfolio = Portfolio.objects.get(id=portfolio_id)

        trades = portfolio.trade_set.select_related("asset")

        holdings = {}

        for trade in trades:
            symbol = trade.asset.symbol

            holdings.setdefault(symbol, 0)

            if trade.trade_type == "buy":
                holdings[symbol] += trade.quantity
            elif trade.trade_type == "sell":
                holdings[symbol] -= trade.quantity

        # Remove zero holdings
        holdings = {k: v for k, v in holdings.items() if v > 0}

        data = []

        total_value = 0

        for symbol, qty in holdings.items():
            try:
                latest_md = (
                    MarketData.objects
                    .filter(asset_symbol=symbol)
                    .latest("timestamp")
                )

                price = float(latest_md.close_price)
                value = price * qty
                total_value += value

                data.append({
                    "symbol": symbol,
                    "quantity": qty,
                    "price": round(price, 2),
                    "value": round(value, 2)
                })

            except MarketData.DoesNotExist:
                continue

        return JsonResponse({
            "portfolio_id": portfolio.id,
            "name": portfolio.name,
            "total_value": round(total_value, 2),
            "holdings": data
        })

    except Portfolio.DoesNotExist:
        return JsonResponse({"error": "Portfolio not found"}, status=404)