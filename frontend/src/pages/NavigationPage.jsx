// components/pages/NavigationPage.jsx
// NAVIGATION PAGE WITH MAP AND DIRECTIONS

import { useState, useEffect } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import {
  ArrowLeft,
  MapPin,
  Navigation,
  Map,
  Share2,
  Phone,
  Clock,
  Footprints,
} from "lucide-react";
import Button from "@/components/ui/Button";
import { products } from "@/constants/data";

// Sample store locations with navigation steps
const STORE_LOCATIONS = {
  1: {
    name: "Shoe Spot",
    coords: { lat: 9.9252, lng: 78.1198 },
    address: "Church Road, 2nd Floor, Madurai",
    distance: "3.5 km",
    walkingTime: "~45 mins",
    phone: "+91 9876543210",
    hours: "9 AM - 10 PM",
    steps: [
      {
        step: 1,
        title: "Start",
        description: "Begin from your current location",
        distance: "0m",
        duration: "0 mins",
      },
      {
        step: 2,
        title: "Go Straight",
        description: "Walk along the main corridor",
        distance: "200m",
        duration: "3 mins",
      },
      {
        step: 3,
        title: "Turn Left",
        description: "Take left at the food section",
        distance: "150m",
        duration: "2 mins",
      },
      {
        step: 4,
        title: "Aisle 5",
        description: "Product is located on right shelf",
        distance: "100m",
        duration: "1 mins",
      },
      {
        step: 5,
        title: "Destination",
        description: "You have reached the product location",
        distance: "Aisle 5 · Rack 6 · Shelf 2",
        duration: "Arrived",
      },
    ],
    totalDistance: "500 meters",
    totalTime: "~20 mins",
  },
};

// Calculate simple distance between two coordinates
const calculateDistance = (lat1, lon1, lat2, lon2) => {
  const R = 6371; // Radius of the Earth in km
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLon = ((lon2 - lon1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return (R * c * 1000).toFixed(0); // Return in meters
};

export default function NavigationPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const locationState = useLocation().state || {};

  const product =
    products.find((p) => String(p.id) === String(id)) || products[0];
  const storeInfo = STORE_LOCATIONS[product.id] || STORE_LOCATIONS[1];

  // User location (Madurai center as default)
  const userLocation = locationState.userLocation || {
    lat: 9.9252,
    lng: 78.1198,
  };

  const [activeStep, setActiveStep] = useState(0);
  const [navigating, setNavigating] = useState(true);

  // Simple map rendering with markers
  const MapVisualization = () => {
    const userLat = userLocation.lat;
    const userLng = userLocation.lng;
    const storeLat = storeInfo.coords.lat;
    const storeLng = storeInfo.coords.lng;

    return (
      <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl overflow-hidden relative w-full h-full flex items-center justify-center">
        {/* Simplified Map Background */}
        <div className="absolute inset-0 opacity-30">
          <svg
            className="w-full h-full"
            viewBox="0 0 400 300"
            preserveAspectRatio="xMidYMid slice"
          >
            {/* Streets */}
            <rect
              x="50"
              y="80"
              width="300"
              height="2"
              fill="#64748b"
              opacity="0.5"
            />
            <rect
              x="50"
              y="120"
              width="300"
              height="2"
              fill="#64748b"
              opacity="0.5"
            />
            <rect
              x="50"
              y="160"
              width="300"
              height="2"
              fill="#64748b"
              opacity="0.5"
            />
            <rect
              x="150"
              y="40"
              width="2"
              height="200"
              fill="#64748b"
              opacity="0.5"
            />
            <rect
              x="220"
              y="40"
              width="2"
              height="200"
              fill="#64748b"
              opacity="0.5"
            />

            {/* Building blocks */}
            <rect
              x="60"
              y="50"
              width="60"
              height="25"
              fill="#cbd5e1"
              opacity="0.4"
            />
            <rect
              x="260"
              y="100"
              width="70"
              height="30"
              fill="#cbd5e1"
              opacity="0.4"
            />
            <rect
              x="80"
              y="180"
              width="80"
              height="40"
              fill="#cbd5e1"
              opacity="0.4"
            />
          </svg>
        </div>

        {/* User Location (Green) */}
        <div
          className="absolute w-5 h-5 rounded-full border-4 border-green-500 bg-green-400 flex items-center justify-center animate-pulse"
          style={{
            left: "35%",
            top: "50%",
            transform: "translate(-50%, -50%)",
          }}
        >
          <div className="w-2 h-2 bg-white rounded-full" />
        </div>

        {/* Route Line */}
        <svg
          className="absolute inset-0 w-full h-full pointer-events-none"
          style={{ width: "100%", height: "100%" }}
        >
          <line
            x1="140"
            y1="150"
            x2="220"
            y2="120"
            stroke="#1d6be5"
            strokeWidth="3"
            strokeDasharray="5,5"
            strokeLinecap="round"
          />
        </svg>

        {/* Store Location (Red) */}
        <div
          className="absolute w-6 h-6 bg-red-500 rounded-full flex items-center justify-center border-4 border-red-300 shadow-lg"
          style={{
            left: "55%",
            top: "40%",
            transform: "translate(-50%, -50%)",
          }}
        >
          <MapPin size={14} color="white" strokeWidth={2} />
        </div>

        {/* Map Controls */}
        <div className="absolute bottom-4 right-4 flex flex-col gap-2 z-10">
          <button className="w-10 h-10 rounded-lg bg-white border border-border shadow-sm hover:shadow-md transition-shadow">
            <span className="text-lg">+</span>
          </button>
          <button className="w-10 h-10 rounded-lg bg-white border border-border shadow-sm hover:shadow-md transition-shadow">
            <span className="text-lg">−</span>
          </button>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-surface">
      {/* Header */}
      <header className="bg-bg border-b border-border sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <button
            onClick={() => navigate(-1)}
            className="flex items-center gap-2 font-semibold cursor-pointer bg-transparent border-none p-0 hover:text-primary transition-colors duration-150"
            style={{
              color: "var(--color-text-muted)",
              fontFamily: "var(--font-display)",
            }}
          >
            <ArrowLeft size={16} strokeWidth={2.5} />
            Back
          </button>
          <h1
            className="text-lg font-bold"
            style={{
              fontFamily: "var(--font-display)",
              color: "var(--color-text-heading)",
            }}
          >
            Navigate to {product.name}
          </h1>
          <button className="w-9 h-9 rounded-full bg-surface border border-border flex items-center justify-center hover:bg-primary-light transition-colors duration-150">
            <Share2 size={16} color="var(--color-text-muted)" strokeWidth={2} />
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 pb-16">
        <div className="grid grid-cols-1 lg:grid-cols-[1.5fr_420px] gap-6">
          {/* ── LEFT: Map ── */}
          <div className="bg-bg border border-border rounded-2xl overflow-hidden shadow-card h-[500px]">
            <MapVisualization />
          </div>

          {/* ── RIGHT: Navigation Steps ── */}
          <div className="flex flex-col gap-4">
            {/* Store Info Card */}
            <div className="bg-bg border border-border rounded-xl p-4 shadow-card">
              <div className="flex items-start gap-3 mb-3">
                <div
                  className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0"
                  style={{ background: "var(--color-icon-blue-bg)" }}
                >
                  <MapPin
                    size={18}
                    color="var(--color-icon-blue)"
                    strokeWidth={2}
                  />
                </div>
                <div className="flex-1 min-w-0">
                  <p
                    className="font-bold text-sm"
                    style={{
                      fontFamily: "var(--font-display)",
                      color: "var(--color-text-heading)",
                    }}
                  >
                    {storeInfo.name}
                  </p>
                  <p
                    className="text-xs mt-1"
                    style={{
                      color: "var(--color-text-muted)",
                      fontFamily: "var(--font-body)",
                    }}
                  >
                    {storeInfo.address}
                  </p>
                </div>
              </div>

              <div className="space-y-2 mb-4 pb-4 border-b border-border">
                <div className="flex items-center gap-2">
                  <Footprints
                    size={14}
                    color="var(--color-text-muted)"
                    strokeWidth={2}
                  />
                  <span
                    className="text-xs"
                    style={{
                      color: "var(--color-text-muted)",
                      fontFamily: "var(--font-body)",
                    }}
                  >
                    {storeInfo.totalDistance} · {storeInfo.totalTime}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <Clock
                    size={14}
                    color="var(--color-text-muted)"
                    strokeWidth={2}
                  />
                  <span
                    className="text-xs"
                    style={{
                      color: "var(--color-text-muted)",
                      fontFamily: "var(--font-body)",
                    }}
                  >
                    {storeInfo.hours}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <Phone
                    size={14}
                    color="var(--color-text-muted)"
                    strokeWidth={2}
                  />
                  <a
                    href={`tel:${storeInfo.phone}`}
                    className="text-xs hover:text-primary transition-colors duration-150"
                    style={{
                      color: "var(--color-primary)",
                      fontFamily: "var(--font-body)",
                    }}
                  >
                    {storeInfo.phone}
                  </a>
                </div>
              </div>

              <Button
                variant="primary"
                size="sm"
                className="w-full"
                icon={<Phone size={14} />}
              >
                Call Store
              </Button>
            </div>

            {/* Navigation Steps */}
            <div className="bg-bg border border-border rounded-xl p-4 shadow-card flex-1 overflow-y-auto">
              <p
                className="font-bold text-sm mb-3"
                style={{
                  fontFamily: "var(--font-display)",
                  color: "var(--color-text-heading)",
                }}
              >
                Navigation Steps
              </p>

              <div className="space-y-3">
                {storeInfo.steps.map((navStep, idx) => (
                  <div
                    key={navStep.step}
                    onClick={() => setActiveStep(idx)}
                    className="p-3 rounded-lg border border-border cursor-pointer transition-all duration-150 hover:border-primary"
                    style={{
                      background:
                        activeStep === idx
                          ? "var(--color-primary-light)"
                          : "var(--color-bg)",
                      borderColor:
                        activeStep === idx
                          ? "var(--color-primary)"
                          : "var(--color-border)",
                    }}
                  >
                    <div className="flex items-start gap-3">
                      <div
                        className="w-8 h-8 rounded-full flex items-center justify-center shrink-0 font-bold text-sm"
                        style={{
                          background:
                            activeStep === idx
                              ? "var(--color-primary)"
                              : "var(--color-surface)",
                          color:
                            activeStep === idx
                              ? "white"
                              : "var(--color-text-muted)",
                          fontFamily: "var(--font-display)",
                        }}
                      >
                        {navStep.step}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p
                          className="text-xs font-bold"
                          style={{
                            fontFamily: "var(--font-display)",
                            color:
                              activeStep === idx
                                ? "var(--color-primary)"
                                : "var(--color-text-heading)",
                          }}
                        >
                          {navStep.title}
                        </p>
                        <p
                          className="text-xs mt-0.5"
                          style={{
                            color: "var(--color-text-muted)",
                            fontFamily: "var(--font-body)",
                          }}
                        >
                          {navStep.description}
                        </p>
                        <div className="flex items-center gap-2 mt-1 text-xs">
                          {navStep.distance && (
                            <span style={{ color: "var(--color-primary)" }}>
                              {navStep.distance}
                            </span>
                          )}
                          {navStep.duration && (
                            <span style={{ color: "var(--color-text-muted)" }}>
                              · {navStep.duration}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Action Button */}
            <Button
              variant="primary"
              size="lg"
              className="w-full"
              icon={<Navigation size={16} />}
              onClick={() => setNavigating(!navigating)}
            >
              {navigating ? "Stop Navigation" : "Start Navigation"}
            </Button>
          </div>
        </div>
      </main>
    </div>
  );
}
