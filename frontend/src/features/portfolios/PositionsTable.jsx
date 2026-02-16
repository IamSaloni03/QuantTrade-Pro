import { useMarketData } from "../market/hooks";
import { formatCurrency } from "../../shared/utils/format";


const PositionsTable = ({ trades, assets }) => {
  const { data: marketData } = useMarketData();

  if (!trades || trades.length === 0) {
    return (
      <div className="bg-white border border-gray-200 p-5 rounded-lg shadow-sm hover:shadow-md transition">
        <h3 className="text-sm font-semibold mb-4">Positions</h3>
        <p className="text-sm text-gray-500">No positions available</p>
      </div>
    );
  }

  const latestPrice =
    marketData && marketData.length > 0
      ? marketData[marketData.length - 1].close
      : 0;

  // Group trades by asset
  const positions = trades.reduce((acc, trade) => {
    const key = trade.asset;

    if (!acc[key]) {
      acc[key] = {
        quantity: 0,
        totalCost: 0
      };
    }

    const qty = trade.trade_type === "buy"
      ? trade.quantity
      : -trade.quantity;

    acc[key].quantity += qty;
    acc[key].totalCost += trade.quantity * parseFloat(trade.price);

    return acc;
  }, {});

  const rows = Object.entries(positions).map(([assetId, position]) => {
    const avgPrice =
      position.quantity !== 0
        ? position.totalCost / Math.abs(position.quantity)
        : 0;

    const currentValue = position.quantity * latestPrice;
    const invested = position.totalCost;
    const pnl = currentValue - invested;
    const pnlPercent =
      invested !== 0
        ? ((pnl / invested) * 100).toFixed(2)
        : 0;

    return {
      assetId,
      ...position,
      avgPrice,
      currentValue,
      pnl,
      pnlPercent
    };
  });

  return (
  <div className="bg-white border border-gray-200 p-5 rounded-lg shadow-sm hover:shadow-md transition">
    <h3 className="text-sm font-semibold mb-4">Positions</h3>

    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="text-xs text-gray-500 uppercase border-b">
            <th className="text-left py-2">Asset</th>
            <th className="text-right py-2">Qty</th>
            <th className="text-right py-2">Avg Price</th>
            <th className="text-right py-2">Current</th>
            <th className="text-right py-2">PnL</th>
            <th className="text-right py-2">%</th>
          </tr>
        </thead>

        <tbody>
          {rows.map((row) => (
            <tr key={row.assetId} className="border-b last:border-none">
              <td className="py-3 font-medium">
                {
  assets.find(a => a.id === Number(row.assetId))?.symbol 
  || `Asset ${row.assetId}`
}

              </td>

              <td className="text-right">
                {row.quantity}
              </td>

              <td className="text-right">
                ₹ {formatCurrency(row.avgPrice)}
              </td>

              <td className="text-right">
                ₹ {formatCurrency(latestPrice)}
              </td>

              <td
                className={`text-right font-semibold ${
                  row.pnl >= 0
                    ? "text-green-600"
                    : "text-red-600"
                }`}
              >
                ₹ {formatCurrency(row.pnl)}
              </td>

              <td
                className={`text-right font-semibold ${
                  row.pnl >= 0
                    ? "text-green-600"
                    : "text-red-600"
                }`}
              >
                {row.pnlPercent}%
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);
};

export default PositionsTable;
