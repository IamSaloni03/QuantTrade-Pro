import api from "../../api/axios";

export const fetchAssets = async () => {
  const response = await api.get("assets/");
  return response.data;
};

export const searchAssets = async (query) => {
  const response = await api.get(`assets/?search=${query}`);
  return response.data;
};

export const fetchLatestPrice = async (assetId) => {
  const response = await api.get(`assets/${assetId}/latest_price/`);
  return response.data;
};
