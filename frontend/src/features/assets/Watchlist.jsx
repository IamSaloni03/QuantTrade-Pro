import { useAssets } from "./hooks";

const Watchlist = ({ assets = [] }) => {
  return (
    <div className="bg-white border border-gray-200 p-5 rounded-lg shadow-sm hover:shadow-md transition">

      <h3 className="text-sm font-semibold mb-4">Watchlist</h3>

      {assets.length === 0 ? (
        <p className="text-sm text-gray-500">
          No assets available
        </p>
      ) : (
        <div className="space-y-2">
          {assets.map((asset) => (
            <div
              key={asset.id}
              className="flex flex-col px-3 py-2 rounded-md hover:bg-gray-100 transition cursor-pointer"
            >
              <span className="text-sm font-medium text-gray-800">
                {asset.symbol}
              </span>
              <span className="text-xs text-gray-500 truncate">
                {asset.name}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};




export default Watchlist;
