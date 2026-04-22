
import MarketChart from "../features/market/MarketChart";
import Watchlist from "../features/assets/Watchlist";
import { useAssets } from "../features/assets/hooks";

const Market = () => {
  const assetsState = useAssets();

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-xl font-semibold mb-6">
        Market
      </h1>

      <div className="grid grid-cols-12 gap-6">

        {/* LEFT - ASSET LIST */}
        <div className="col-span-3">
          <div className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm">
            <Watchlist assets={assetsState?.assets || []} />
          </div>
        </div>

        {/* RIGHT - CHART */}
        <div className="col-span-9">
          <div className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm">
            <MarketChart />
          </div>
        </div>

      </div>
    </div>
  );
};

export default Market;

