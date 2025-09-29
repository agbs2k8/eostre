import React from "react";
import clsx from "clsx";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: "primary" | "secondary"; // optional custom props
  size?: "sm" | "md" | "lg";
}

export function Button({
  children, 
  className, 
  variant = "primary",
  size = "md", 
  ...props 
}: ButtonProps) {
  return (
    <button
      className={clsx(
        "font-semibold transition-colors duration-200 rounded-lg",
        // size variations
        size === "sm" && "px-3 py-1 text-sm",
        size === "md" && "px-5 py-2 text-base",
        size === "lg" && "px-8 py-3 text-lg",
        // variant variations
        variant === "primary" &&
          "bg-brand-accent text-brand-light hover:bg-brand-primary hover:text-brand-light",
        variant === "secondary" &&
          "bg-gray-200 text-gray-900 hover:bg-gray-300",
        className
      )}
      {...props} 
    >
      {children}
    </button>
  );
}