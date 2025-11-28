"use client";

import { useMemo, useState } from "react";

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
  const {
    setValue,
    watch,
    trigger,
    formState: { errors },
  } = useFormContext<UploadPhotoFormData>();
  const [file, capturedAt, lat, lng, alt] = watch([
    "file",
    "capturedAt",
    "lat",
    "lng",
    "alt",
  ]);

  const imageUrl = useImageUrl(file);

  const location = useMemo(() => {
    return lat && lng ? new LatLng(lat, lng, alt) : undefined;
  }, [lat, lng, alt]);

  const capturedAtDate = useMemo(() => {
    return capturedAt ? new Date(capturedAt) : undefined;
  }, [capturedAt]);

  const [peak, setPeak] = useState<Peak | null>(null);

  const handleAccept = async () => {
    const isValid = await trigger(["capturedAt"]);
    if (!isValid) return;

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
          <LocationPicker
            value={location}
            onChange={(location) => {
              setValue("lat", location?.lat);
              setValue("lng", location?.lng);
              setValue("alt", location?.alt);
            }}
            peak={peak}
          />
          <div>
            <DateTimePicker
              value={capturedAtDate}
              onChange={(date) =>
                setValue("capturedAt", date ? date.toISOString() : "", {
                  shouldValidate: true,
                })
              }
            />
            <span className="text-destructive ml-2 text-xs">
              {errors.capturedAt?.message}
            </span>
          </div>
          <Tooltip>
            <TooltipTrigger asChild>
              <div>
                <PeakSearchInput
                  disabled={!location}
                  lat={location?.lat ?? 0}
                  lng={location?.lng ?? 0}
                  onSelect={(peak) => {
                    setValue("peakId", peak?.id);
                    setPeak(peak);
                    setPeakToDisplay(peak);
                  }}
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
        <Button onClick={handleAccept} disabled={!!errors.capturedAt}>
          Accept
        </Button>
      </div>
    </div>
  );
}
