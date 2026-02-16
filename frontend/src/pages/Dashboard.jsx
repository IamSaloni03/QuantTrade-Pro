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
  const assets= useAssets();

  return (
    <div className="grid grid-cols-12 gap-6">

      {/* LEFT SIDEBAR */}
      <div className="col-span-3 space-y-6">
        <Watchlist assets={assets}/>
        <TradeForm refetchTrades={tradesState.refetch} />
      </div>

      {/* MAIN CONTENT */}
      <div className="col-span-9 space-y-6">

        <PortfolioSummary tradesState={tradesState} />

        <PositionsTable trades=
        {tradesState.trades} 
        assets={assets}
        />

        <OrderHistory trades=
        {tradesState.trades} 
        assets={assets}
        />

        <MarketChart />

      </div>

    </div>
  );
};



export default Dashboard;


