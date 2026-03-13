from src.apps.trading.models import Asset
from src.apps.data_pipeline.models import MarketData
from src.apps.strategies.models import Signal
from src.apps.strategies.implementations.moving_average import MovingAverageStrategy


class StrategyRunner:

    def run_moving_average(self, asset_symbol):

        asset = Asset.objects.get(symbol=asset_symbol)

        market_data = MarketData.objects.filter(
            asset_symbol=asset_symbol
        ).order_by("timestamp")

        strategy = MovingAverageStrategy(asset, market_data)

        signal_type = strategy.generate_signal()

        latest_price = market_data.last().close_price

        signal = Signal.objects.create(
            asset=asset,
            strategy="MovingAverage",
            signal_type=signal_type,
            price=latest_price,
            timestamp=market_data.last().timestamp
        )

        return signal