# src/apps/strategies/performance_metrics.py

def calculate_win_rate(trades):
    total_trades = 0
    winning_trades = 0
    buy_price = None

    for trade in trades:
        if trade["type"] == "BUY":
            buy_price = trade["price"]

        elif trade["type"] == "SELL" and buy_price is not None:
            total_trades += 1

            if trade["price"] > buy_price:
                winning_trades += 1

            buy_price = None

    win_rate = (winning_trades / total_trades) if total_trades > 0 else 0
    return win_rate, total_trades


def calculate_max_drawdown(equity_curve):
    if not equity_curve:
        return 0

    peak = equity_curve[0]["equity"]
    max_drawdown = 0

    for point in equity_curve:
        equity = point["equity"]

        if equity > peak:
            peak = equity

        if peak > 0:
            drawdown = (equity - peak) / peak
            max_drawdown = min(max_drawdown, drawdown)

    return max_drawdown


def calculate_sharpe_ratio(equity_curve):
    returns = []

    for i in range(1, len(equity_curve)):
        prev = equity_curve[i - 1]["equity"]
        curr = equity_curve[i]["equity"]

        if prev != 0:
            returns.append((curr - prev) / prev)

    if not returns:
        return 0

    avg_return = sum(returns) / len(returns)
    variance = sum((r - avg_return) ** 2 for r in returns) / len(returns)
    std_dev = variance ** 0.5

    return avg_return / std_dev if std_dev != 0 else 0