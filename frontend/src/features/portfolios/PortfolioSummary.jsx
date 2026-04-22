
import { useMarketData } from "../market/hooks";
import { formatCurrency } from "../../shared/utils/format";

const PortfolioSummary = ({ tradesState }) => {
  const trades = tradesState?.trades || [];
  const tradesLoading = tradesState?.loading;
  const tradesError = tradesState?.error;

  const { data: marketData } = useMarketData();

  if (tradesLoading) {
    return (
      <div className="bg-white border border-gray-200 p-5 rounded-lg shadow-sm">
        <p className="text-sm text-gray-500">Loading portfolio...</p>
      </div>
    );
  }

  if (tradesError) {
    return (
      <div className="bg-white border border-gray-200 p-5 rounded-lg shadow-sm">
        <p className="text-sm text-red-500">{tradesError}</p>
      </div>
    );
  }

  const totalTrades = trades.length;

  const totalQuantity = trades.reduce(
    (sum, trade) => sum + trade.quantity,
    0
  );

  const totalInvested = trades.reduce(
    (sum, trade) =>
      sum + trade.quantity * parseFloat(trade.price),
    0
  );

  const latestMarketPrice =
    marketData && marketData.length > 0
      ? marketData[marketData.length - 1].close
      : 0;

  const currentValue = totalQuantity * latestMarketPrice;

  const unrealizedPnL = currentValue - totalInvested;
  const isProfit = unrealizedPnL >= 0;

  const pnlPercent =
    totalInvested > 0
      ? ((unrealizedPnL / totalInvested) * 100).toFixed(2)
      : 0;

  return (
    <div className="bg-white border border-gray-200 p-5 rounded-lg shadow-sm">
      <h3 className="text-sm font-medium text-gray-700 mb-4">
        Portfolio Summary
      </h3>

      <div className="space-y-3 text-sm">

        <div className="flex justify-between">
          <span className="text-gray-500">Total Trades</span>
          <span className="font-medium">{totalTrades}</span>
        </div>

        <div className="flex justify-between">
          <span className="text-gray-500">Total Quantity</span>
          <span className="font-medium">{totalQuantity}</span>
        </div>

        <div className="flex justify-between">
          <span className="text-gray-500">Total Invested</span>
          <span className="font-medium">
            ₹ {formatCurrency(totalInvested)}
          </span>
        </div>

        <div className="flex justify-between">
          <span className="text-gray-500">Current Value</span>
          <span className="font-medium">
            ₹ {formatCurrency(currentValue)}
          </span>
        </div>

        <div className="flex justify-between">
          <span className="text-gray-500">Unrealized PnL</span>
          <span
            className={`font-semibold ${
              isProfit ? "text-green-600" : "text-red-600"
            }`}
          >
            ₹ {formatCurrency(unrealizedPnL)}
          </span>
        </div>

        {/* PnL % FIXED */}
        <div className="flex justify-between">
          <span className="text-gray-500">PnL %</span>
          <span
            className={`px-2 py-1 rounded text-sm font-medium ${
              isProfit
                ? "bg-green-100 text-green-700"
                : "bg-red-100 text-red-700"
            }`}
          >
            {pnlPercent}%
          </span>
        </div>

      </div>
    </div>
  );
};

export default PortfolioSummary;

