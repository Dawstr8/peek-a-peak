"use client";

import { useQuery } from "@tanstack/react-query";
import { Masonry } from "masonic";

import { photoMetadataService } from "@/lib/metadata/service";
import { PhotoClient } from "@/lib/photos/client";
import type { SummitPhoto } from "@/lib/photos/types";

import { SummitPhotoCard } from "@/components/photos/SummitPhotoCard";

export default function Gallery() {
  const { data: summitPhotos } = useQuery({
    queryKey: ["summitPhotos"],
    queryFn: async () => PhotoClient.getAllPhotos("captured_at", "desc"),
  });

  const renderCard = ({ data: summitPhoto }: { data: SummitPhoto }) => (
    <SummitPhotoCard
      key={summitPhoto.id}
      className="transition-all duration-200 hover:bg-gray-50 hover:shadow-lg"
      summitPhoto={summitPhoto}
      formatter={photoMetadataService.getFormatter()}
    />
  );

  return (
    <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
      <Masonry
        items={summitPhotos || []}
        render={renderCard}
        columnWidth={300}
        columnGutter={16}
        rowGutter={16}
      />
    </div>
  );
}
