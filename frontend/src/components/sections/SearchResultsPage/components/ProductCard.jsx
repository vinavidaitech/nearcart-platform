import {
  Home,
  Star,
  CheckCircle,
  Monitor,
  MapPin,
  Navigation,
  BarChart2,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import ShoePlaceholder from "@/components/sections/SearchResultsPage/components/ShoePlaceholder";
import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";
import ColorSwatch from "@/components/sections/SearchResultsPage/components/ColorSwatch";

export default function ProductCard({ product }) {
  const navigate = useNavigate();
  const {
    id,
    name,
    store,
    address,
    rating,
    reviewCount,
    price,
    inStock,
    sizeAvailable,
    aisle,
    aisleDistance,
    distance,
    badges,
    swatches,
    shoeColor,
  } = product;

  return (
    <div className="bg-bg border border-border rounded-xl p-5 flex flex-col sm:flex-row gap-5 shadow-card transition-shadow duration-200 hover:shadow-md">
      {/* Shoe image */}
      <div
        className="w-full sm:w-[148px] h-[140px] sm:h-[110px] rounded-md overflow-hidden shrink-0 border border-border cursor-pointer"
        onClick={() => navigate(`/product/${id}`)}
      >
        <ShoePlaceholder colorHex={shoeColor} />
      </div>

      {/* Info */}
      <div className="flex-1 min-w-0">
        {/* Top row */}
        <div className="flex items-start justify-between gap-2 mb-1.5">
          <h3
            className="font-bold text-[0.9375rem] leading-snug cursor-pointer hover:text-primary transition-colors duration-150"
            style={{
              fontFamily: "var(--font-display)",
              color: "var(--color-text-heading)",
            }}
            onClick={() => navigate(`/product/${id}`)}
          >
            {name}
          </h3>
          <div className="flex gap-1.5 shrink-0 flex-wrap justify-end">
            {badges.map((b) => (
              <Badge key={b.label} variant={b.variant}>
                {b.label}
              </Badge>
            ))}
          </div>
        </div>

        {/* Store name */}
        <div className="flex items-center gap-1.5 mb-0.5">
          <div
            className="w-[18px] h-[18px] rounded flex items-center justify-center shrink-0"
            style={{ background: "var(--color-icon-blue-bg)" }}
          >
            <Home size={11} color="var(--color-icon-blue)" strokeWidth={2.5} />
          </div>
          <span
            className="font-semibold text-sm"
            style={{
              fontFamily: "var(--font-display)",
              color: "var(--color-text-body)",
            }}
          >
            {store}
          </span>
        </div>

        {/* Address */}
        <p
          className="text-[0.8125rem] mb-2"
          style={{
            color: "var(--color-text-muted)",
            fontFamily: "var(--font-body)",
          }}
        >
          {address}
        </p>

        {/* Rating & Price */}
        <div className="flex items-center gap-3 mb-2">
          <div className="flex items-center gap-1">
            <Star
              size={14}
              fill="var(--color-star)"
              color="var(--color-star)"
              strokeWidth={1}
            />
            <span
              className="font-bold text-sm"
              style={{
                fontFamily: "var(--font-display)",
                color: "var(--color-text-heading)",
              }}
            >
              {rating}
            </span>
            <span
              className="text-[0.8125rem]"
              style={{
                color: "var(--color-text-muted)",
                fontFamily: "var(--font-body)",
              }}
            >
              ({reviewCount})
            </span>
          </div>
          <span
            className="font-extrabold text-lg"
            style={{
              fontFamily: "var(--font-display)",
              color: "var(--color-text-heading)",
            }}
          >
            ₹{price.toLocaleString("en-IN")}
          </span>
        </div>

        {/* Availability row */}
        <div className="flex flex-wrap items-center gap-3 mb-2.5">
          <div className="flex items-center gap-1">
            <CheckCircle
              size={14}
              color="var(--color-success)"
              strokeWidth={2.5}
            />
            <span
              className="text-[0.8125rem] font-semibold"
              style={{
                fontFamily: "var(--font-display)",
                color: "var(--color-success)",
              }}
            >
              {inStock ? "In Stock" : "Out of Stock"} · {sizeAvailable}
            </span>
          </div>
          <div className="flex items-center gap-1">
            <Monitor
              size={14}
              color="var(--color-text-muted)"
              strokeWidth={2}
            />
            <span
              className="text-[0.8125rem]"
              style={{
                color: "var(--color-text-muted)",
                fontFamily: "var(--font-body)",
              }}
            >
              {aisle} · {aisleDistance}
            </span>
          </div>
          <div className="flex items-center gap-1">
            <MapPin size={14} color="var(--color-text-muted)" strokeWidth={2} />
            <span
              className="text-[0.8125rem]"
              style={{
                color: "var(--color-text-muted)",
                fontFamily: "var(--font-body)",
              }}
            >
              {distance}
            </span>
          </div>
        </div>

        {/* Bottom row: swatches + buttons */}
        <div className="flex items-center justify-between gap-3 flex-wrap">
          {/* Color swatches */}
          <div className="flex gap-1.5 items-center">
            {swatches.map((c, i) => (
              <ColorSwatch key={i} color={c} />
            ))}
          </div>

          {/* Action buttons */}
          <div className="flex gap-2 flex-wrap">
            <Button
              variant="primary"
              size="sm"
              onClick={() => navigate(`/product/${id}`)}
            >
              View Store
            </Button>
            <button
              className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-md border border-border bg-transparent font-semibold text-[0.8125rem] cursor-pointer transition-colors duration-150 hover:bg-surface"
              style={{
                fontFamily: "var(--font-display)",
                color: "var(--color-text-body)",
              }}
            >
              <Navigation size={14} strokeWidth={2} />
              Navigate
            </button>
            <button
              className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-md border border-border bg-transparent font-semibold text-[0.8125rem] cursor-pointer transition-colors duration-150 hover:bg-surface"
              style={{
                fontFamily: "var(--font-display)",
                color: "var(--color-text-body)",
              }}
            >
              <BarChart2 size={14} strokeWidth={2} />
              Compare
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
