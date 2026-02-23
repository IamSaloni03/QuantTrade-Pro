import api from "../../api/axios";

export const fetchAssetPosition = async (portfolioId, assetId) => {
  const response = await api.get(
    `portfolios/${portfolioId}/asset_position/?asset_id=${assetId}`
  );
  return response.data;
};
