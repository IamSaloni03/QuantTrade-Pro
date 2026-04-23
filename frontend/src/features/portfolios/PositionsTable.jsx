
import { useMarketData } from "../market/hooks";
import { formatCurrency } from "../../shared/utils/format";

const PositionsTable = ({ trades = [], assets = [] }) => {
  const { data: marketData } = useMarketData();

  if (!trades || trades.length === 0) {
    return (
      <div className="bg-white border border-gray-200 p-5 rounded-lg shadow-sm">
        <h3 className="text-sm font-medium text-gray-700 mb-4">
          Positions
        </h3>
        <p className="text-sm text-gray-500">
          No positions available
        </p>
      </div>
    );
  }

  const latestPrice =
    marketData && marketData.length > 0
      ? marketData[marketData.length - 1].close
      : 0;

  // Group trades into positions
  const positions = trades.reduce((acc, trade) => {
    const key = trade.asset;

    if (!acc[key]) {
      acc[key] = {
        quantity: 0,
        totalCost: 0,
      };
    }

    const qty =
      trade.trade_type === "buy"
        ? trade.quantity
        : -trade.quantity;

    acc[key].quantity += qty;
    acc[key].totalCost +=
      trade.quantity * parseFloat(trade.price);

    return acc;
  }, {});

  const rows = Object.entries(positions).map(
    ([assetId, position]) => {
      const avgPrice =
        position.quantity !== 0
          ? position.totalCost / Math.abs(position.quantity)
          : 0;

      const currentValue =
        position.quantity * latestPrice;

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
        pnl,
        pnlPercent,
      };
    }
  );

  return (
    <div className="bg-white border border-gray-200 p-5 rounded-lg shadow-sm">
      <h3 className="text-sm font-medium text-gray-700 mb-4">
        Positions
      </h3>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-xs text-gray-400 uppercase border-b border-gray-200 tracking-wide">
              <th className="text-left py-2 px-2">Asset</th>
              <th className="text-right py-2 px-2">Qty</th>
              <th className="text-right py-2 px-2">Avg Price</th>
              <th className="text-right py-2 px-2">Current</th>
              <th className="text-right py-2 px-2">PnL</th>
              <th className="text-right py-2 px-2">%</th>
            </tr>
          </thead>

          <tbody>
            {rows.map((row) => {
              const isProfit = row.pnl >= 0;

              return (
                <tr
                  key={row.assetId}
                  className="border-b border-gray-100 last:border-none hover:bg-gray-50 transition"
                >
                  {/* ASSET */}
                  <td className="py-3 px-2 font-medium">
                    {
                      (assets || []).find(
                        (a) => a.id === Number(row.assetId)
                      )?.symbol || `Asset ${row.assetId}`
                    }
                  </td>

                  {/* QTY */}
                  <td className="text-right py-3 px-2">
                    {row.quantity}
                  </td>

                  {/* AVG PRICE */}
                  <td className="text-right py-3 px-2">
                    ₹ {formatCurrency(row.avgPrice)}
                  </td>

                  {/* CURRENT */}
                  <td className="text-right py-3 px-2">
                    ₹ {formatCurrency(latestPrice)}
                  </td>

                  {/* PNL */}
                  <td
                    className={`text-right py-3 px-2 font-semibold ${
                      isProfit
                        ? "text-green-600"
                        : "text-red-600"
                    }`}
                  >
                    ₹ {formatCurrency(row.pnl)}
                  </td>

                  {/* PNL % */}
                  <td
                    className={`text-right py-3 px-2 font-semibold ${
                      isProfit
                        ? "text-green-600"
                        : "text-red-600"
                    }`}
                  >
                    {row.pnlPercent}%
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default PositionsTable;

