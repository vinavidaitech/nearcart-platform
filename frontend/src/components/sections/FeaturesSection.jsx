// components/sections/FeaturesSection.jsx
// UPDATED FOR TAILWIND V4

import { Search, Navigation, Package, Clock } from "lucide-react";

const features = [
  {
    Icon: Search,
    iconColor: "var(--color-icon-blue)",
    iconBg: "var(--color-icon-blue-bg)",
    title: "Smart Product Search",
    desc: "Search products instantly across nearby stores.",
  },
  {
    Icon: Navigation,
    iconColor: "var(--color-icon-green)",
    iconBg: "var(--color-icon-green-bg)",
    title: "Indoor Navigation",
    desc: "Find the exact aisle, rack, and shelf location.",
  },
  {
    Icon: Package,
    iconColor: "var(--color-icon-purple)",
    iconBg: "var(--color-icon-purple-bg)",
    title: "Real-Time Inventory",
    desc: "Know product availability before visiting.",
  },
  {
    Icon: Clock,
    iconColor: "var(--color-icon-orange)",
    iconBg: "var(--color-icon-orange-bg)",
    title: "Faster Shopping",
    desc: "Save time with guided store navigation.",
  },
];

export default function FeaturesSection() {
  return (
    <section className="py-[72px] bg-bg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2
          className="font-extrabold text-[1.75rem] text-center mb-10"
          style={{
            fontFamily: "var(--font-display)",
            color: "var(--color-text-heading)",
          }}
        >
          Everything You Need for Smart Shopping
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {features.map((f) => (
            <div
              key={f.title}
              className="bg-bg border border-border rounded-lg p-7 shadow-card transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md cursor-default"
            >
              <div
                className="w-12 h-12 rounded-md flex items-center justify-center mb-4"
                style={{ background: f.iconBg }}
              >
                <f.Icon size={22} color={f.iconColor} strokeWidth={2} />
              </div>

              <h3
                className="font-bold text-[0.9375rem] mb-2"
                style={{
                  fontFamily: "var(--font-display)",
                  color: "var(--color-text-heading)",
                }}
              >
                {f.title}
              </h3>

              <p
                className="text-sm leading-[1.55]"
                style={{
                  color: "var(--color-text-muted)",
                  fontFamily: "var(--font-body)",
                }}
              >
                {f.desc}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
