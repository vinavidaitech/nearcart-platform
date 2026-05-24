// components/ui/Badge.jsx
const variantMap = {
  blue: "bg-[var(--badge-blue-bg)] text-[var(--badge-blue-text)]",
  green: "bg-[var(--badge-green-bg)] text-[var(--badge-green-text)]",
  orange: "bg-[var(--badge-orange-bg)] text-[var(--badge-orange-text)]",
  gray: "bg-[var(--badge-gray-bg)] text-[var(--badge-gray-text)]",
  "best-price": "bg-[var(--badge-blue-bg)] text-[var(--badge-blue-text)]",
  "nearest-store": "bg-[var(--badge-green-bg)] text-[var(--badge-green-text)]",
  "top-rated": "bg-[var(--badge-orange-bg)] text-[var(--badge-orange-text)]",
};

export default function Badge({ variant = "blue", className = "", children }) {
  const cls = [
    "inline-flex items-center gap-1 px-2 py-0.5",
    "text-xs font-semibold rounded",
    variantMap[variant] ?? variantMap.blue,
    className,
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <span className={cls} style={{ fontFamily: "var(--font-display)" }}>
      {children}
    </span>
  );
}
