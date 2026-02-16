import { formatCurrency } from "../../shared/utils/format";


const OrderHistory = ({ trades, assets }) => {
  if (!trades || trades.length === 0) {
    return (
      <div className="bg-white border border-gray-200 p-5 rounded-lg shadow-sm hover:shadow-md transition">
        <h3 className="text-sm font-semibold mb-4">Order History</h3>
        <p className="text-sm text-gray-500">No trades yet</p>
      </div>
    );
  }

  return (
    <div className="bg-white border border-gray-200 p-5 rounded-lg shadow-sm hover:shadow-md transition">
      <h3 className="text-sm font-semibold mb-4">Order History</h3>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-xs text-gray-500 uppercase border-b">
              <th className="text-left py-2">Type</th>
              <th className="text-left py-2">Asset</th>
              <th className="text-right py-2">Qty</th>
              <th className="text-right py-2">Price</th>
              <th className="text-right py-2">Total</th>
              <th className="text-right py-2">Date</th>
              

            </tr>
          </thead>

          <tbody>
            {trades
              .slice()
              .reverse()
              .map((trade) => {
                const total =
                  trade.quantity * parseFloat(trade.price);

                return (
                  <tr
                    key={trade.id}
                    className="border-b last:border-none"
                  >
                    <td
                      className={`py-3 font-medium ${
                        trade.trade_type === "buy"
                          ? "text-green-600"
                          : "text-red-600"
                      }`}
                    >
                      {trade.trade_type.toUpperCase()}
                    </td>

                      {/* ASSET */}
  <td className="py-3 font-medium">
    {
      assets.find(a => a.id === trade.asset)?.symbol
      || trade.asset
    }
  </td>

                    <td className="text-right">
                      {trade.quantity}
                    </td>

                    <td className="text-right">
                      ₹ {formatCurrency(parseFloat(trade.price))}
                    </td>

                    <td className="text-right">
                      ₹ {formatCurrency(total)}
                    </td>

                    <td className="text-right text-gray-500">
                      {new Date(trade.trade_date).toLocaleString()}
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
