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
        <div className="space-y-3">
          {assets.map((asset) => (
            <div
              key={asset.id}
              className="flex justify-between items-center text-sm border-b border-gray-100 pb-2"
            >
              <span className="font-medium">
                {asset.symbol}
              </span>
              <span className="text-gray-500">
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
