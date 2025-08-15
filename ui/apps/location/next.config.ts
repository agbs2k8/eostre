import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/locationserv/:path*",
        destination: "http://localhost:8001/:path*", // Proxy to your API service
      },
    ];
  },
};

export default nextConfig;
