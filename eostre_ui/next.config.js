/** @type {import('next').NextConfig} */
const pick = (...vals) => vals.find(v => v && v.trim().length) || "";

const ADMIN_INTERNAL = pick(
  process.env.ADMIN_API_INTERNAL,          // .env.local (local dev) or docker env
  process.env.NEXT_PUBLIC_ADMIN_API,       // public fallback
  "http://localhost:5000"                  // final fallback
);

const LOCATION_INTERNAL = pick(
  process.env.LOCATION_API_INTERNAL,
  process.env.NEXT_PUBLIC_LOCATION_API,
  "http://localhost:8001"
);

module.exports = {
  trailingSlash: false,
  skipTrailingSlashRedirect: true,
  async rewrites() {
  const admin = ADMIN_INTERNAL.replace(/\/$/, "");
  const loc = LOCATION_INTERNAL.replace(/\/$/, "");
  return [
    { 
      source: "/auth/:path*",
      destination: `${admin}/auth/:path*` 
    },
    { 
      source: "/locationserv/:path*",
      destination: `${loc}/:path*`
    },
    { 
      source: "/v1api/:path*",
      destination: `${admin}/api/v1/:path*`
    }
  ];
}
};