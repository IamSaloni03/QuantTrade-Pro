import { Link, useLocation } from "react-router-dom";

const Sidebar = () => {
  const location = useLocation();

  const navItems = [
    { name: "Dashboard", path: "/" },
    { name: "Portfolio", path: "/portfolio" },
    { name: "Trading", path: "/trading" },
    { name: "Market", path: "/market" },
  ];

  return (
    <aside className="w-60 bg-white border-r border-gray-200">
      <div className="px-6 py-6 border-b border-gray-200">
        <h1 className="text-lg font-semibold tracking-tight">
          QuantTrade Pro
        </h1>
      </div>

      <nav className="p-4 space-y-2">
        {navItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`block px-4 py-2 rounded-md text-sm transition ${
              location.pathname === item.path
                ? "bg-gray-100 font-medium"
                : "text-gray-600 hover:bg-gray-50"
            }`}
          >
            {item.name}
          </Link>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;
