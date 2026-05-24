export default function ShoePlaceholder({ colorHex }) {
  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: `linear-gradient(135deg, #F1F5F9 0%, #E2E8F0 100%)`,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        borderRadius: "var(--radius-md)",
      }}
    >
      {/* Stylised sneaker SVG */}
      <svg
        width="80"
        height="52"
        viewBox="0 0 100 60"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <ellipse cx="50" cy="52" rx="44" ry="6" fill="#CBD5E1" opacity="0.6" />
        <path
          d="M8 44 C8 44 12 20 30 18 C40 17 52 22 62 20 C72 18 80 14 88 16 C94 17 92 28 88 32 C84 36 76 40 60 42 C44 44 28 46 20 46 C12 46 8 44 8 44 Z"
          fill={colorHex || "#334155"}
        />
        <path
          d="M28 42 C28 42 30 26 42 24 C50 22 58 26 66 24"
          stroke="white"
          strokeWidth="1.5"
          strokeLinecap="round"
          opacity="0.4"
        />
        <path d="M8 44 L88 32" stroke="white" strokeWidth="1.5" opacity="0.2" />
        <ellipse cx="16" cy="44" rx="7" ry="4" fill="#94A3B8" opacity="0.8" />
        <ellipse cx="82" cy="33" rx="7" ry="4" fill="#94A3B8" opacity="0.8" />
        {/* Swoosh-style mark */}
        <path
          d="M40 30 C44 26 54 22 64 24 C68 25 64 28 58 30 C52 32 44 33 40 30 Z"
          fill="white"
          opacity="0.25"
        />
      </svg>
    </div>
  );
}
