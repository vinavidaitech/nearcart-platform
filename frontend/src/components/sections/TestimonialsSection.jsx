// components/sections/TestimonialsSection.jsx
// UPDATED FOR TAILWIND V4

import { User } from "lucide-react";

const testimonials = [
  {
    name: "Ramesh Kumar",
    text: "I found products inside supermarkets within seconds. Super useful!",
  },
  {
    name: "Vanitha Sharma",
    text: "Indoor navigation saved a lot of shopping time.",
  },
];

export default function TestimonialsSection() {
  return (
    <section className="py-[72px] bg-surface">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2
          className="font-extrabold text-[1.75rem] text-center mb-10"
          style={{
            fontFamily: "var(--font-display)",
            color: "var(--color-text-heading)",
          }}
        >
          What Users Say
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 max-w-[800px] mx-auto">
          {testimonials.map((t) => (
            <div
              key={t.name}
              className="bg-bg border border-border rounded-xl p-6 flex gap-4 shadow-card"
            >
              {/* Avatar */}
              <div
                className="w-[52px] h-[52px] rounded-full flex items-center justify-center shrink-0 border-2 border-primary-border"
                style={{
                  background: "linear-gradient(135deg, #DBEAFE, #EFF6FF)",
                }}
              >
                <User
                  size={24}
                  color="var(--color-icon-blue)"
                  strokeWidth={2}
                />
              </div>

              <div>
                <p
                  className="text-[0.9375rem] leading-[1.55] mb-2.5"
                  style={{
                    color: "var(--color-text-body)",
                    fontFamily: "var(--font-body)",
                  }}
                >
                  "{t.text}"
                </p>

                <span
                  className="font-bold text-sm"
                  style={{
                    fontFamily: "var(--font-display)",
                    color: "var(--color-primary)",
                  }}
                >
                  {t.name}
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* Pagination dots */}
        <div className="flex justify-center gap-2 mt-8">
          {[0, 1, 2, 3].map((i) => (
            <div
              key={i}
              className="h-2 rounded-full transition-all duration-200"
              style={{
                width: i === 1 ? 20 : 8,
                background:
                  i === 1 ? "var(--color-primary)" : "var(--color-border)",
              }}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
