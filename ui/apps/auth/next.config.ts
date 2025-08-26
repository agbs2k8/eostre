import TsconfigPathsPlugin from "tsconfig-paths-webpack-plugin";
import type { NextConfig } from "next";
import type { Configuration } from "webpack";

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
  webpack: (config: Configuration) => {
    if (!config.resolve?.plugins) config.resolve!.plugins = [];
    config.resolve!.plugins!.push(new TsconfigPathsPlugin());
    return config;
  },
};

export default nextConfig;
