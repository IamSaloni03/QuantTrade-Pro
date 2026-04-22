
import { formatCurrency } from "../../shared/utils/format";

const OrderHistory = ({ trades = [], assets = [] }) => {
  if (!trades || trades.length === 0) {
    return (
      <div className="bg-white border border-gray-200 p-5 rounded-lg shadow-sm">
        <h3 className="text-sm font-medium text-gray-700 mb-4">
          Order History
        </h3>
        <p className="text-sm text-gray-500">No trades yet</p>
      </div>
    );
  }

  return (
    <div className="bg-white border border-gray-200 p-5 rounded-lg shadow-sm">
      <h3 className="text-sm font-medium text-gray-700 mb-4">
        Order History
      </h3>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-xs text-gray-400 uppercase border-b border-gray-200 tracking-wide">
              <th className="text-left py-2 px-2">Type</th>
              <th className="text-left py-2 px-2">Asset</th>
              <th className="text-right py-2 px-2">Qty</th>
              <th className="text-right py-2 px-2">Price</th>
              <th className="text-right py-2 px-2">Total</th>
              <th className="text-right py-2 px-2">Date</th>
            </tr>
          </thead>

          <tbody>
            {(trades || [])
              .slice()
              .reverse()
              .map((trade) => {
                const total =
                  trade.quantity * parseFloat(trade.price);

                return (
                  <tr
                    key={trade.id}
                    className="border-b border-gray-100 last:border-none hover:bg-gray-50 transition"
                  >
                    {/* TYPE BADGE */}
                    <td className="py-3 px-2">
                      <span
                        className={`px-2 py-1 text-xs rounded font-medium ${
                          trade.trade_type === "buy"
                            ? "bg-green-100 text-green-700"
                            : "bg-red-100 text-red-700"
                        }`}
                      >
                        {trade.trade_type.toUpperCase()}
                      </span>
                    </td>

                    {/* ASSET */}
                    <td className="py-3 px-2 font-medium">
                      {
                        (assets || []).find(
                          (a) => a.id === trade.asset
                        )?.symbol || trade.asset
                      }
                    </td>

                    {/* QTY */}
                    <td className="text-right py-3 px-2">
                      {trade.quantity}
                    </td>

                    {/* PRICE */}
                    <td className="text-right py-3 px-2">
                      ₹ {formatCurrency(parseFloat(trade.price))}
                    </td>

                    {/* TOTAL */}
                    <td className="text-right py-3 px-2">
                      ₹ {formatCurrency(total)}
                    </td>

                    {/* DATE */}
                    <td className="text-right py-3 px-2 text-gray-500">
                      {new Date(trade.trade_date).toLocaleDateString(
                        "en-IN",
                        {
                          day: "numeric",
                          month: "short",
                        }
                      )}{" "}
                      {new Date(trade.trade_date).toLocaleTimeString(
                        "en-IN",
                        {
                          hour: "2-digit",
                          minute: "2-digit",
                        }
                      )}
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

export default OrderHistory;

