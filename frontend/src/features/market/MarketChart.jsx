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
      <div className="bg-white border border-gray-200 p-5 rounded-lg">
        <p className="text-sm text-gray-500">Loading market data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white border border-gray-200 p-5 rounded-lg shadow-sm hover:shadow-md transition">
        <p className="text-sm text-red-500">{error}</p>
      </div>
    );
  }

  return (
    <div className="bg-white border border-gray-200 p-5 rounded-lg shadow-sm hover:shadow-md transition">
      <h3 className="text-sm font-semibold mb-4">Market Overview</h3>

      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
            <XAxis dataKey="date" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip />
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
