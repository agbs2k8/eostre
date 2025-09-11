import React from "react";
import clsx from "clsx";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: "primary" | "secondary"; // optional custom props
}

export function Button({ children, className, ...props }: ButtonProps) {
  return (
    <button
      className={clsx(
        "px-8 py-2 font-semibold transition-colors duration-200 rounded-lg",
        "bg-brand-accent text-brand-light hover:bg-brand-primary hover:text-brand-light",
        className
      )}
      {...props} 
    >
      {children}
    </button>
  );
}