// components/sections/SearchResultsPage/components/SuggestionCard.jsx
import { useNavigate } from "react-router-dom";
import ShoePlaceholder from "@/components/sections/SearchResultsPage/components/ShoePlaceholder";

export default function SuggestionCard({ id, name, price, shoeColor }) {
  const navigate = useNavigate();
  return (
    <div
      className="bg-[var(--color-bg)] border border-[var(--color-border)] rounded-[var(--radius-xl)] overflow-hidden shadow-[var(--shadow-card)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[var(--shadow-md)] cursor-pointer"
      onClick={() => navigate(`/product/${id}`)}
    >
      <div className="h-40 p-3">
        <ShoePlaceholder colorHex={shoeColor} />
      </div>
      <div className="px-4 pb-4 pt-3">
        <h4
          className="font-bold text-[0.9375rem] mb-1.5"
          style={{
            fontFamily: "var(--font-display)",
            color: "var(--color-text-heading)",
          }}
        >
          {name}
        </h4>
        <p
          className="font-extrabold text-[1.0625rem]"
          style={{
            fontFamily: "var(--font-display)",
            color: "var(--color-text-heading)",
          }}
        >
          ₹{price.toLocaleString("en-IN")}
        </p>
      </div>
    </div>
  );
}
