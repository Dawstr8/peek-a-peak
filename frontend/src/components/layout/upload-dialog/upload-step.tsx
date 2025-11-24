"use client";

import { useMutation } from "@tanstack/react-query";

import type { Peak } from "@/lib/peaks/types";
import { PhotoClient } from "@/lib/photos/client";
import { photoDetailsFormatter } from "@/lib/photos/formatter";
import type { SummitPhoto, SummitPhotoCreate } from "@/lib/photos/types";

import { SummitPhotoCard } from "@/components/photos/summit-photo-card";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";

interface UploadStepProps {
  file: File;
  summitPhotoCreate: SummitPhotoCreate;
  selectedPeak: Peak | null;
  back: () => void;
  next: () => void;
}

export function UploadStep({
  file,
  summitPhotoCreate,
  selectedPeak,
  back,
  next,
}: UploadStepProps) {
  const { isPending, isError, error, mutate } = useMutation({
    mutationFn: ({
      file,
      summitPhotoCreate,
    }: {
      file: File;
      summitPhotoCreate: SummitPhotoCreate | null;
    }) => PhotoClient.uploadPhoto(file, summitPhotoCreate),
    onSuccess: () => {
      next();
    },
  });

  const summitPhoto = {
    ...summitPhotoCreate,
    fileName: URL.createObjectURL(file),
    uploadedAt: new Date().toISOString(),
    id: 999,
    peak: selectedPeak,
  } as unknown as SummitPhoto;

  return (
    <div className="space-y-6">
      {isError && (
        <div className="bg-destructive/10 border-destructive/30 text-destructive rounded-lg border px-4 py-3">
          {error.message}
        </div>
      )}

      <SummitPhotoCard
        summitPhoto={summitPhoto}
        formatter={photoDetailsFormatter}
        uploadsBaseUrl=""
        className="mx-auto max-w-1/3"
      />
      <div className="flex justify-center gap-4">
        <Button variant="outline" onClick={back}>
          Back
        </Button>
        <Button
          onClick={() => file && mutate({ file, summitPhotoCreate })}
          disabled={isPending}
        >
          {isPending && <Spinner />}
          {isPending ? "Uploading..." : "Upload Photo"}
        </Button>
      </div>
    </div>
  );
}
