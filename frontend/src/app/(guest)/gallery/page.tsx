"use client";
import { useQuery } from "@tanstack/react-query";

import { photoMetadataService } from "@/lib/metadata/service";
import { PhotoClient } from "@/lib/photos/client";

import { SummitPhotosGrid } from "@/components/photos/SummitPhotosGrid";

export default function Gallery() {
  const { data: summitPhotos, isLoading } = useQuery({
    queryKey: ["summitPhotos"],
    queryFn: async () => PhotoClient.getAllPhotos("captured_at", "desc"),
  });

  return (
    <div className="container mx-auto max-w-7xl p-10">
      <SummitPhotosGrid
        summitPhotos={summitPhotos}
        isLoading={isLoading}
        formatter={photoMetadataService.getFormatter()}
      />
    </div>
  );
}
