// lib/queryClient.js
import { QueryClient } from "@tanstack/react-query";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 min — data stays fresh, no refetch
      gcTime: 1000 * 60 * 10, // 10 min — keep unused cache in memory
      retry: 2, // retry failed requests twice
      refetchOnWindowFocus: false, // don't refetch when tab regains focus
    },
    mutations: {
      retry: 0, // don't auto-retry mutations
    },
  },
});

export default queryClient;
