import React from "react";

export const Button = ({ children }: { children: React.ReactNode }) => (
  <button className="px-4 py-2 bg-blue-600 text-white rounded">
    {children}
  </button>
);
