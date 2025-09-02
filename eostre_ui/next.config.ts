import type { NextConfig } from "next";

const nextConfig: NextConfig = {
   async rewrites() {
    return [
      {
        source: "/api/auth/:path*",
        destination: "http://localhost:5000/auth/:path*", 
      },
      {
        source: "/api/locationserv/:path*",
        destination: "http://localhost:8001/:path*",
      },
    ];
  },
};

export default nextConfig;
