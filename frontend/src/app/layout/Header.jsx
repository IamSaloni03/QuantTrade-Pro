import { useLocation } from "react-router-dom";

const Header = () => {
  const location = useLocation();

  const pageTitleMap = {
    "/": "Dashboard",
    "/portfolio": "Portfolio",
    "/trading": "Trading",
    "/market": "Market",
  };

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4">
      <h2 className="text-base font-semibold">
        {pageTitleMap[location.pathname] || "QuantTrade Pro"}
      </h2>
    </header>
  );
};

export default Header;
