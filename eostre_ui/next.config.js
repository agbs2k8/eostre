/** @type {import('next').NextConfig} */
const ADMIN_INTERNAL = process.env.ADMIN_API_INTERNAL || "http://localhost:5000";
const LOCATION_INTERNAL = process.env.LOCATION_API_INTERNAL || "http://localhost:8001";

module.exports = {
  async rewrites() {
    const admin = ADMIN_INTERNAL.replace(/\/$/, "");
    const loc = LOCATION_INTERNAL.replace(/\/$/, "");
    return [
      {
        source: "/api/auth/:path*",
        destination: `${admin}/auth/:path*`,
      },
      {
        source: "/api/locationserv/:path*",
        destination: `${loc}/:path*`,
      },
      {
        source: "/api/v1/:path*",
        destination: `${admin}/api/v1/:path*`,
      },
    ];
  },
};