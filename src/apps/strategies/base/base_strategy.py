class BaseStrategy:
    """
    Base class for all trading strategies.
    Every strategy must implement generate_signal().
    """

    name = "BaseStrategy"

    def __init__(self, asset, market_data):
        self.asset = asset
        self.market_data = market_data

    def generate_signal(self):
        """
        Must return one of:
        BUY
        SELL
        HOLD
        """
        raise NotImplementedError("Strategy must implement generate_signal()")