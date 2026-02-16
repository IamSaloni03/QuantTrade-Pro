import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainLayout from "./layout/MainLayout";

import Dashboard from "../pages/Dashboard";
import Trading from "../pages/Trading";
import Portfolio from "../pages/Portfolio";
import Market from "../pages/Market";

const AppRoutes = () => {
  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/trading" element={<Trading />} />
          <Route path="/portfolio" element={<Portfolio />} />
          <Route path="/market" element={<Market />} />
        </Routes>
      </MainLayout>
    </BrowserRouter>
  );
};

export default AppRoutes;

