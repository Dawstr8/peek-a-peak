"use client";

import { useState } from "react";

import { LatLng } from "leaflet";

import { Peak } from "@/lib/peaks/types";
import type { SummitPhotoCreate } from "@/lib/photos/types";

import { DateTimePicker } from "@/components/common/DateTimePicker";
import { LocationPicker } from "@/components/common/LocationPicker";
import { PhotoAspectRatio } from "@/components/photos/PhotoAspectRatio";
import { Button } from "@/components/ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

import { useImageUrl } from "@/hooks/use-image-url";

import { PeakSearchInput } from "./PeakSearchInput";

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
  const imageUrl = useImageUrl(file);

  const [location, setLocation] = useState<LatLng | undefined>(() => {
    const { latitude: lat, longitude: lng, altitude: alt } = summitPhotoCreate;
    return lat && lng ? new LatLng(lat, lng, alt) : undefined;
  });

  const [capturedAt, setCapturedAt] = useState<Date | undefined>(() => {
    return summitPhotoCreate.captured_at
      ? new Date(summitPhotoCreate.captured_at)
      : undefined;
  });

  const [peak, setPeak] = useState<Peak | null>(null);

  const handleAccept = () => {
    onAccept(
      {
        ...summitPhotoCreate,
        peak_id: peak?.id,
        captured_at: capturedAt?.toISOString() || undefined,
        latitude: location?.lat,
        longitude: location?.lng,
        altitude: location?.alt,
      },
      peak,
    );
  };

  const {
    latitude: lat,
    longitude: lng,
    altitude: alt,
    captured_at: prevCapturedAt,
  } = summitPhotoCreate;

  const originalLocation = lat && lng ? new LatLng(lat, lng, alt) : undefined;
  const originalCapturedAt = prevCapturedAt
    ? new Date(prevCapturedAt)
    : undefined;

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
          <LocationPicker
            originalValue={originalLocation}
            value={location}
            onChange={setLocation}
          />

          <DateTimePicker
            originalValue={originalCapturedAt}
            value={capturedAt}
            onChange={setCapturedAt}
          />

          <Tooltip>
            <TooltipTrigger asChild>
              <div>
                <PeakSearchInput
                  disabled={!location}
                  latitude={location?.lat ?? 0}
                  longitude={location?.lng ?? 0}
                  onSelect={setPeak}
                />
              </div>
            </TooltipTrigger>
            {!location && (
              <TooltipContent>Select location first</TooltipContent>
            )}
          </Tooltip>
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
