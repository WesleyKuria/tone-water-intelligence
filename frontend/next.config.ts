import path from "path";
import { fileURLToPath } from "url";
import type { NextConfig } from "next";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const nextConfig: NextConfig = {
  webpack: (config) => {
    config.resolve.modules = [
      path.resolve(process.cwd(), "node_modules"),
      path.resolve(__dirname, "node_modules"),
      ...(config.resolve.modules || ["node_modules"]),
    ];
    return config;
  },
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          {
            key: "Content-Security-Policy",
            value: [
              "default-src 'self'",
              "script-src 'self' 'unsafe-eval' 'unsafe-inline' blob:",
              "worker-src 'self' blob:",
              "connect-src 'self' https: https://*.cartocdn.com https://*.basemaps.cartocdn.com https://basemaps.cartocdn.com https://services.arcgisonline.com http://localhost:8000 http://127.0.0.1:8000",
              "img-src 'self' data: blob: https://*.cartocdn.com https://*.basemaps.cartocdn.com https://services.arcgisonline.com https://maps.googleapis.com",
              "style-src 'self' 'unsafe-inline' https://*.cartocdn.com https://basemaps.cartocdn.com",
              "font-src 'self' data:",
            ].join("; "),
          },
        ],
      },
    ];
  },
};

export default nextConfig;
