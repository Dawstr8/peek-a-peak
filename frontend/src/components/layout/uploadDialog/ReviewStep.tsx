"use client";

import { useState } from "react";

import dynamic from "next/dynamic";

import { ArrowUp, Clock } from "lucide-react";

import { Peak } from "@/lib/peaks/types";
import { photoDetailsFormatter as formatter } from "@/lib/photos/formatter";
import type { SummitPhotoCreate } from "@/lib/photos/types";

import { PhotoAspectRatio } from "@/components/photos/PhotoAspectRatio";
import { PhotoDetail } from "@/components/photos/PhotoDetail";
import { Button } from "@/components/ui/button";

import { useImageUrl } from "@/hooks/use-image-url";

import { PeakSearchInput } from "./PeakSearchInput";

const LocationMap = dynamic(
  () => import("./LocationMap").then((mod) => mod.LocationMap),
  { ssr: false },
);

interface ReviewStepProps {
  file: File;
  summitPhotoCreate: SummitPhotoCreate;
  onAccept: (summitPhotoCreate: SummitPhotoCreate, peak: Peak | null) => void;
  back: () => void;
}

export function ReviewStep({
  file,
  summitPhotoCreate,
  onAccept,
  back,
}: ReviewStepProps) {
  const [peak, setPeak] = useState<Peak | null>(null);
  const imageUrl = useImageUrl(file);

  const handleAccept = () => {
    onAccept({ ...summitPhotoCreate, peak_id: peak?.id }, peak);
  };

  const {
    latitude,
    longitude,
    altitude,
    captured_at: capturedAt,
  } = summitPhotoCreate;

  if (!imageUrl) {
    return (
      <div className="flex items-center justify-center p-12">
        <p className="text-muted-foreground">No file selected</p>
      </div>
    );
  }
  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-6 lg:flex-row">
        <div className="flex-1">
          <PhotoAspectRatio src={imageUrl} alt="Photo preview" />
        </div>

        <div className="flex-1 space-y-6">
          {altitude && (
            <PhotoDetail
              icon={<ArrowUp />}
              title="Altitude"
              description={formatter.formatAltitude(altitude)}
              className="p-0"
            />
          )}
          {capturedAt && (
            <PhotoDetail
              icon={<Clock />}
              title="Captured"
              description={formatter.formatCapturedAt(capturedAt)}
              className="p-0"
            />
          )}

          {latitude && longitude && (
            <PeakSearchInput
              latitude={latitude}
              longitude={longitude}
              onSelect={setPeak}
            />
          )}

          {latitude && longitude && (
            <div className="space-y-2">
              <h4 className="text-muted-foreground text-sm font-medium">
                Location
              </h4>
              <div className="h-64 overflow-hidden rounded-lg">
                <LocationMap
                  locations={[
                    {
                      index: "photo-location",
                      latitude: latitude,
                      longitude: longitude,
                      title: "Photo Location",
                      popupContent: `${formatter.formatLatitude(latitude)} ${formatter.formatLongitude(longitude)}`,
                    },
                  ]}
                />
              </div>
            </div>
          )}
        </div>
      </div>
      <div className="flex justify-center gap-4">
        <Button variant="outline" onClick={back}>
          Back
        </Button>
        <Button onClick={handleAccept}>Accept</Button>
      </div>
    </div>
  );
}
