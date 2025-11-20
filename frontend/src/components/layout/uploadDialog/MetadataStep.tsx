"use client";

import { useState } from "react";

import dynamic from "next/dynamic";

import { ArrowUp, Clock } from "lucide-react";

import { photoMetadataService } from "@/lib/metadata/service";
import type { PhotoMetadata } from "@/lib/metadata/types";
import { Peak } from "@/lib/peaks/types";
import { mapPhotoMetadataToSummitPhotoCreate } from "@/lib/photos/mappers";
import type { SummitPhotoCreate } from "@/lib/photos/types";

import { MetadataItem } from "@/components/metadata/MetadataItem";
import { PhotoAspectRatio } from "@/components/photos/PhotoAspectRatio";
import { Button } from "@/components/ui/button";

import { useImageUrl } from "@/hooks/use-image-url";

import { PeakSearchInput } from "./PeakSearchInput";

const LocationMap = dynamic(
  () => import("./LocationMap").then((mod) => mod.LocationMap),
  { ssr: false },
);

interface MetadataStepProps {
  file: File;
  metadata: PhotoMetadata;
  onAccept: (summitPhotoCreate: SummitPhotoCreate, peak: Peak | null) => void;
  back: () => void;
  next: () => void;
}

export function MetadataStep({
  file,
  metadata,
  onAccept,
  back,
  next,
}: MetadataStepProps) {
  const [summitPhotoCreate, setSummitPhotoCreate] = useState<SummitPhotoCreate>(
    mapPhotoMetadataToSummitPhotoCreate(metadata),
  );

  const [peak, setPeak] = useState<Peak | null>(null);

  const imageUrl = useImageUrl(file);

  const handleSelect = (peak: Peak | null) => {
    setPeak(peak);
    setSummitPhotoCreate((prevSummitPhotoCreate) => ({
      ...prevSummitPhotoCreate,
      peak_id: peak?.id,
    }));
  };

  const handleAccept = () => {
    onAccept(summitPhotoCreate, peak);
    next();
  };

  const { latitude, longitude } = metadata;
  const formatter = photoMetadataService.getFormatter();

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
          {metadata.altitude && (
            <MetadataItem
              icon={<ArrowUp />}
              title="Altitude"
              description={formatter.formatAltitude(metadata.altitude)}
              className="p-0"
            />
          )}
          {metadata.capturedAt && (
            <MetadataItem
              icon={<Clock />}
              title="Captured"
              description={formatter.formatCapturedAt(metadata.capturedAt)}
              className="p-0"
            />
          )}

          {latitude && longitude && (
            <PeakSearchInput
              latitude={latitude}
              longitude={longitude}
              onSelect={handleSelect}
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
