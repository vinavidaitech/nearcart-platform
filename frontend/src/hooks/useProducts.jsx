// hooks/useProducts.js
// Drop-in hooks for every component that needs data.
// Usage: const { data, isLoading, isError } = useProducts({ search: "nike" });
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  fetchProducts,
  fetchProductById,
  fetchStores,
  fetchStoreById,
  searchProducts,
  loginUser,
  registerUser,
} from "@/api";

// ── Query Keys ─────────────────────────────────────────────────────────────
// Centralised so invalidation is consistent everywhere.
export const queryKeys = {
  products: (filters) => ["products", filters],
  product: (id) => ["products", id],
  stores: (params) => ["stores", params],
  store: (id) => ["stores", id],
  search: (query) => ["search", query],
};

// ── Products ───────────────────────────────────────────────────────────────

export function useProducts(filters = {}) {
  return useQuery({
    queryKey: queryKeys.products(filters),
    queryFn: () => fetchProducts(filters),
    // Don't fetch if no meaningful filter yet
    enabled: true,
  });
}

export function useProduct(id) {
  return useQuery({
    queryKey: queryKeys.product(id),
    queryFn: () => fetchProductById(id),
    enabled: !!id, // skip if id is null/undefined
  });
}

// ── Search ─────────────────────────────────────────────────────────────────

export function useSearchProducts(query) {
  return useQuery({
    queryKey: queryKeys.search(query),
    queryFn: () => searchProducts(query),
    enabled: query?.trim().length > 1, // only fetch after 2+ characters
    staleTime: 1000 * 30, // search results go stale in 30s
  });
}

// ── Stores ─────────────────────────────────────────────────────────────────

export function useStores(params = {}) {
  return useQuery({
    queryKey: queryKeys.stores(params),
    queryFn: () => fetchStores(params),
  });
}

export function useStore(id) {
  return useQuery({
    queryKey: queryKeys.store(id),
    queryFn: () => fetchStoreById(id),
    enabled: !!id,
  });
}

// ── Auth mutations ─────────────────────────────────────────────────────────

export function useLogin() {
  return useMutation({
    mutationFn: loginUser,
    onSuccess: (data) => {
      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);
    },
  });
}

export function useRegister() {
  return useMutation({
    mutationFn: registerUser,
  });
}
