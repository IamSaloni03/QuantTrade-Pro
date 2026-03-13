from src.apps.data_pipeline.models import MarketData
from src.apps.trading.models import Asset
from src.apps.strategies.implementations.moving_average import MovingAverageStrategy


class BacktestEngine:

    

    def run_backtest(self, asset_symbol, initial_capital, strategy_type, short_window, long_window):

        print("ENGINE PARAMS:", short_window, long_window)

        capital = initial_capital

        asset = Asset.objects.get(symbol=asset_symbol)

        market_data = list(
    MarketData.objects.filter(
        asset_symbol=asset_symbol
    ).order_by("timestamp"))
        
        if not market_data:
            raise ValueError(f"No market data found for asset: {asset_symbol}")
        
        required_data = max(short_window, long_window)

        if len(market_data) <= required_data:
            raise ValueError(
                f"Not enough market data. Required at least {required_data} rows but found {len(market_data)}.")

        capital = initial_capital
        position = 0
        trades = []

        equity_curve = []

        start_index = max(short_window, long_window)
        
        for i in range(start_index, len(market_data)):

            window = market_data[:i]

            if strategy_type == "moving_average":
                strategy = MovingAverageStrategy(
                    asset,
                    window,
                    short_window=short_window,
                    long_window=long_window
                    )
            else:
                raise ValueError(f"Unsupported strategy: {strategy_type}")
            
            signal = strategy.generate_signal()

            price = float(market_data[i].close_price)

            if signal == "BUY" and position == 0:
                position = capital / price
                capital = 0

                trades.append({
                    "type": "BUY",
                    "price": price,
                    "time": market_data[i].timestamp
                })

            elif signal == "SELL" and position > 0:
                capital = position * price
                position = 0

                trades.append({
                    "type": "SELL",
                    "price": price,
                    "time": market_data[i].timestamp
                })
            
            current_value = capital + (position * price)
            
            equity_curve.append({
                "time": market_data[i].timestamp,
                "equity": current_value
})

            


        final_value = capital + (position * float(market_data[-1].close_price))

        total_trades = len(trades) // 2

        return {
            "initial_capital": initial_capital,
            "final_value": final_value,
            "profit": final_value - initial_capital,
            "trades": trades,
            "equity_curve": equity_curve,
            "total_trades": total_trades

            }