import api from "../../api/axios";

import axios from "axios";

const API_BASE = "http://localhost:8000/api";

export const fetchTrades = async () => {
  const response = await axios.get(`${API_BASE}/trades/`);
  return response.data;
};

export const createTrade = async (tradeData) => {
  const response = await axios.post(`${API_BASE}/trades/`, tradeData);
  return response.data;
};



