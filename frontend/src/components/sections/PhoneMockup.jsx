export default function PhoneMockup() {
  return (
    <div
      style={{
        width: 220,
        height: 420,
        background: "#1C1C1E",
        borderRadius: 32,
        padding: "10px",
        boxShadow:
          "0 24px 48px rgba(0,0,0,0.28), inset 0 0 0 1px rgba(255,255,255,0.08)",
        position: "relative",
        flexShrink: 0,
      }}
    >
      {/* Screen */}
      <div
        style={{
          width: "100%",
          height: "100%",
          background: "#FFFFFF",
          borderRadius: 24,
          overflow: "hidden",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {/* Status bar */}
        <div
          style={{
            background: "#F8FAFC",
            padding: "8px 14px 4px",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <span
            style={{
              fontSize: 10,
              fontWeight: 700,
              fontFamily: "var(--font-display)",
            }}
          >
            9:41
          </span>
          <div style={{ display: "flex", gap: 4, alignItems: "center" }}>
            <div
              style={{
                width: 12,
                height: 8,
                borderRadius: 2,
                background: "var(--color-text-heading)",
                opacity: 0.7,
              }}
            />
            <div
              style={{
                width: 8,
                height: 8,
                borderRadius: "50%",
                border: "1.5px solid var(--color-text-heading)",
                opacity: 0.7,
              }}
            />
          </div>
        </div>

        {/* Back bar */}
        <div
          style={{
            padding: "6px 12px",
            background: "#F8FAFC",
            display: "flex",
            alignItems: "center",
            gap: 8,
            borderBottom: "1px solid #E2E8F0",
          }}
        >
          <span style={{ fontSize: 14 }}>←</span>
          <div
            style={{
              flex: 1,
              height: 6,
              background: "#E2E8F0",
              borderRadius: 3,
            }}
          />
          <span style={{ fontSize: 14 }}>↺</span>
        </div>

        {/* Indoor map area */}
        <div
          style={{
            flex: 1,
            position: "relative",
            background: "#F0F4F8",
            overflow: "hidden",
          }}
        >
          {/* Grid lines simulating store layout */}
          <svg
            width="100%"
            height="100%"
            style={{ position: "absolute", inset: 0 }}
          >
            {/* Aisles */}
            <rect x="10" y="10" width="82" height="14" rx="2" fill="#E2E8F0" />
            <rect x="10" y="30" width="82" height="14" rx="2" fill="#E2E8F0" />
            <rect x="10" y="50" width="38" height="14" rx="2" fill="#E2E8F0" />
            <rect x="54" y="50" width="38" height="14" rx="2" fill="#E2E8F0" />
            <rect x="10" y="70" width="82" height="14" rx="2" fill="#E2E8F0" />
            <rect x="10" y="90" width="38" height="14" rx="2" fill="#E2E8F0" />
            <rect x="54" y="90" width="38" height="14" rx="2" fill="#E2E8F0" />
            <rect x="10" y="110" width="82" height="14" rx="2" fill="#E2E8F0" />

            {/* Path from entry to product */}
            <path
              d="M 50 200 L 50 140 L 50 110 L 70 110 L 70 80"
              stroke="var(--color-primary)"
              strokeWidth="2.5"
              fill="none"
              strokeDasharray="5,3"
              strokeLinecap="round"
            />

            {/* Entry point (green dot) */}
            <circle cx="50" cy="200" r="5" fill="#16A34A" />

            {/* Destination pin */}
            <circle cx="70" cy="74" r="10" fill="var(--color-primary)" />
            <circle cx="70" cy="74" r="5" fill="white" />
          </svg>

          {/* Location labels */}
          <div
            style={{
              position: "absolute",
              left: 10,
              top: 12,
              fontSize: 7,
              color: "#64748B",
              fontFamily: "var(--font-display)",
              fontWeight: 600,
            }}
          >
            Aisle 1
          </div>
          <div
            style={{
              position: "absolute",
              left: 10,
              top: 32,
              fontSize: 7,
              color: "#64748B",
              fontFamily: "var(--font-display)",
              fontWeight: 600,
            }}
          >
            Aisle 2
          </div>
          <div
            style={{
              position: "absolute",
              left: 10,
              top: 52,
              fontSize: 7,
              color: "#64748B",
              fontFamily: "var(--font-display)",
              fontWeight: 600,
            }}
          >
            Aisle 3
          </div>
        </div>

        {/* Product card at bottom of screen */}
        <div
          style={{
            padding: "10px 12px",
            borderTop: "1px solid #E2E8F0",
            display: "flex",
            gap: 8,
            alignItems: "center",
          }}
        >
          {/* Product thumb */}
          <div
            style={{
              width: 40,
              height: 40,
              borderRadius: 8,
              background: "linear-gradient(135deg, #F8FAFC, #E2E8F0)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              flexShrink: 0,
            }}
          >
            <span style={{ fontSize: 18 }}>🥤</span>
          </div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div
              style={{
                fontFamily: "var(--font-display)",
                fontWeight: 700,
                fontSize: 9,
                color: "var(--color-text-heading)",
                lineHeight: 1.2,
              }}
            >
              Boost Bottle
            </div>
            <div
              style={{
                fontSize: 8,
                color: "var(--color-text-muted)",
                marginTop: 1,
              }}
            >
              500ml
            </div>
            <div
              style={{
                fontSize: 8,
                color: "var(--color-primary)",
                marginTop: 2,
                fontWeight: 600,
              }}
            >
              Aisle 3 · Rack 6 · Shelf 2
            </div>
          </div>
        </div>
      </div>

      {/* Home indicator */}
      <div
        style={{
          position: "absolute",
          bottom: 4,
          left: "50%",
          transform: "translateX(-50%)",
          width: 60,
          height: 4,
          background: "rgba(255,255,255,0.25)",
          borderRadius: 2,
        }}
      />
    </div>
  );
}
