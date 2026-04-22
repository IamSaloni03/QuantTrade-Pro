
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import { useMarketData } from "./hooks";

const MarketChart = () => {
  const { data, loading, error } = useMarketData();

  if (loading) {
    return (
      <div className="bg-white border border-gray-200 p-5 rounded-lg shadow-sm">
        <p className="text-sm text-gray-500">Loading market data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white border border-gray-200 p-5 rounded-lg shadow-sm">
        <p className="text-sm text-red-500">{error}</p>
      </div>
    );
  }

  return (
    <div className="bg-white border border-gray-200 p-5 rounded-lg shadow-sm">
      <h2 className="text-sm font-medium text-gray-700 mb-4">
        Market Overview
      </h2>

      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid stroke="#f1f5f9" vertical={false} />

            <XAxis
              dataKey="date"
              tick={{ fontSize: 12 }}
              tickFormatter={(value) =>
                new Date(value).toLocaleDateString("en-IN", {
                  day: "numeric",
                  month: "short",
                })
              }
            />

            <YAxis tick={{ fontSize: 12 }} />

            <Tooltip
              contentStyle={{ fontSize: "12px", borderRadius: "8px" }}
              labelFormatter={(label) =>
                new Date(label).toLocaleDateString()
              }
            />

            <Line
              type="monotone"
              dataKey="close"
              stroke="#2563eb"
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default MarketChart;

