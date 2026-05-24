// components/sections/StatsSection.jsx
// UPDATED FOR TAILWIND V4

import { Home, ShoppingBag, Users, Zap } from "lucide-react";

const stats = [
  {
    value: "500+",
    label: "Stores",
    Icon: Home,
    iconColor: "var(--color-icon-blue)",
    iconBg: "var(--color-icon-blue-bg)",
  },
  {
    value: "50K+",
    label: "Products",
    Icon: ShoppingBag,
    iconColor: "var(--color-icon-green)",
    iconBg: "var(--color-icon-green-bg)",
  },
  {
    value: "10K+",
    label: "Users",
    Icon: Users,
    iconColor: "var(--color-icon-purple)",
    iconBg: "var(--color-icon-purple-bg)",
  },
  {
    value: "99%",
    label: "Faster Product Discovery",
    Icon: Zap,
    iconColor: "var(--color-icon-orange)",
    iconBg: "var(--color-icon-orange-bg)",
  },
];

export default function StatsSection() {
  return (
    <section className="pb-[72px] bg-bg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {stats.map((s) => (
            <div
              key={s.label}
              className="bg-bg border border-border rounded-lg px-6 py-5 flex items-center gap-4 shadow-card"
            >
              <div
                className="w-12 h-12 rounded-md flex items-center justify-center shrink-0"
                style={{ background: s.iconBg }}
              >
                <s.Icon size={20} color={s.iconColor} strokeWidth={2} />
              </div>

              <div>
                <div
                  className="font-extrabold text-[1.625rem] leading-none"
                  style={{
                    fontFamily: "var(--font-display)",
                    color: "var(--color-text-heading)",
                  }}
                >
                  {s.value}
                </div>

                <div
                  className="text-[0.8125rem] mt-1"
                  style={{
                    color: "var(--color-text-muted)",
                    fontFamily: "var(--font-body)",
                  }}
                >
                  {s.label}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
