// components/pages/ProductDetailPage.jsx
// UPDATED TO MATCH FIGMA DESIGN

import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  Star,
  CheckCircle,
  MapPin,
  Navigation,
  Monitor,
  Share2,
  Heart,
  ShoppingCart,
  ChevronRight,
  Home,
  Package,
  Zap,
} from "lucide-react";
import SearchHeader from "@/components/sections/SearchResultsPage/SearchHeader";
import ShoePlaceholder from "@/components/sections/SearchResultsPage/components/ShoePlaceholder";
import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";
import { products } from "@/constants/data";

const colorOptions = [
  { hex: "#334155", label: "Slate" },
  { hex: "#1d6be5", label: "Blue" },
  { hex: "#16a34a", label: "Green" },
  { hex: "#dc2626", label: "Red" },
];
const sizes = ["6", "7", "8", "9", "10", "11", "12"];

export default function ProductDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [query, setQuery] = useState("");
  const [selectedColor, setSelectedColor] = useState(colorOptions[0].hex);
  const [selectedSize, setSelectedSize] = useState("10");
  const [wishlisted, setWishlisted] = useState(false);

  const product =
    products.find((p) => String(p.id) === String(id)) || products[0];
  const related = products
    .filter((p) => String(p.id) !== String(id))
    .slice(0, 3);

  const handleNavigate = () => {
    navigate(`/navigate/${product.id}`, {
      state: {
        product,
        userLocation: { lat: 9.9252, lng: 78.1198 }, // Madurai coordinates
      },
    });
  };

  return (
    <div className="min-h-screen bg-surface">
      <SearchHeader query={query} setQuery={setQuery} userName="Guest" />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 pb-16">
        {/* Breadcrumb */}
        <nav
          className="flex items-center gap-1.5 mb-6 text-sm"
          style={{ fontFamily: "var(--font-body)" }}
        >
          <button
            onClick={() => navigate(-1)}
            className="flex items-center gap-1 font-semibold transition-colors duration-150 hover:text-primary cursor-pointer bg-transparent border-none p-0"
            style={{
              color: "var(--color-text-muted)",
              fontFamily: "var(--font-display)",
            }}
          >
            <ArrowLeft size={14} strokeWidth={2.5} />
            Back to Results
          </button>
          <ChevronRight size={14} color="var(--color-text-subtle)" />
          <span
            style={{
              color: "var(--color-text-heading)",
              fontWeight: 600,
              fontFamily: "var(--font-display)",
            }}
          >
            {product.name}
          </span>
        </nav>

        <div className="grid grid-cols-1 lg:grid-cols-[1fr_1.2fr] gap-8">
          {/* ── LEFT: Image + Options ── */}
          <div className="flex flex-col gap-5">
            {/* Product image */}
            <div className="bg-bg border border-border rounded-2xl overflow-hidden shadow-card relative">
              <div className="h-[380px] p-6 bg-gradient-to-br from-surface to-surface-alt flex items-center justify-center">
                <ShoePlaceholder colorHex={selectedColor} />
              </div>

              {/* Wishlist button */}
              <button
                className="absolute top-4 right-4 w-10 h-10 rounded-full bg-white border border-border flex items-center justify-center transition-all duration-150 hover:border-red-300 cursor-pointer shadow-sm hover:shadow-md"
                onClick={() => setWishlisted(!wishlisted)}
              >
                <Heart
                  size={18}
                  strokeWidth={2}
                  fill={wishlisted ? "#ef4444" : "none"}
                  color={wishlisted ? "#ef4444" : "var(--color-text-muted)"}
                />
              </button>

              {/* Badges */}
              <div className="absolute top-4 left-4 flex flex-col gap-2">
                {product.badges.map((b) => (
                  <Badge key={b.label} variant={b.variant}>
                    {b.label}
                  </Badge>
                ))}
              </div>
            </div>

            {/* Color picker */}
            <div className="bg-bg border border-border rounded-xl p-5 shadow-card">
              <p
                className="font-bold text-sm mb-4"
                style={{
                  fontFamily: "var(--font-display)",
                  color: "var(--color-text-heading)",
                }}
              >
                Choose Color
              </p>
              <div className="flex gap-3 flex-wrap">
                {colorOptions.map((c) => (
                  <button
                    key={c.hex}
                    onClick={() => setSelectedColor(c.hex)}
                    className="flex flex-col items-center gap-1.5 cursor-pointer bg-transparent border-none transition-all duration-150"
                  >
                    <div
                      className="w-10 h-10 rounded-full border-2 transition-all duration-150 hover:scale-110"
                      style={{
                        background: c.hex,
                        borderColor:
                          selectedColor === c.hex
                            ? "var(--color-primary)"
                            : "var(--color-border)",
                        boxShadow:
                          selectedColor === c.hex
                            ? "0 0 0 3px var(--color-primary-light)"
                            : "none",
                      }}
                    />
                    <span
                      className="text-xs font-semibold"
                      style={{
                        fontFamily: "var(--font-display)",
                        color:
                          selectedColor === c.hex
                            ? "var(--color-primary)"
                            : "var(--color-text-muted)",
                      }}
                    >
                      {c.label}
                    </span>
                  </button>
                ))}
              </div>
            </div>

            {/* Store location card */}
            <div className="bg-bg border border-border rounded-xl p-5 shadow-card">
              <div className="flex items-start gap-3 mb-4">
                <div
                  className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0"
                  style={{ background: "var(--color-icon-blue-bg)" }}
                >
                  <Home
                    size={18}
                    color="var(--color-icon-blue)"
                    strokeWidth={2}
                  />
                </div>
                <div className="flex-1">
                  <p
                    className="font-bold text-sm"
                    style={{
                      fontFamily: "var(--font-display)",
                      color: "var(--color-text-heading)",
                    }}
                  >
                    {product.store}
                  </p>
                  <p
                    className="text-xs mt-0.5"
                    style={{
                      color: "var(--color-text-muted)",
                      fontFamily: "var(--font-body)",
                    }}
                  >
                    {product.address}
                  </p>
                </div>
              </div>

              <div className="space-y-2 mb-4 pb-4 border-b border-border">
                <div className="flex items-center gap-2">
                  <Monitor
                    size={14}
                    color="var(--color-text-muted)"
                    strokeWidth={2}
                  />
                  <span
                    className="text-xs"
                    style={{
                      color: "var(--color-text-muted)",
                      fontFamily: "var(--font-body)",
                    }}
                  >
                    {product.aisle} · {product.aisleDistance}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <MapPin
                    size={14}
                    color="var(--color-text-muted)"
                    strokeWidth={2}
                  />
                  <span
                    className="text-xs"
                    style={{
                      color: "var(--color-text-muted)",
                      fontFamily: "var(--font-body)",
                    }}
                  >
                    {product.distance} from your location
                  </span>
                </div>
              </div>

              <Button
                variant="primary"
                size="md"
                className="w-full"
                icon={<Navigation size={14} />}
                onClick={handleNavigate}
              >
                Open in Maps
              </Button>
            </div>
          </div>

          {/* ── RIGHT: Product Details ── */}
          <div className="flex flex-col gap-5">
            {/* Main info */}
            <div className="bg-bg border border-border rounded-2xl p-6 shadow-card">
              <div className="flex items-start justify-between gap-3 mb-4">
                <div>
                  <h1
                    className="font-black text-3xl sm:text-4xl leading-tight mb-2"
                    style={{
                      fontFamily: "var(--font-display)",
                      color: "var(--color-text-heading)",
                    }}
                  >
                    {product.name}
                  </h1>
                  <p
                    className="text-sm"
                    style={{
                      color: "var(--color-text-muted)",
                      fontFamily: "var(--font-body)",
                    }}
                  >
                    Premium Athletic Footwear · Unisex
                  </p>
                </div>
                <button className="w-10 h-10 rounded-full bg-surface border border-border flex items-center justify-center shrink-0 cursor-pointer hover:bg-primary-light transition-colors duration-150">
                  <Share2
                    size={16}
                    color="var(--color-text-muted)"
                    strokeWidth={2}
                  />
                </button>
              </div>

              {/* Rating */}
              <div className="flex items-center gap-3 mb-5">
                <div className="flex items-center gap-1">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <Star
                      key={star}
                      size={16}
                      fill={
                        star <= Math.floor(product.rating)
                          ? "var(--color-star)"
                          : "none"
                      }
                      color="var(--color-star)"
                      strokeWidth={1.5}
                    />
                  ))}
                </div>
                <span
                  className="font-bold text-sm"
                  style={{
                    fontFamily: "var(--font-display)",
                    color: "var(--color-text-heading)",
                  }}
                >
                  {product.rating}
                </span>
                <span
                  className="text-sm"
                  style={{
                    color: "var(--color-text-muted)",
                    fontFamily: "var(--font-body)",
                  }}
                >
                  ({product.reviewCount} reviews)
                </span>
              </div>

              {/* Price section */}
              <div className="mb-6 pb-6 border-b border-border">
                <div className="flex items-baseline gap-3">
                  <span
                    className="font-black text-5xl"
                    style={{
                      fontFamily: "var(--font-display)",
                      color: "var(--color-text-heading)",
                    }}
                  >
                    ₹{product.price.toLocaleString("en-IN")}
                  </span>
                  <span
                    className="text-lg line-through"
                    style={{
                      color: "var(--color-text-subtle)",
                      fontFamily: "var(--font-body)",
                    }}
                  >
                    ₹{(product.price * 1.2).toLocaleString("en-IN")}
                  </span>
                  <span
                    className="text-sm font-bold px-2.5 py-1 rounded-full"
                    style={{
                      background: "var(--badge-green-bg)",
                      color: "var(--badge-green-text)",
                      fontFamily: "var(--font-display)",
                    }}
                  >
                    20% OFF
                  </span>
                </div>
              </div>

              {/* Availability */}
              <div
                className="flex items-center gap-2 mb-6 p-4 rounded-lg"
                style={{ background: "var(--color-success-bg)" }}
              >
                <CheckCircle
                  size={18}
                  color="var(--color-success)"
                  strokeWidth={2.5}
                />
                <span
                  className="text-sm font-semibold"
                  style={{
                    fontFamily: "var(--font-display)",
                    color: "var(--color-success)",
                  }}
                >
                  In Stock · {product.sizeAvailable} sizes available
                </span>
              </div>

              {/* Size selector */}
              <div className="mb-6">
                <div className="flex items-center justify-between mb-3">
                  <p
                    className="font-bold text-sm"
                    style={{
                      fontFamily: "var(--font-display)",
                      color: "var(--color-text-heading)",
                    }}
                  >
                    Size (UK)
                  </p>
                  <button
                    className="text-xs font-semibold cursor-pointer bg-transparent border-none"
                    style={{
                      fontFamily: "var(--font-display)",
                      color: "var(--color-primary)",
                    }}
                  >
                    Size Guide
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {sizes.map((s) => (
                    <button
                      key={s}
                      onClick={() => setSelectedSize(s)}
                      className="w-12 h-12 rounded-md border font-bold text-sm cursor-pointer transition-all duration-150 hover:border-primary"
                      style={{
                        fontFamily: "var(--font-display)",
                        borderColor:
                          selectedSize === s
                            ? "var(--color-primary)"
                            : "var(--color-border)",
                        background:
                          selectedSize === s
                            ? "var(--color-primary)"
                            : "var(--color-bg)",
                        color:
                          selectedSize === s
                            ? "white"
                            : "var(--color-text-body)",
                      }}
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </div>

              {/* Action buttons */}
              <div className="flex gap-3">
                <Button
                  variant="primary"
                  size="lg"
                  className="flex-1"
                  icon={<ShoppingCart size={16} />}
                >
                  Add to Cart
                </Button>
                <Button
                  variant="outline"
                  size="lg"
                  className="flex-1"
                  icon={<Navigation size={16} />}
                  onClick={handleNavigate}
                >
                  Navigate
                </Button>
              </div>
            </div>

            {/* Highlights */}
            <div className="bg-bg border border-border rounded-xl p-5 shadow-card">
              <p
                className="font-bold text-sm mb-4"
                style={{
                  fontFamily: "var(--font-display)",
                  color: "var(--color-text-heading)",
                }}
              >
                Why Choose This Product?
              </p>
              <div className="space-y-3">
                {[
                  {
                    Icon: Zap,
                    label: "Lightweight Design",
                    sub: "Ultra-light foam sole for all-day comfort",
                    color: "var(--color-icon-orange)",
                    bg: "var(--color-icon-orange-bg)",
                  },
                  {
                    Icon: Package,
                    label: "Premium Quality",
                    sub: "Made with premium materials",
                    color: "var(--color-icon-blue)",
                    bg: "var(--color-icon-blue-bg)",
                  },
                  {
                    Icon: CheckCircle,
                    label: "Certified & Tested",
                    sub: "Quality assured by experts",
                    color: "var(--color-icon-green)",
                    bg: "var(--color-icon-green-bg)",
                  },
                ].map(({ Icon, label, sub, color, bg }) => (
                  <div
                    key={label}
                    className="flex items-start gap-3 p-3 rounded-lg"
                    style={{ background: bg }}
                  >
                    <Icon
                      size={18}
                      color={color}
                      strokeWidth={2}
                      className="mt-0.5 shrink-0"
                    />
                    <div>
                      <div
                        className="text-xs font-bold"
                        style={{
                          fontFamily: "var(--font-display)",
                          color: "var(--color-text-heading)",
                        }}
                      >
                        {label}
                      </div>
                      <div
                        className="text-xs mt-0.5"
                        style={{
                          color: "var(--color-text-muted)",
                          fontFamily: "var(--font-body)",
                        }}
                      >
                        {sub}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Description */}
            <div className="bg-bg border border-border rounded-xl p-5 shadow-card">
              <p
                className="font-bold text-sm mb-3"
                style={{
                  fontFamily: "var(--font-display)",
                  color: "var(--color-text-heading)",
                }}
              >
                Description
              </p>
              <p
                className="text-sm leading-relaxed"
                style={{
                  color: "var(--color-text-muted)",
                  fontFamily: "var(--font-body)",
                }}
              >
                Experience ultimate comfort with {product.name}. Engineered with
                responsive foam technology, these shoes adapt to your movement
                while maintaining superior support. The breathable mesh upper
                keeps your feet cool and dry throughout the day, making them
                perfect for all-day wear.
              </p>
            </div>

            {/* Related products */}
            {related.length > 0 && (
              <div>
                <h2
                  className="font-extrabold text-lg mb-4"
                  style={{
                    fontFamily: "var(--font-display)",
                    color: "var(--color-text-heading)",
                  }}
                >
                  You May Also Like
                </h2>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  {related.map((p) => (
                    <div
                      key={p.id}
                      className="bg-bg border border-border rounded-xl overflow-hidden shadow-card cursor-pointer transition-all duration-200 hover:-translate-y-1 hover:shadow-lg"
                      onClick={() => navigate(`/product/${p.id}`)}
                    >
                      <div className="h-32 p-3 bg-gradient-to-br from-surface to-surface-alt flex items-center justify-center">
                        <ShoePlaceholder colorHex={p.shoeColor} />
                      </div>
                      <div className="px-3 pb-3 pt-2">
                        <p
                          className="font-bold text-sm leading-snug mb-1"
                          style={{
                            fontFamily: "var(--font-display)",
                            color: "var(--color-text-heading)",
                          }}
                        >
                          {p.name}
                        </p>
                        <p
                          className="font-extrabold text-base"
                          style={{
                            fontFamily: "var(--font-display)",
                            color: "var(--color-primary)",
                          }}
                        >
                          ₹{p.price.toLocaleString("en-IN")}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
