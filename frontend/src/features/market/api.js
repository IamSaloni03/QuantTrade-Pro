import api from "../../api/axios";

export const fetchMarketData = async () => {
  const response = await api.get("market-data/");
  return response.data;
};
