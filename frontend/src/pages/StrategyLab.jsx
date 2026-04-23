import { useState } from "react";
import { useBacktest } from "../features/strategies/hooks";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Scatter
} from "recharts";

export default function StrategyLab() {
  const [asset, setAsset] = useState("RELIANCE");

  const { result, loading, executeBacktest } = useBacktest();

  const buyTrades =
  result?.trades?.filter((t) => t.type === "BUY") || [];
  
  const sellTrades =
  result?.trades?.filter((t) => t.type === "SELL") || [];

  const buyMarkers = buyTrades.map(t => ({
  time: t.time,
  equity: t.price
  }));

  const sellMarkers = sellTrades.map(t => ({
    time: t.time,
    equity: t.price
  }));

  const run = () => {
    executeBacktest(asset);
  };

  return (
    <div className="p-6">

      <h1 className="text-xl font-bold mb-4">
        Strategy Lab
      </h1>

      <div className="flex gap-4 mb-6">

        <input
          value={asset}
          onChange={(e) => setAsset(e.target.value)}
          className="border p-2"
        />

        <button
          onClick={run}
          className="bg-blue-600 text-white px-4 py-2"
        >
          Run Backtest
        </button>

      </div>

      {loading && <p>Running backtest...</p>}

      {result && (
        <div className="space-y-2">

          <p>Initial Capital: ₹{result.initial_capital}</p>

          <p>Final Value: ₹{result.final_value}</p>

          <p className="font-semibold">
            Profit: ₹{result.profit}
          </p>

          <p>Total Trades: {result.total_trades}</p>


        </div>

        
      )}

      {result?.equity_curve && (

  <div className="mt-8 h-80">

    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={result.equity_curve}>

        <CartesianGrid strokeDasharray="3 3" />

        <XAxis dataKey="time" />

        <YAxis />

        <Tooltip />

        <Line
          type="monotone"
          dataKey="equity"
          stroke="#2563eb"
          strokeWidth={2}
          dot={false}
        />

        <Scatter
        data={buyTrades}
        xAxisId={0}
        yAxisId={0}
        name="BUY"
        dataKey="price"
        fill="green"
        />
        
        <Scatter
        data={sellTrades}
        xAxisId={0}
        yAxisId={0}
        name="SELL"
        dataKey="price"
        fill="red"
        />

      </LineChart>
    </ResponsiveContainer>

  </div>

)}

    </div>
  );
}