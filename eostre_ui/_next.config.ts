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
      {
        source: "/api/v1/:path*",
        destination: "http://localhost:5000/api/v1/:path*", 
      },
    ];
  },
};

export default nextConfig;
