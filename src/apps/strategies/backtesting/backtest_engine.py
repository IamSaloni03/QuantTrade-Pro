from statistics import variance

from src.apps.data_pipeline.models import MarketData
from src.apps.trading.models import Asset
from src.apps.strategies.implementations.moving_average import MovingAverageStrategy
from src.apps.strategies.performance_metrics import (
    calculate_win_rate,
    calculate_max_drawdown,
    calculate_sharpe_ratio
)
from src.apps.strategies.sentiment import get_market_sentiment
from src.apps.strategies.strategy_factory import get_strategy

class BacktestEngine:

    def run_multiple_backtests(self, strategies, asset_symbol, initial_capital, short_window, long_window):
        results = []

        for strategy_type in strategies:
            result = self.run_backtest(
                asset_symbol,
                initial_capital,
                strategy_type,
                short_window,
                long_window
                )

            result["strategy"] = strategy_type
            results.append(result)

        return results

    

    def run_backtest(self, asset_symbol, initial_capital, strategy_type, short_window, long_window):

        if initial_capital <= 0:
            raise ValueError("Initial capital must be greater than 0")

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

        sentiment_score = get_market_sentiment()
        
        for i in range(start_index, len(market_data)):

            window = market_data[:i]

            strategy = get_strategy(
                strategy_type,
                asset,
                window,
                short_window=short_window,
                long_window=long_window
                )
            
            signal = strategy.generate_signal()

            price = float(market_data[i].close_price)

            if signal == "BUY" and position == 0 and sentiment_score > -0.2:
                position = capital / price
                capital = 0

                trades.append({
                    "type": "BUY",
                    "price": price,
                    "time": market_data[i].timestamp.isoformat()
                })

            elif signal == "SELL" and position > 0:
                capital = position * price
                position = 0

                trades.append({
                    "type": "SELL",
                    "price": price,
                    "time": market_data[i].timestamp.isoformat()
                })
            
            current_value = capital + (position * price)
            
            equity_curve.append({
                "time": market_data[i].timestamp.isoformat(),
                "equity": current_value
})

            


        final_value = capital + (position * float(market_data[-1].close_price))

        win_rate, total_trades = calculate_win_rate(trades)
        max_drawdown = calculate_max_drawdown(equity_curve)
        sharpe_ratio = calculate_sharpe_ratio(equity_curve)
        


        return {
            "initial_capital": initial_capital,
            "final_value": final_value,
            "total_trades": total_trades,
            "win_rate": round(win_rate, 4),
            "max_drawdown": round(max_drawdown, 4),
            "sharpe_ratio": round(sharpe_ratio, 4),
            "sentiment_score": round(sentiment_score, 4),
            "profit": round(final_value - initial_capital, 2),
            "trades": trades,
            "equity_curve": equity_curve,

            }
    
    def run_portfolio_backtest(self, assets, initial_capital, strategy_type, short_window, long_window):

        results = []
        capital_per_asset = initial_capital / len(assets)

        combined_equity = {}

        for asset_symbol in assets:

            result = self.run_backtest(
                asset_symbol=asset_symbol,
                initial_capital=capital_per_asset,
                strategy_type=strategy_type,
                short_window=short_window,
                long_window=long_window
                )

            results.append({
                "asset": asset_symbol,
                "strategy": strategy_type,
                "result": result
                })

            # Combine equity curves
            for point in result["equity_curve"]:
                time = point["time"]
                equity = point["equity"]

                if time not in combined_equity:
                    combined_equity[time] = 0

                combined_equity[time] += equity

        # Convert combined equity to list
        combined_equity_curve = [
            {"time": time, "equity": equity}
            for time, equity in sorted(combined_equity.items())
            ]

        portfolio_value = sum(r["result"]["final_value"] for r in results)

        # --- PORTFOLIO METRICS ---

        portfolio_returns = []

        for i in range(1, len(combined_equity_curve)):
            prev = combined_equity_curve[i - 1]["equity"]
            curr = combined_equity_curve[i]["equity"]

            if prev != 0:
                portfolio_returns.append((curr - prev) / prev)

        # Sharpe Ratio
        if portfolio_returns:
            avg_return = sum(portfolio_returns) / len(portfolio_returns)
            variance = sum((r - avg_return) ** 2 for r in portfolio_returns) / len(portfolio_returns)
            std_dev = variance ** 0.5
            portfolio_sharpe = avg_return / std_dev if std_dev != 0 else 0
        else:
            portfolio_sharpe = 0

        #Max Drawdown
        peak = combined_equity_curve[0]["equity"] if combined_equity_curve else 0
        portfolio_drawdown = 0

        for point in combined_equity_curve:
            equity = point["equity"]

            if equity > peak:
                peak = equity

            if peak > 0:
                drawdown = (equity - peak) / peak
                portfolio_drawdown = min(portfolio_drawdown, drawdown)
        
        return { 
             "portfolio": {
                 "value": round(portfolio_value, 2)
                 },
                 "assets": results,
                 "equity_curve": combined_equity_curve,
                 "portfolio_metrics": {
                     "sharpe_ratio": round(portfolio_sharpe, 4),
                     "max_drawdown": round(portfolio_drawdown, 4)
                     }
                     }