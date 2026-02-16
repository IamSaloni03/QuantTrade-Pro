import { useState, useEffect } from "react";
import { searchAssets } from "../../assets/api";

export default function AssetSearchSelect({ onSelect }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  useEffect(() => {
    if (query.length < 1) {
      setResults([]);
      return;
    }

    const delayDebounce = setTimeout(async () => {
      try {
        const data = await searchAssets(query);
        setResults(data);
      } catch (err) {
        console.error("Search error:", err);
      }
    }, 400);

    return () => clearTimeout(delayDebounce);
  }, [query]);

  return (
    <div className="relative w-full">
      <input
        type="text"
        placeholder="Search asset..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="w-full border px-3 py-2 rounded bg-gray-800 text-white"
      />

      {results.length > 0 && (
        <div className="absolute w-full bg-gray-900 border mt-1 rounded shadow max-h-60 overflow-y-auto z-50">
          {results.map((asset) => (
            <div
              key={asset.id}
              onClick={() => {
                onSelect(asset);
                setQuery(asset.symbol);
                setResults([]);
              }}
              className="px-4 py-2 hover:bg-gray-700 cursor-pointer"
            >
              <div className="font-medium">{asset.symbol}</div>
              <div className="text-sm text-gray-400">
                {asset.name}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
