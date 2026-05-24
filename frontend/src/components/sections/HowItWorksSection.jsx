// components/sections/HowItWorksSection.jsx
// UPDATED FOR TAILWIND V4

import { Layers, MapPin, Globe } from "lucide-react";

const steps = [
  {
    Icon: Layers,
    iconColor: "var(--color-icon-blue)",
    iconBg: "var(--color-icon-blue-bg)",
    borderColor: "var(--color-icon-blue)",
    title: "Search Your Product",
    desc: "Type or scan the product you need.",
  },
  {
    Icon: MapPin,
    iconColor: "var(--color-icon-orange)",
    iconBg: "var(--color-icon-orange-bg)",
    borderColor: "var(--color-icon-orange)",
    title: "Locate the Product",
    desc: "View store location, aisle, and shelf details instantly.",
  },
  {
    Icon: Globe,
    iconColor: "var(--color-icon-purple)",
    iconBg: "var(--color-icon-purple-bg)",
    borderColor: "var(--color-icon-purple)",
    title: "Navigate & Purchase",
    desc: "Follow the store map and buy quickly.",
  },
];

export default function HowItWorksSection() {
  return (
    <section className="py-[72px] bg-surface">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2
          className="font-extrabold text-[1.75rem] text-center mb-14"
          style={{
            fontFamily: "var(--font-display)",
            color: "var(--color-text-heading)",
          }}
        >
          How It Works
        </h2>

        <div className="flex flex-col sm:flex-row items-start justify-center gap-0">
          {steps.map((step, i) => (
            <div key={step.title} className="flex items-center flex-1">
              {/* Step card */}
              <div className="text-center flex-1 px-3">
                <div
                  className="w-[72px] h-[72px] rounded-full flex items-center justify-center mx-auto mb-4 border-2"
                  style={{
                    background: step.iconBg,
                    borderColor: step.borderColor,
                  }}
                >
                  <step.Icon size={26} color={step.iconColor} strokeWidth={2} />
                </div>

                <h3
                  className="font-bold text-[0.9375rem] mb-2"
                  style={{
                    fontFamily: "var(--font-display)",
                    color: "var(--color-text-heading)",
                  }}
                >
                  {step.title}
                </h3>

                <p
                  className="text-sm leading-[1.55] max-w-[200px] mx-auto"
                  style={{
                    color: "var(--color-text-muted)",
                    fontFamily: "var(--font-body)",
                  }}
                >
                  {step.desc}
                </p>
              </div>

              {/* Connector line */}
              {i < steps.length - 1 && (
                <div className="w-20 shrink-0 relative -top-7 hidden sm:block">
                  <svg width="80" height="24" viewBox="0 0 80 24" fill="none">
                    <path
                      d="M2 12 Q20 2 40 12 Q60 22 78 12"
                      stroke="var(--color-border)"
                      strokeWidth="2"
                      strokeDasharray="5,4"
                      fill="none"
                      strokeLinecap="round"
                    />
                  </svg>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
