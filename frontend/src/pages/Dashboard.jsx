
import Watchlist from "../features/assets/Watchlist";
import MarketChart from "../features/market/MarketChart";
import PortfolioSummary from "../features/portfolios/PortfolioSummary";
import TradeForm from "../features/trading/TradeForm";
import { useTrades } from "../features/trading/hooks";
import PositionsTable from "../features/portfolios/PositionsTable";
import OrderHistory from "../features/trading/OrderHistory";
import { useAssets } from "../features/assets/hooks";

const Dashboard = () => {
  const tradesState = useTrades();
  const assetsState = useAssets();

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-xl font-semibold mb-6">Dashboard</h1>

      <div className="grid grid-cols-12 gap-6">

        {/* LEFT PANEL */}
        <div className="col-span-3 space-y-6">

          <div className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm">
            <Watchlist assets={assetsState.assets} />
          </div>

          <div className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm">
            <TradeForm />
          </div>

        </div>

        {/* RIGHT PANEL */}
        <div className="col-span-9 space-y-6">

          <div className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm">
            <PortfolioSummary tradesState={tradesState} />
          </div>

          <div className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm">
            <PositionsTable />
          </div>

          <div className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm">
            <OrderHistory trades={tradesState.trades} assets={assetsState.assets} />
          </div>

          <div className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm">
            <MarketChart />
          </div>

        </div>
      </div>
    </div>
  );
};

export default Dashboard;

