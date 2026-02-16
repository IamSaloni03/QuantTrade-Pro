import { useEffect, useState, useCallback } from "react";
import { fetchTrades } from "./api";

export const useTrades = () => {
  const [trades, setTrades] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadTrades = useCallback(async () => {
    try {
      setLoading(true);
      const data = await fetchTrades();
      setTrades(data);
      setError(null);
    } catch (err) {
      setError("Failed to fetch trades");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadTrades();
  }, [loadTrades]);

  return { trades, loading, error, refetch: loadTrades };
};
