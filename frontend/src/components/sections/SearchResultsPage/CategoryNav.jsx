// components/sections/SearchResultsPage/CategoryNav.jsx
import { ChevronDown } from "lucide-react";

const categories = [
  "Groceries",
  "Dairy",
  "Snacks",
  "Beverages",
  "Personal Care",
  "Home Care",
  "Fresh Produce",
  "Baby Care",
  "Household",
];

export default function CategoryNav({ activeCategory, setActiveCategory }) {
  return (
    <nav className="bg-[var(--color-bg)] border-b border-[var(--color-border)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex gap-1 overflow-x-auto py-2.5 no-scrollbar">
        {categories.map((cat) => {
          const active = cat === activeCategory;
          return (
            <button
              key={cat}
              onClick={() => setActiveCategory(cat)}
              className="shrink-0 inline-flex items-center gap-1 px-3.5 py-1.5 rounded-full border font-semibold text-sm cursor-pointer transition-all duration-150 whitespace-nowrap"
              style={{
                fontFamily: "var(--font-display)",
                borderColor: active
                  ? "var(--color-primary)"
                  : "var(--color-border)",
                background: active
                  ? "var(--color-primary-light)"
                  : "transparent",
                color: active
                  ? "var(--color-primary)"
                  : "var(--color-text-muted)",
              }}
            >
              {cat}
              <ChevronDown size={12} strokeWidth={2.5} />
            </button>
          );
        })}
      </div>
    </nav>
  );
}
