"use client";

import { useState } from "react";

import { LatLng } from "leaflet";
import { useFormContext } from "react-hook-form";

import { Peak } from "@/lib/peaks/types";

import { DateTimePicker } from "@/components/common/date-time-picker";
import { LocationPicker } from "@/components/common/location-picker";
import { PhotoAspectRatio } from "@/components/photos/photo-aspect-ratio";
import { Button } from "@/components/ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

import { useImageUrl } from "@/hooks/use-image-url";

import type { UploadPhotoFormData } from "../upload-dialog";
import { PeakSearchInput } from "./peak-search-input";

interface ReviewStepProps {
  setPeakToDisplay: (peak: Peak | null) => void;
  back: () => void;
  next: () => void;
}

export function ReviewStep({ setPeakToDisplay, back, next }: ReviewStepProps) {
  const { setValue, getValues } = useFormContext<UploadPhotoFormData>();
  const { file, capturedAt, lat, lng, alt } = getValues();

  const imageUrl = useImageUrl(file);

  const [location, setLocation] = useState<LatLng | undefined>(() => {
    return lat && lng ? new LatLng(lat, lng, alt) : undefined;
  });

  const [capturedAtDate, setCapturedAtDate] = useState<Date | undefined>(() => {
    return capturedAt ? new Date(capturedAt) : undefined;
  });

  const [peak, setPeak] = useState<Peak | null>(null);

  const handleAccept = () => {
    if (capturedAtDate) setValue("capturedAt", capturedAtDate.toISOString());
    if (location) {
      setValue("lat", location.lat);
      setValue("lng", location.lng);
      setValue("alt", location.alt);
    }
    if (peak) setValue("peakId", peak.id);

    setPeakToDisplay(peak);

    next();
  };

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
          <LocationPicker value={location} onChange={setLocation} peak={peak} />
          <DateTimePicker value={capturedAtDate} onChange={setCapturedAtDate} />
          <Tooltip>
            <TooltipTrigger asChild>
              <div>
                <PeakSearchInput
                  disabled={!location}
                  lat={location?.lat ?? 0}
                  lng={location?.lng ?? 0}
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
