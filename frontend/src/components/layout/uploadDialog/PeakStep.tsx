"use client";

import { useState } from "react";

import type { Peak, PeakWithDistance } from "@/lib/peaks/types";
import type { SummitPhotoCreate } from "@/lib/photos/types";

import { Button } from "@/components/ui/button";

import { PeakSearchInput } from "./PeakSearchInput";

interface PeakStepProps {
  summitPhotoCreate: SummitPhotoCreate | null;
  setSummitPhotoCreate: (summitPhotoCreate: SummitPhotoCreate) => void;
  setSelectedPeak: (peak: Peak | null) => void;
  back: () => void;
  next: () => void;
}

export function PeakStep({
  summitPhotoCreate,
  setSummitPhotoCreate,
  setSelectedPeak,
  back,
  next,
}: PeakStepProps) {
  const [isSelected, setIsSelected] = useState<boolean>(false);

  const { latitude, longitude } = summitPhotoCreate || {};

  const handleSelect = (peakWithDistance: PeakWithDistance | null) => {
    const isSelected = peakWithDistance !== null;
    const peak = isSelected ? peakWithDistance.peak : null;
    const distance = isSelected ? peakWithDistance.distance : undefined;
    const peakId = isSelected ? peakWithDistance.peak.id : undefined;

    setIsSelected(isSelected);
    setSelectedPeak(peak);
    setSummitPhotoCreate({
      ...summitPhotoCreate,
      peak_id: peakId,
      distance_to_peak: distance,
    });
  };

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h3 className="mb-2 text-lg font-semibold">Select a Peak</h3>
        <p className="text-muted-foreground">
          Choose the peak this photo was taken near. This helps organize your
          mountain adventures.
        </p>
      </div>

      {latitude && longitude && (
        <PeakSearchInput
          latitude={latitude}
          longitude={longitude}
          onSelect={handleSelect}
        />
      )}

      <div className="flex flex-col gap-4">
        <div className="flex justify-center gap-4">
          <Button variant="outline" onClick={back}>
            Back
          </Button>
          <Button onClick={next} size="lg">
            {isSelected ? "Confirm Selection" : "Skip Peak Selection"}
          </Button>
        </div>
      </div>
    </div>
  );
}
