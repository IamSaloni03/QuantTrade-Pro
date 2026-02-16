import api from "../../api/axios";

export const fetchMarketData = async () => {
  const response = await api.get("marketdata/");
  return response.data;
};
