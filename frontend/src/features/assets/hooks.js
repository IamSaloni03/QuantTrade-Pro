import { useEffect, useState } from "react";
import axios from "axios";

const API_BASE = "http://localhost:8000/api";

export const useAssets = () => {
  const [assets, setAssets] = useState([]);

  useEffect(() => {
    const fetchAssets = async () => {
      const response = await axios.get(`${API_BASE}/assets/`);
      setAssets(response.data);
    };

    fetchAssets();
  }, []);

  return assets;
};

