import { useEffect, useState } from "react";
import { fetchMarketData } from "./api";

export const useMarketData = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadMarketData = async () => {
      try {
        const response = await fetchMarketData();

        // Transform backend data for chart
        const formatted = response.map((item) => ({
          date: new Date(item.timestamp).toLocaleDateString(),
          close: parseFloat(item.close_price),
        }));

        setData(formatted);
      } catch (err) {
        setError("Failed to fetch market data");
      } finally {
        setLoading(false);
      }
    };

    loadMarketData();
  }, []);

  return { data, loading, error };
};
