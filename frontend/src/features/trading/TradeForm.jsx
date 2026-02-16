import { useState } from "react";
import { createTrade } from "./api";
import AssetSearchSelect from "./components/AssetSearchSelect";
import { fetchLatestPrice } from "../assets/api";
import { useEffect } from "react";





const TradeForm = ({refetchTrades}) => {
  const [tradeType, setTradeType] = useState("buy");
  const [quantity, setQuantity] = useState("");
  const [price, setPrice] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedAsset, setSelectedAsset] = useState(null);


  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedAsset || !quantity || !price) {
  setError("Please select asset and fill all fields");
  return;
}


    setLoading(true);
    setError(null);

    try {
      await createTrade({
        trade_type: tradeType,
        quantity: parseInt(quantity),
        price: parseFloat(price),
        portfolio: 1,   // assuming portfolio id = 1
        asset: selectedAsset.id
     // assuming asset id = 3
      });
      await refetchTrades(); // Refresh trades after successful creation

      setQuantity("");
      setPrice("");
      setSelectedAsset(null);

    } catch (err) {
      setError("Trade failed. Check backend.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
  const loadPrice = async () => {
    if (!selectedAsset) return;

    try {
      const data = await fetchLatestPrice(selectedAsset.id);
      setPrice(data.price);
    } catch (err) {
      console.error("Failed to fetch latest price", err);
    }
  };

  loadPrice();
}, [selectedAsset]);

  return (
    <div className="bg-white border border-gray-200 p-5 rounded-lg shadow-sm hover:shadow-md transition">
      <h3 className="text-sm font-semibold mb-4">Place Order</h3>

      <form onSubmit={handleSubmit} className="space-y-4">

        <div className="flex space-x-2">
          <button
            type="button"
            onClick={() => setTradeType("buy")}
            className={`flex-1 py-2 rounded-md text-sm font-medium ${
              tradeType === "buy"
                ? "bg-green-600 text-white"
                : "bg-gray-100"
            }`}
          >
            Buy
          </button>

          <button
            type="button"
            onClick={() => setTradeType("sell")}
            className={`flex-1 py-2 rounded-md text-sm font-medium ${
              tradeType === "sell"
                ? "bg-red-600 text-white"
                : "bg-gray-100"
            }`}
          >
            Sell
          </button>
        </div>

        <div>
  <AssetSearchSelect onSelect={setSelectedAsset} />
</div>


        <div>
          <input
            type="number"
            placeholder="Quantity"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            className="w-full border border-gray-200 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
        </div>

        <div>
          <input
            type="number"
            step="0.01"
            placeholder="Price"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            className="w-full border border-gray-200 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
        </div>

        {error && (
          <p className="text-xs text-red-500">{error}</p>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition"
        >
          {loading ? "Placing..." : "Place Order"}
        </button>
      </form>
    </div>
  );
};

export default TradeForm;
