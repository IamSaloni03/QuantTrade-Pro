from src.apps.strategies.base.base_strategy import BaseStrategy


class MovingAverageStrategy(BaseStrategy):

    name = "MovingAverage"

    def __init__(self, asset, market_data, short_window=5, long_window=20):
        super().__init__(asset, market_data)
        self.short_window = short_window
        self.long_window = long_window

    def generate_signal(self):

        prices = [data.close_price for data in self.market_data]

        if len(prices) < self.long_window:
            return "HOLD"

        short_ma = sum(prices[-self.short_window:]) / self.short_window
        long_ma = sum(prices[-self.long_window:]) / self.long_window

        if short_ma > long_ma:
            return "BUY"

        elif short_ma < long_ma:
            return "SELL"

        return "HOLD"