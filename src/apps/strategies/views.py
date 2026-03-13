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
        capital = serializer.validated_data["initial_capital"]

        strategy_type = serializer.validated_data["strategy_type"]

        short_window = serializer.validated_data["short_window"]
        long_window = serializer.validated_data["long_window"]

        print("SHORT WINDOW:", short_window)
        print("LONG WINDOW:", long_window)

        engine = BacktestEngine()

        result = engine.run_backtest(
            asset_symbol=asset_symbol,
            initial_capital=capital,
            strategy_type=strategy_type,
            short_window=short_window,
            long_window=long_window
        )

        return Response(result)