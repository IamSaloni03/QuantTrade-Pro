import { useState } from "react";
import { runBacktest } from "./api";

export const useBacktest = () => {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const executeBacktest = async (asset) => {
    setLoading(true);

    try {
      const response = await runBacktest(asset);
      setResult(response.data);
      console.log("Backtest result:", response.data);
    } catch (err) {
      console.error("Backtest failed", err);
    }

    setLoading(false);
  };

  return { result, loading, executeBacktest };
};