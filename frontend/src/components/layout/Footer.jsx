// components/layout/Footer.jsx
// UPDATED FOR TAILWIND V4

import {
  FaFacebookF,
  FaInstagram,
  FaXTwitter,
  FaLinkedinIn,
} from "react-icons/fa6";
import Logo from "@/components/ui/Logo";

const quickLinks = [
  "About",
  "Contact",
  "Privacy Policy",
  "Terms & Conditions",
  "Help Center",
];
const storeLinks = ["Register Store", "Store Login", "Features", "Pricing"];

const socials = [
  { label: "Facebook", Icon: FaFacebookF },
  { label: "Instagram", Icon: FaInstagram },
  { label: "X (Twitter)", Icon: FaXTwitter },
  { label: "LinkedIn", Icon: FaLinkedinIn },
];

function SocialIcon({ label, Icon }) {
  return (
    <a
      href="#"
      aria-label={label}
      className="w-9 h-9 rounded-md bg-surface border border-border flex items-center justify-center text-text-muted transition-colors duration-150 hover:bg-primary-light hover:text-primary"
    >
      <Icon size={15} />
    </a>
  );
}

export default function Footer() {
  return (
    <footer className="border-t border-border bg-bg pt-12 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-10">
          {/* Brand */}
          <div>
            <Logo />
            <p
              className="mt-3 text-sm leading-relaxed max-w-[220px]"
              style={{
                color: "var(--color-text-muted)",
                fontFamily: "var(--font-body)",
              }}
            >
              Smart shopping begins with smart navigation. Find products easily
              inside any store.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4
              className="font-bold text-[0.9375rem] mb-4"
              style={{
                fontFamily: "var(--font-display)",
                color: "var(--color-text-heading)",
              }}
            >
              Quick Links
            </h4>
            <ul className="flex flex-col gap-2.5">
              {quickLinks.map((link) => (
                <li key={link}>
                  <a
                    href="#"
                    className="text-sm transition-colors duration-150 hover:text-primary no-underline"
                    style={{
                      color: "var(--color-text-muted)",
                      fontFamily: "var(--font-body)",
                    }}
                  >
                    {link}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* For Stores */}
          <div>
            <h4
              className="font-bold text-[0.9375rem] mb-4"
              style={{
                fontFamily: "var(--font-display)",
                color: "var(--color-text-heading)",
              }}
            >
              For Stores
            </h4>
            <ul className="flex flex-col gap-2.5">
              {storeLinks.map((link) => (
                <li key={link}>
                  <a
                    href="#"
                    className="text-sm transition-colors duration-150 hover:text-primary no-underline"
                    style={{
                      color: "var(--color-text-muted)",
                      fontFamily: "var(--font-body)",
                    }}
                  >
                    {link}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Follow Us */}
          <div>
            <h4
              className="font-bold text-[0.9375rem] mb-4"
              style={{
                fontFamily: "var(--font-display)",
                color: "var(--color-text-heading)",
              }}
            >
              Follow Us
            </h4>
            <div className="flex gap-2 flex-wrap">
              {socials.map((s) => (
                <SocialIcon key={s.label} label={s.label} Icon={s.Icon} />
              ))}
            </div>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="mt-10 pt-5 border-t border-border flex items-center justify-center">
          <p
            className="text-[0.8125rem]"
            style={{
              color: "var(--color-text-subtle)",
              fontFamily: "var(--font-body)",
            }}
          >
            © {new Date().getFullYear()} NearCart. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
