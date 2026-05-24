// components/sections/SearchResultsPage/SearchHeader.jsx
import { Search, User } from "lucide-react";
import Logo from "@/components/ui/Logo";

export default function SearchHeader({ query, setQuery, userName }) {
  return (
    <header className="bg-[var(--color-bg)] border-b border-[var(--color-border)] sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center gap-5">
        {/* Logo */}
        <a href="/" className="shrink-0 no-underline">
          <Logo />
        </a>

        {/* Search bar */}
        <div className="flex-1 flex items-center bg-[var(--color-bg)] border border-[var(--color-border)] rounded-full overflow-hidden px-4 gap-2.5 max-w-[600px] transition-colors duration-150 focus-within:border-[var(--color-primary)]">
          <Search
            size={18}
            color="var(--color-text-muted)"
            strokeWidth={2}
            className="shrink-0"
          />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1 border-none outline-none py-2.5 text-[0.9375rem] bg-transparent"
            style={{
              fontFamily: "var(--font-body)",
              color: "var(--color-text-body)",
            }}
          />
        </div>

        {/* User greeting */}
        <div className="shrink-0 flex items-center gap-2 ml-auto">
          <div className="w-8 h-8 rounded-full bg-[var(--color-surface)] border border-[var(--color-border)] flex items-center justify-center">
            <User size={16} color="var(--color-text-muted)" strokeWidth={2} />
          </div>
          <span
            className="font-semibold text-[0.9375rem] hidden sm:block"
            style={{
              fontFamily: "var(--font-display)",
              color: "var(--color-text-body)",
            }}
          >
            Hi, {userName}!
          </span>
        </div>
      </div>
    </header>
  );
}
