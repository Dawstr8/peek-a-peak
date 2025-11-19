"use client";

import { useState } from "react";

import dynamic from "next/dynamic";

import { photoMetadataService } from "@/lib/metadata/service";
import type { PhotoMetadata } from "@/lib/metadata/types";
import { Peak, PeakWithDistance } from "@/lib/peaks/types";
import { mapPhotoMetadataToSummitPhotoCreate } from "@/lib/photos/mappers";
import type { SummitPhotoCreate } from "@/lib/photos/types";

import { MetadataDisplay } from "@/components/metadata/MetadataDisplay";
import { Button } from "@/components/ui/button";

import { PeakSearchInput } from "./PeakSearchInput";

const LocationMap = dynamic(
  () => import("./LocationMap").then((mod) => mod.LocationMap),
  { ssr: false },
);

interface MetadataStepProps {
  metadata: PhotoMetadata;
  onAccept: (summitPhotoCreate: SummitPhotoCreate, peak: Peak | null) => void;
  back: () => void;
  next: () => void;
}

export function MetadataStep({
  metadata,
  onAccept,
  back,
  next,
}: MetadataStepProps) {
  const [summitPhotoCreate, setSummitPhotoCreate] = useState<SummitPhotoCreate>(
    mapPhotoMetadataToSummitPhotoCreate(metadata),
  );

  const [peakWithDistance, setPeakWithDistance] =
    useState<PeakWithDistance | null>(null);

  const handleSelect = (peakWithDistance: PeakWithDistance | null) => {
    const peakId = peakWithDistance ? peakWithDistance.peak.id : undefined;
    const distance = peakWithDistance ? peakWithDistance.distance : undefined;

    setPeakWithDistance(peakWithDistance);
    setSummitPhotoCreate((prevSummitPhotoCreate) => ({
      ...prevSummitPhotoCreate,
      peak_id: peakId,
      distance_to_peak: distance,
    }));
  };

  const handleAccept = () => {
    onAccept(
      summitPhotoCreate,
      peakWithDistance ? peakWithDistance.peak : null,
    );
    next();
  };

  const { latitude, longitude } = metadata;

  return (
    <div className="space-y-6">
      <MetadataDisplay
        metadata={metadata}
        formatter={photoMetadataService.getFormatter()}
        className="bg-muted/20"
      />

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
            Location Preview
          </h4>
          <LocationMap
            locations={[
              {
                index: "photo-location",
                latitude: latitude,
                longitude: longitude,
                title: "Photo Location",
                popupContent: `${photoMetadataService.getFormatter().formatLatitude(latitude)} ${photoMetadataService.getFormatter().formatLongitude(longitude)}`,
              },
            ]}
          />
        </div>
      )}
      <div className="flex justify-center gap-4">
        <Button variant="outline" onClick={back}>
          Back
        </Button>
        <Button onClick={handleAccept}>Accept</Button>
      </div>
    </div>
  );
}
