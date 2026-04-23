from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import BacktestRequestSerializer
from .backtesting.backtest_engine import BacktestEngine


class BacktestView(APIView):

    def post(self, request):

        serializer = BacktestRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        asset_symbol = serializer.validated_data["asset_symbol"]
        assets = request.data.get("assets", [asset_symbol])
        capital = serializer.validated_data["initial_capital"]
        strategy_type = serializer.validated_data["strategy_type"]
        short_window = serializer.validated_data["short_window"]
        long_window = serializer.validated_data["long_window"]

        # ✅ VALIDATION
        if short_window >= long_window:
            return Response(
                {"error": "short_window must be less than long_window"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if capital <= 0:
            return Response(
                {"error": "initial capital must be greater than 0"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ DEFAULTS
        short_window = short_window or 5
        long_window = long_window or 20

        engine = BacktestEngine()

        try:
            # 🔹 PORTFOLIO BACKTEST
            if len(assets) > 1:
                result = engine.run_portfolio_backtest(
                    assets=assets,
                    initial_capital=capital,
                    strategy_type=strategy_type,
                    short_window=short_window,
                    long_window=long_window
                )
                return Response(result)

            # 🔹 SINGLE ASSET BACKTEST
            result = engine.run_backtest(
                asset_symbol=asset_symbol,
                initial_capital=capital,
                strategy_type=strategy_type,
                short_window=short_window,
                long_window=long_window
            )

            return Response(result)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )