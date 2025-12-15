"use client";

import { useMutation } from "@tanstack/react-query";
import { useFormContext } from "react-hook-form";

import { detailsFormatter } from "@/lib/common/formatter";
import type { Peak } from "@/lib/peaks/types";
import { PhotoClient } from "@/lib/photos/client";
import type { SummitPhoto, SummitPhotoCreate } from "@/lib/photos/types";

import { SummitPhotoCard } from "@/components/photos/summit-photo-card";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";

import type { UploadPhotoFormData } from "../upload-dialog";

interface UploadStepProps {
  peakToDisplay: Peak | null;
  back: () => void;
  next: () => void;
}

export function UploadStep({ peakToDisplay, back, next }: UploadStepProps) {
  const { getValues } = useFormContext<UploadPhotoFormData>();

  const { file, capturedAt, lat, lng, alt, peakId } = getValues();
  const summitPhotoCreate = {
    capturedAt,
    lat,
    lng,
    alt,
    peakId,
  } as SummitPhotoCreate;

  const summitPhoto = {
    ...summitPhotoCreate,
    fileName: URL.createObjectURL(file),
    id: 999,
    peak: peakToDisplay,
  } as SummitPhoto;

  const { isPending, isError, error, mutate } = useMutation({
    mutationFn: () => PhotoClient.uploadPhoto(file, summitPhotoCreate),
    onSuccess: () => {
      next();
    },
  });

  return (
    <div className="space-y-6">
      {isError && (
        <div className="bg-destructive/10 border-destructive/30 text-destructive rounded-lg border px-4 py-3">
          {error.message}
        </div>
      )}

      <SummitPhotoCard
        summitPhoto={summitPhoto}
        formatter={detailsFormatter}
        uploadsBaseUrl=""
        className="mx-auto max-w-1/3"
      />
      <div className="flex justify-center gap-4">
        <Button variant="outline" onClick={back}>
          Back
        </Button>
        <Button onClick={() => mutate()} disabled={isPending}>
          {isPending && <Spinner />}
          {isPending ? "Uploading..." : "Upload Photo"}
        </Button>
      </div>
    </div>
  );
}
