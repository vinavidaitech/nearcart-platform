// components/sections/HeroSection.jsx
// UPDATED FOR TAILWIND V4

import { Search, ArrowRight } from "lucide-react";
import PhoneMockup from "@/components/sections/PhoneMockup";
import Button from "@/components/ui/Button";

export default function HeroSection() {
  return (
    <section
      className="relative overflow-hidden min-h-[480px]"
      style={{
        background:
          "linear-gradient(110deg, #FFFFFF 0%, #FFFFFF 52%, #EFF6FF 52%, #DBEAFE 100%)",
      }}
    >
      {/* Decorative blur circles */}
      <div
        className="absolute rounded-full pointer-events-none"
        style={{
          top: -80,
          right: "30%",
          width: 300,
          height: 300,
          background: "rgba(29,107,229,0.06)",
          filter: "blur(60px)",
        }}
      />
      <div
        className="absolute rounded-full pointer-events-none"
        style={{
          bottom: -60,
          right: "10%",
          width: 240,
          height: 240,
          background: "rgba(29,107,229,0.08)",
          filter: "blur(50px)",
        }}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center gap-10 lg:gap-12 py-16">
        {/* Left: Text & Search */}
        <div className="flex-1 min-w-0">
          <h1
            className="font-black leading-tight tracking-tight max-w-[460px]"
            style={{
              fontFamily: "var(--font-display)",
              fontSize: "clamp(1.875rem, 4vw, 2.75rem)",
              color: "var(--color-text-heading)",
              letterSpacing: "-0.02em",
            }}
          >
            Find Products Inside Stores Instantly
          </h1>
          <p
            className="mt-4 leading-relaxed max-w-[420px]"
            style={{
              fontSize: "1.0625rem",
              color: "var(--color-text-muted)",
              fontFamily: "var(--font-body)",
            }}
          >
            Discover products faster with smart indoor store navigation and
            real-time inventory visibility.
          </p>

          {/* Search bar */}
          <div className="mt-7 flex items-center bg-white border border-border rounded-md shadow-sm overflow-hidden max-w-[440px]">
            <input
              type="text"
              placeholder="Search product, brands or stores"
              className="flex-1 border-none outline-none px-4 py-3 text-[0.9375rem] bg-transparent"
              style={{
                fontFamily: "var(--font-body)",
                color: "var(--color-text-body)",
              }}
            />
            <button
              className="p-[10px] flex items-center justify-center transition-colors duration-150 cursor-pointer hover:opacity-90"
              style={{ background: "var(--color-primary)" }}
            >
              <Search size={18} color="white" strokeWidth={2.5} />
            </button>
          </div>

          {/* CTA Buttons */}
          <div className="mt-5 flex flex-wrap items-center gap-2.5">
            <Button
              variant="primary"
              size="md"
              icon={<ArrowRight size={15} />}
              iconPosition="right"
            >
              Get Started
            </Button>
            <Button variant="outline" size="md">
              Explore Stores
            </Button>
            <button
              className="bg-transparent border-none cursor-pointer px-1 py-2.5 text-[0.9375rem] font-semibold transition-opacity duration-150 hover:opacity-70"
              style={{
                color: "var(--color-primary)",
                fontFamily: "var(--font-display)",
              }}
            >
              Continue as Guest
            </button>
          </div>
        </div>

        {/* Right: Phone mockup */}
        <div className="hidden md:flex items-center justify-center shrink-0">
          <PhoneMockup />
        </div>
      </div>
    </section>
  );
}
