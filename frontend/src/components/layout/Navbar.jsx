// components/layout/Navbar.jsx
// UPDATED FOR TAILWIND V4

import { LogIn, UserPlus } from "lucide-react";
import Button from "@/components/ui/Button";
import Logo from "@/components/ui/Logo";

export default function Navbar({ onLogin, onSignup }) {
  return (
    <header className="bg-bg border-b border-border sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-[60px] flex items-center justify-between">
        {/* Logo */}
        <a href="/" aria-label="NearCart home" className="no-underline">
          <Logo />
        </a>

        {/* Auth actions */}
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            icon={<UserPlus size={14} />}
            onClick={onSignup}
          >
            Sign up
          </Button>
          <Button
            variant="primary"
            size="sm"
            icon={<LogIn size={14} />}
            onClick={onLogin}
          >
            Log in
          </Button>
        </div>
      </div>
    </header>
  );
}
