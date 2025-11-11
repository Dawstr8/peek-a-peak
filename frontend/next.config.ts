import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    unoptimized: true,
  },
  rewrites: async () => {
    return [
      {
        source: "/api/:path*",
        destination: "http://backend:8000/api/:path*",
      },
      {
        source: "/uploads/:path*",
        destination: "http://backend:8000/uploads/:path*",
      },
    ];
  },
};

export default nextConfig;
