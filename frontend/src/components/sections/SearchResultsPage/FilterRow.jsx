// components/sections/SearchResultsPage/FilterRow.jsx
import { useState } from "react";
import { SlidersHorizontal, ChevronDown } from "lucide-react";

const filterOptions = ["Price", "Distance", "Brand", "Rating", "Availability"];

export default function FilterRow({ activeFilters, toggleFilter }) {
  const [sort, setSort] = useState("Nearest First");

  return (
    <div className="flex items-center justify-between gap-3 flex-wrap">
      {/* Left: filter chips */}
      <div className="flex items-center gap-2 flex-wrap">
        <div className="w-8 h-8 rounded-[var(--radius-sm)] border border-[var(--color-border)] flex items-center justify-center cursor-pointer bg-[var(--color-bg)] hover:bg-[var(--color-surface)] transition-colors duration-150">
          <SlidersHorizontal
            size={16}
            color="var(--color-text-muted)"
            strokeWidth={2}
          />
        </div>

        {filterOptions.map((f) => {
          const active = activeFilters.includes(f);
          return (
            <button
              key={f}
              onClick={() => toggleFilter(f)}
              className="px-3.5 py-1.5 rounded-full border font-semibold text-sm cursor-pointer transition-all duration-150"
              style={{
                fontFamily: "var(--font-display)",
                borderColor: active
                  ? "var(--color-primary)"
                  : "var(--color-border)",
                background: active
                  ? "var(--color-primary-light)"
                  : "var(--color-bg)",
                color: active
                  ? "var(--color-primary)"
                  : "var(--color-text-body)",
              }}
            >
              {f}
            </button>
          );
        })}
      </div>

      {/* Right: Sort */}
      <div className="flex items-center gap-2">
        <span
          className="text-sm whitespace-nowrap"
          style={{
            color: "var(--color-text-muted)",
            fontFamily: "var(--font-body)",
          }}
        >
          Sort by:
        </span>
        <div className="relative">
          <select
            value={sort}
            onChange={(e) => setSort(e.target.value)}
            className="pl-3 pr-8 py-1.5 rounded-[var(--radius-md)] border border-[var(--color-border)] bg-[var(--color-bg)] font-semibold text-sm cursor-pointer outline-none appearance-none"
            style={{
              fontFamily: "var(--font-display)",
              color: "var(--color-text-body)",
            }}
          >
            <option>Nearest First</option>
            <option>Price: Low to High</option>
            <option>Price: High to Low</option>
            <option>Best Rated</option>
          </select>
          <ChevronDown
            size={12}
            strokeWidth={2.5}
            className="absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none"
            color="var(--color-text-muted)"
          />
        </div>
      </div>
    </div>
  );
}
