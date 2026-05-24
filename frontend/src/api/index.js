// api/index.js
// All raw API calls live here — hooks import from this file, not axios directly.
// Mirrors your Django URL structure: /api/products/, /api/stores/, etc.
import api from "@/lib/axios";

// ── Products ───────────────────────────────────────────────────────────────

export const fetchProducts = async ({
  search = "",
  category = "",
  page = 1,
} = {}) => {
  const { data } = await api.get("/products/", {
    params: { search, category, page },
  });
  return data; // { results: [], count: 0, next: null, previous: null }
};

export const fetchProductById = async (id) => {
  const { data } = await api.get(`/products/${id}/`);
  return data;
};

// ── Stores ─────────────────────────────────────────────────────────────────

export const fetchStores = async ({ lat, lng, radius = 5 } = {}) => {
  const { data } = await api.get("/stores/", {
    params: { lat, lng, radius },
  });
  return data;
};

export const fetchStoreById = async (id) => {
  const { data } = await api.get(`/stores/${id}/`);
  return data;
};

// ── Search ─────────────────────────────────────────────────────────────────

export const searchProducts = async (query) => {
  const { data } = await api.get("/products/search/", {
    params: { q: query },
  });
  return data;
};

// ── Auth ───────────────────────────────────────────────────────────────────

export const loginUser = async (credentials) => {
  const { data } = await api.post("/auth/token/", credentials);
  return data; // { access, refresh }
};

export const registerUser = async (payload) => {
  const { data } = await api.post("/auth/register/", payload);
  return data;
};
