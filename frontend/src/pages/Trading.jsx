
import TradeForm from "../features/trading/TradeForm";
import OrderHistory from "../features/trading/OrderHistory";
import { useTrades } from "../features/trading/hooks";
import { useAssets } from "../features/assets/hooks";

const Trading = () => {
  const tradesState = useTrades();
  const assetsState = useAssets();

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-xl font-semibold mb-6">
        Trading
      </h1>

      <div className="grid grid-cols-12 gap-6">

        {/* LEFT - ORDER FORM */}
        <div className="col-span-4">
          <div className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm">
            <TradeForm />
          </div>
        </div>

        {/* RIGHT - ORDER HISTORY */}
        <div className="col-span-8">
          <div className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm">
            <OrderHistory
              trades={tradesState?.trades || []}
              assets={assetsState?.assets || []}
            />
          </div>
        </div>

      </div>
    </div>
  );
};

export default Trading;

