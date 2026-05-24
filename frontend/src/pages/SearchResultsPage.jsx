// pages/SearchResultsPage.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import ProductCard from "@/components/sections/SearchResultsPage/components/ProductCard";
import SearchHeader from "@/components/sections/SearchResultsPage/SearchHeader";
import CategoryNav from "@/components/sections/SearchResultsPage/CategoryNav";
import FilterRow from "@/components/sections/SearchResultsPage/FilterRow";
import SuggestionCard from "@/components/sections/SearchResultsPage/components/SuggestionCard";
import { products, suggestions } from "@/constants/data";

export default function SearchResultsPage() {
  const [query, setQuery] = useState("Nike Air Max 270 size 10");
  const [activeCategory, setActiveCategory] = useState("");
  const [activeFilters, setActiveFilters] = useState([]);

  const toggleFilter = (f) => {
    setActiveFilters((prev) =>
      prev.includes(f) ? prev.filter((x) => x !== f) : [...prev, f],
    );
  };

  return (
    <div
      className="min-h-screen"
      style={{ background: "var(--color-surface)" }}
    >
      <SearchHeader query={query} setQuery={setQuery} userName="Satheesh" />
      <CategoryNav
        activeCategory={activeCategory}
        setActiveCategory={setActiveCategory}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 pb-16">
        {/* Search meta */}
        <p
          className="text-sm mb-3.5"
          style={{
            color: "var(--color-text-muted)",
            fontFamily: "var(--font-body)",
          }}
        >
          Showing {products.length} results for{" "}
          <strong
            style={{
              color: "var(--color-text-heading)",
              fontFamily: "var(--font-display)",
            }}
          >
            Nike Air Max 270 Size 10
          </strong>
        </p>

        {/* Filter row */}
        <div className="mb-6">
          <FilterRow
            activeFilters={activeFilters}
            toggleFilter={toggleFilter}
          />
        </div>

        {/* Available Near You */}
        <section>
          <h2
            className="font-extrabold text-xl mb-4"
            style={{
              fontFamily: "var(--font-display)",
              color: "var(--color-text-heading)",
            }}
          >
            Available Near You
          </h2>
          <div className="flex flex-col gap-4">
            {products.map((p) => (
              <ProductCard key={p.id} product={p} />
            ))}
          </div>
        </section>

        {/* You May Also Like */}
        <section className="mt-12">
          <h2
            className="font-extrabold text-xl mb-5"
            style={{
              fontFamily: "var(--font-display)",
              color: "var(--color-text-heading)",
            }}
          >
            You May Also Like
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
            {suggestions.map((s, i) => (
              <SuggestionCard key={i} {...s} />
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

// pages/SearchResultsPage.jsx  ← wired to real Django data
// import { useState } from "react";
// import { Loader2, AlertCircle } from "lucide-react";
// import SearchHeader from "@/components/sections/SearchResultsPage/SearchHeader";
// import CategoryNav from "@/components/sections/SearchResultsPage/CategoryNav";
// import FilterRow from "@/components/sections/SearchResultsPage/FilterRow";
// import ProductCard from "@/components/sections/SearchResultsPage/components/ProductCard";
// import { useProducts, useSearchProducts } from "@/hooks/useProducts";

// export default function SearchResultsPage() {
//   const [query, setQuery] = useState("");
//   const [activeCategory, setActiveCategory] = useState("");
//   const [activeFilters, setActiveFilters] = useState([]);
//
//   const {
//     data: searchData,
//     isLoading: isSearching,
//     isError: searchError,
//   } = useSearchProducts(query);
//
//   const {
//     data: productsData,
//     isLoading: isLoadingAll,
//     isError: allError,
//   } = useProducts({ category: activeCategory });
//
//   const toggleFilter = (f) =>
//     setActiveFilters((prev) =>
//       prev.includes(f) ? prev.filter((x) => x !== f) : [...prev, f]
//     );
//
//   const isSearchActive = query.trim().length > 1;
//   const products = isSearchActive
//     ? (searchData?.results ?? [])
//     : (productsData?.results ?? []);
//   const isLoading = isSearchActive ? isSearching : isLoadingAll;
//   const isError = isSearchActive ? searchError : allError;
//   const totalCount = isSearchActive
//     ? (searchData?.count ?? 0)
//     : (productsData?.count ?? 0);
//
//   return (
//     <div className="min-h-screen" style={{ background: "var(--color-surface)" }}>
//       <SearchHeader query={query} setQuery={setQuery} userName="Satheesh" />
//       <CategoryNav activeCategory={activeCategory} setActiveCategory={setActiveCategory} />
//
//       <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 pb-16">
//         {!isLoading && !isError && (
//           <p className="text-sm mb-3.5" style={{ color: "var(--color-text-muted)", fontFamily: "var(--font-body)" }}>
//             Showing {totalCount} results
//             {isSearchActive && (
//               <> for <strong style={{ color: "var(--color-text-heading)", fontFamily: "var(--font-display)" }}>{query}</strong></>
//             )}
//           </p>
//         )}
//
//         <div className="mb-6">
//           <FilterRow activeFilters={activeFilters} toggleFilter={toggleFilter} />
//         </div>
//
//         {/* Loading */}
//         {isLoading && (
//           <div className="flex items-center justify-center py-24 gap-3">
//             <Loader2 size={28} className="animate-spin" color="var(--color-primary)" />
//             <span className="text-sm font-semibold" style={{ fontFamily: "var(--font-display)", color: "var(--color-text-muted)" }}>
//               Finding products near you...
//             </span>
//           </div>
//         )}
//
//         {/* Error */}
//         {isError && !isLoading && (
//           <div className="flex flex-col items-center justify-center py-24 gap-3 text-center">
//             <AlertCircle size={36} color="var(--color-error)" strokeWidth={1.5} />
//             <p className="font-bold text-base" style={{ fontFamily: "var(--font-display)", color: "var(--color-text-heading)" }}>
//               Something went wrong
//             </p>
//             <p className="text-sm" style={{ color: "var(--color-text-muted)", fontFamily: "var(--font-body)" }}>
//               Could not connect to the server. Please try again.
//             </p>
//           </div>
//         )}
//
//         {/* Results */}
//         {!isLoading && !isError && products.length > 0 && (
//           <section>
//             <h2 className="font-extrabold text-xl mb-4" style={{ fontFamily: "var(--font-display)", color: "var(--color-text-heading)" }}>
//               Available Near You
//             </h2>
//             <div className="flex flex-col gap-4">
//               {products.map((p) => (
//                 <ProductCard key={p.id} product={p} />
//               ))}
//             </div>
//           </section>
//         )}
//
//         {/* Empty */}
//         {!isLoading && !isError && products.length === 0 && (
//           <div className="flex flex-col items-center justify-center py-24 gap-3 text-center">
//             <p className="font-bold text-base" style={{ fontFamily: "var(--font-display)", color: "var(--color-text-heading)" }}>
//               No products found
//             </p>
//             <p className="text-sm" style={{ color: "var(--color-text-muted)", fontFamily: "var(--font-body)" }}>
//               Try a different search term or category.
//             </p>
//           </div>
//         )}
//       </main>
//     </div>
//   );
// }
