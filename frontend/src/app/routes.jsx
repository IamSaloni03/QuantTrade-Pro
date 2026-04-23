import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainLayout from "./layout/MainLayout";
import Signals from "../pages/Signals";
import Dashboard from "../pages/Dashboard";
import Trading from "../pages/Trading";
import Portfolio from "../pages/Portfolio";
import Market from "../pages/Market";
import StrategyLab from "../pages/StrategyLab";
import Login from "../pages/Login";



const AppRoutes = () => {
  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/trading" element={<Trading />} />
          <Route path="/portfolio" element={<Portfolio />} />
          <Route path="/market" element={<Market />} />
          <Route path="/strategies" element={<StrategyLab />} />
          <Route path="/signals" element={<Signals />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </MainLayout>
    </BrowserRouter>
  );
};

export default AppRoutes;

