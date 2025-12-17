import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  images: {
    unoptimized: true,
  },
  rewrites: async () => {
    const backendUrl =
      process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    const s3Url = process.env.NEXT_PUBLIC_S3_URL;

    return [
      {
        source: "/api/:path*",
        destination: `${backendUrl}/api/:path*`,
      },
      {
        source: "/uploads/:path*",
        destination: `${s3Url || `${backendUrl}/uploads`}/:path*`,
      },
    ];
  },
};

export default nextConfig;
