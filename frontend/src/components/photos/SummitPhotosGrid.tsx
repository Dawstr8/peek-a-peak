"use client";

import { Camera } from "lucide-react";

import type { PhotoMetadataFormatter } from "@/lib/metadata/types";
import type { SummitPhoto } from "@/lib/photos/types";

import { MessageBlock } from "@/components/common/MessageBlock";
import CallToAction from "@/components/layout/topbar/CallToAction";
import { Spinner } from "@/components/ui/spinner";

import { SummitPhotoCard } from "./SummitPhotoCard";

interface SummitPhotosGridProps {
  summitPhotos: SummitPhoto[] | undefined;
  isLoading: boolean;
  formatter: PhotoMetadataFormatter;
}

export function SummitPhotosGrid({
  summitPhotos,
  isLoading,
  formatter,
}: SummitPhotosGridProps) {
  if (isLoading) {
    return (
      <div className="flex w-full items-center justify-center py-20">
        <Spinner className="text-muted-foreground size-8" />
      </div>
    );
  }

  if (!summitPhotos || summitPhotos.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <MessageBlock
          iconComponent={Camera}
          title="Start your summit journal"
          description="Upload photos from your mountain adventures to create a personal diary of your achievements"
          className="mb-4"
        />
        <CallToAction />
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {summitPhotos.map((summitPhoto) => (
        <SummitPhotoCard
          key={summitPhoto.id}
          className="transition-all duration-200 hover:bg-gray-50 hover:shadow-lg"
          summitPhoto={summitPhoto}
          formatter={formatter}
        />
      ))}
    </div>
  );
}
