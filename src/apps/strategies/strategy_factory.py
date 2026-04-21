# src/apps/strategies/strategy_factory.py

from src.apps.strategies.implementations.moving_average import MovingAverageStrategy
# from src.apps.strategies.implementations.rsi import RSIStrategy (later)


def get_strategy(strategy_type, asset, window, **kwargs):
    
    if strategy_type == "moving_average":
        return MovingAverageStrategy(
            asset,
            window,
            short_window=kwargs.get("short_window"),
            long_window=kwargs.get("long_window")
        )

    # Future extension
    # elif strategy_type == "rsi":
    #     return RSIStrategy(asset, window, period=kwargs.get("period"))

    else:
        raise ValueError(f"Unsupported strategy: {strategy_type}")