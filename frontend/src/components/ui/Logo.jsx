// components/ui/Logo.jsx
export default function Logo({ className = "" }) {
  return (
    <div
      className={`inline-flex flex-col leading-none select-none ${className}`}
    >
      <span
        className="text-xl font-black tracking-tight"
        style={{
          fontFamily: "var(--font-display)",
          color: "var(--color-text-heading)",
        }}
      >
        NearCart
      </span>
      {/* Barcode-style accent bar */}
      <span
        className="block h-[5px] mt-0.5 rounded-sm"
        style={{
          background: `repeating-linear-gradient(
            90deg,
            var(--color-text-heading) 0px, var(--color-text-heading) 2px,
            transparent 2px, transparent 4px,
            var(--color-text-heading) 4px, var(--color-text-heading) 5px,
            transparent 5px, transparent 7px,
            var(--color-text-heading) 7px, var(--color-text-heading) 9px,
            transparent 9px, transparent 11px,
            var(--color-text-heading) 11px, var(--color-text-heading) 12px,
            transparent 12px, transparent 14px,
            var(--color-text-heading) 14px, var(--color-text-heading) 15px,
            transparent 15px, transparent 17px
          )`,
        }}
      />
      <span
        className="text-[0.6rem] font-medium uppercase tracking-widest mt-0.5"
        style={{
          fontFamily: "var(--font-display)",
          color: "var(--color-text-muted)",
        }}
      >
        Find it Faster
      </span>
    </div>
  );
}
