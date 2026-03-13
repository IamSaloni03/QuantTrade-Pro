import axios from "axios";

console.log("BACKTEST PAYLOAD SENT");

export const runBacktest = async (asset) => {
  return axios.post("http://localhost:8000/api/strategies/backtest/run/", {
    asset_symbol: asset,
    initial_capital: 100000,
    strategy_type: "moving_average",
    short_window: 3,
    long_window: 5
  });
};