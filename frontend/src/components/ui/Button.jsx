// components/ui/Button.jsx
// UPDATED WITH ADDITIONAL VARIANTS AND PROPS

import { forwardRef } from "react";

const Button = forwardRef(function Button(
  {
    variant = "primary",
    size = "md",
    children,
    icon,
    iconPosition = "left",
    className = "",
    disabled = false,
    fullWidth = false,
    onClick,
    ...props
  },
  ref,
) {
  // Base Tailwind classes
  const baseClasses =
    "font-semibold rounded-md transition-all duration-150 cursor-pointer inline-flex items-center justify-center gap-2 border-none";

  // Size variants
  const sizes = {
    sm: "px-3 py-1.5 text-[0.8125rem]",
    md: "px-4 py-2.5 text-[0.9375rem]",
    lg: "px-6 py-3 text-base",
  };

  // Style objects for variants
  const variantStyles = {
    primary: {
      background: "var(--color-primary)",
      color: "var(--color-primary-fg)",
      border: "none",
    },
    outline: {
      background: "transparent",
      color: "var(--color-text-body)",
      border: "1px solid var(--color-border)",
    },
    soft: {
      background: "var(--color-primary-light)",
      color: "var(--color-primary)",
      border: "1px solid var(--color-primary-border)",
    },
    ghost: {
      background: "transparent",
      color: "var(--color-text-body)",
      border: "none",
    },
  };

  const variantStyle = variantStyles[variant];

  const handleMouseEnter = (e) => {
    if (disabled) return;
    if (variant === "primary") {
      e.currentTarget.style.background = "var(--color-primary-hover)";
    } else if (variant === "outline") {
      e.currentTarget.style.backgroundColor = "var(--color-surface)";
    } else if (variant === "soft") {
      e.currentTarget.style.backgroundColor = "var(--color-primary)";
      e.currentTarget.style.color = "var(--color-primary-fg)";
    }
  };

  const handleMouseLeave = (e) => {
    if (disabled) return;
    if (variant === "primary") {
      e.currentTarget.style.background = variantStyle.background;
    } else if (variant === "outline") {
      e.currentTarget.style.backgroundColor = variantStyle.background;
    } else if (variant === "soft") {
      e.currentTarget.style.backgroundColor = variantStyle.background;
      e.currentTarget.style.color = variantStyle.color;
    }
  };

  const widthClass = fullWidth ? "w-full" : "";

  return (
    <button
      ref={ref}
      className={`${baseClasses} ${sizes[size]} ${widthClass} ${className} ${
        disabled ? "opacity-50 cursor-not-allowed" : ""
      }`}
      style={variantStyle}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      disabled={disabled}
      onClick={onClick}
      {...props}
    >
      {icon && iconPosition === "left" && icon}
      {children}
      {icon && iconPosition === "right" && icon}
    </button>
  );
});

Button.displayName = "Button";

export default Button;
