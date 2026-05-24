// components/sections/StoreOwnerSection.jsx
// UPDATED FOR TAILWIND V4

import Button from "@/components/ui/Button";
import { Store } from "lucide-react";

export default function StoreOwnerSection() {
  return (
    <section className="py-[72px] bg-bg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div
          className="rounded-2xl border border-primary-border overflow-hidden flex flex-col md:flex-row items-center gap-10 p-8 md:p-12 relative min-h-[240px]"
          style={{
            background: "linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%)",
          }}
        >
          {/* Left content */}
          <div className="flex-1">
            <h2
              className="font-extrabold text-[1.75rem] mb-3"
              style={{
                fontFamily: "var(--font-display)",
                color: "var(--color-text-heading)",
              }}
            >
              Own a Store?
            </h2>

            <p
              className="text-base leading-relaxed max-w-[380px] mb-7"
              style={{
                color: "var(--color-text-muted)",
                fontFamily: "var(--font-body)",
              }}
            >
              Manage inventory, track shelves, and improve customer shopping
              experience with our smart management platform.
            </p>

            <Button variant="primary" size="md" icon={<Store size={15} />}>
              Register Your Store
            </Button>
          </div>

          {/* Right: Dashboard illustration */}
          <div className="hidden md:flex items-center justify-center shrink-0">
            {/* Laptop frame */}
            <div className="flex flex-col">
              <div
                className="w-[280px] rounded-t-xl p-2.5"
                style={{
                  background: "#1C1C2E",
                  boxShadow: "0 16px 40px rgba(0,0,0,0.18)",
                }}
              >
                {/* Screen */}
                <div
                  className="rounded-md p-3"
                  style={{ background: "#0F172A", minHeight: 160 }}
                >
                  {/* Dashboard top bar */}
                  <div className="flex gap-2 mb-2.5">
                    {["#1D6BE5", "#16A34A", "#7C3AED"].map((c, idx) => (
                      <div
                        key={c}
                        className="flex-1 rounded-md p-2"
                        style={{ background: c }}
                      >
                        <div
                          className="h-1.5 rounded mb-1"
                          style={{ background: "rgba(255,255,255,0.3)" }}
                        />
                        <div
                          className="h-2.5 rounded w-[60%]"
                          style={{ background: "rgba(255,255,255,0.9)" }}
                        />
                      </div>
                    ))}
                  </div>

                  {/* Bar chart */}
                  <div className="flex items-end gap-1 h-[70px] mt-2 pb-1">
                    {[40, 60, 35, 75, 55, 80, 65].map((h, i) => (
                      <div
                        key={i}
                        className="flex-1 rounded-t"
                        style={{
                          background: `rgba(29,107,229,${0.4 + (i % 3) * 0.2})`,
                          height: `${h}%`,
                        }}
                      />
                    ))}
                  </div>

                  {/* Table rows */}
                  {[...Array(3)].map((_, i) => (
                    <div key={i} className="flex gap-1.5 mt-1.5">
                      <div
                        className="w-3.5 h-1.5 rounded"
                        style={{ background: "rgba(255,255,255,0.12)" }}
                      />
                      <div
                        className="flex-1 h-1.5 rounded"
                        style={{ background: "rgba(255,255,255,0.06)" }}
                      />
                      <div
                        className="w-6 h-1.5 rounded"
                        style={{ background: "rgba(29,107,229,0.5)" }}
                      />
                    </div>
                  ))}
                </div>
              </div>

              {/* Laptop base */}
              <div
                className="w-[300px] h-2 self-center rounded-b"
                style={{ background: "#2D2D44" }}
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
