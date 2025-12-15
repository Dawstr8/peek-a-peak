"use client";

import { Camera, Plus } from "lucide-react";

import type { SummitPhoto } from "@/lib/photos/types";

import { MessageBlock } from "@/components/common/message-block";
import { useUploadDialog } from "@/components/layout/upload-dialog-context";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";

import { SummitPhotoHoverableCard } from "./summit-photo-hoverable-card";

interface SummitPhotosGridProps {
  summitPhotos: SummitPhoto[] | undefined;
  isLoading: boolean;
}

export function SummitPhotosGrid({
  summitPhotos,
  isLoading,
}: SummitPhotosGridProps) {
  const { openDialog } = useUploadDialog();

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
        <Button onClick={openDialog}>
          <Plus />
          Add your first trip
        </Button>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 gap-0.5 sm:grid-cols-3 lg:grid-cols-4">
      {summitPhotos.map((summitPhoto) => (
        <SummitPhotoHoverableCard
          key={summitPhoto.id}
          summitPhoto={summitPhoto}
        />
      ))}
    </div>
  );
}
