
import PortfolioSummary from "../features/portfolios/PortfolioSummary";
import PositionsTable from "../features/portfolios/PositionsTable";
import OrderHistory from "../features/trading/OrderHistory";
import { useTrades } from "../features/trading/hooks";
import { useAssets } from "../features/assets/hooks";

const Portfolio = () => {
  const tradesState = useTrades();
  const assetsState = useAssets();

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-xl font-semibold mb-6">
        Portfolio
      </h1>

      <div className="space-y-6">

        {/* Portfolio Summary */}
        <div className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm">
          <PortfolioSummary tradesState={tradesState} />
        </div>

        {/* Positions */}
        <div className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm">
          <PositionsTable
            trades={tradesState?.trades || []}
            assets={assetsState?.assets || []}
          />
        </div>

        {/* Order History */}
        <div className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm">
          <OrderHistory
            trades={tradesState?.trades || []}
            assets={assetsState?.assets || []}
          />
        </div>

      </div>
    </div>
  );
};

export default Portfolio;

