import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const API_BASE = "http://localhost:8000/api";

const Signals = () => {
  const [signals, setSignals] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const handleSignalClick = (item) => {
    navigate("/trading",{
        state: {
            symbol: item.symbol,
            signal: item.signal,
        },
    })
  };
  
  useEffect(() => {
    const fetchSignals = async () => {
      try {
        const response = await axios.get(`${API_BASE}/strategies/signals/`);
        setSignals(response.data);
      } catch (err) {
        console.error("Failed to fetch signals", err);
      } finally {
        setLoading(false);
      }
    };

    fetchSignals();
  }, []);

  if (loading) {
    return <p className="p-6">Loading signals...</p>;
  }

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-xl font-semibold mb-6">Strategy Signals</h1>

      <div className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm">
        <div className="space-y-3">
          {signals.map((item, index) => (
            <div
              key={index}
              onClick={() => handleSignalClick(item)}
              className="flex justify-between items-center px-4 py-3 rounded-md hover:bg-gray-100"
            >
              <span className="font-medium">{item.symbol}</span>

              <span
                className={`text-sm font-semibold ${
                  item.signal === "BUY"
                    ? "text-green-600"
                    : item.signal === "SELL"
                    ? "text-red-600"
                    : "text-gray-500"
                }`}
              >
                {item.signal}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Signals;