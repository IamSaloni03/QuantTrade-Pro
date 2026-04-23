from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from src.apps.trading.models import Asset
from src.apps.data_pipeline.models import MarketData
from src.apps.strategies.implementations.moving_average import MovingAverageStrategy


class SignalsView(APIView):

    def get(self, request):
        signals = []

        assets = Asset.objects.all()

        for asset in assets:
            data = list(
                MarketData.objects.filter(
                    asset_symbol=asset.symbol
                ).order_by("timestamp")
            )

            if len(data) < 20:
                continue

            strategy = MovingAverageStrategy(
                asset,
                data,
                short_window=5,
                long_window=20
            )

            signal = strategy.generate_signal()

            signals.append({
                "symbol": asset.symbol,
                "signal": signal
            })

        return Response(signals, status=status.HTTP_200_OK)