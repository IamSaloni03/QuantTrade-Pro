import { useState } from "react";
import { runBacktest } from "./api";
import axios from "axios";

export const useBacktest = () => {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const executeBacktest = async (asset) => {
    console.log("FUNCTION STARTED", asset);

    try {
      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/api/strategies/backtest/run/", // ✅ WITH SLASH
        {
          strategy_type: "moving_average",
          asset_symbol: asset,
          initial_capital: 10000,
          short_window: 5,
          long_window: 20,
        }
      );

      console.log("RESPONSE:", response.data);

      const data = Array.isArray(response.data)
        ? response.data[0]
        : response.data;

      setResult(data);

    } catch (error) {
      console.error("ERROR:", error);
    } finally {
      setLoading(false);
    }
  };

  return { result, loading, executeBacktest };
};

