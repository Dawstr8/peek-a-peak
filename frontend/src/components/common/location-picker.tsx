"use client";

import { useMemo } from "react";

import { Eraser, RotateCcw } from "lucide-react";

import { Location } from "@/lib/common/types";
import { Peak } from "@/lib/peaks/types";
import { locationsEqual } from "@/lib/utils";

import { PeakMarker } from "@/components/peaks/peak-marker";
import { Button } from "@/components/ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

import { useValueChange } from "@/hooks/use-value-change";

import { InteractiveMap } from "./interactive-map";
import { LocationMarker } from "./interactive-map/location-marker";
import { LocationsLine } from "./interactive-map/locations-line";
import { MapLocationPicker } from "./interactive-map/map-location-picker";

interface LocationPickerProps {
  value?: Location;
  onChange?: (value: Location | undefined) => void;
  peak: Peak | null;
}

export function LocationPicker({ value, onChange, peak }: LocationPickerProps) {
  const { originalValue, hasValueChanged } = useValueChange<
    Location | undefined
  >(value, locationsEqual);

  const locations = useMemo(() => {
    const locs = [];
    if (value) locs.push(value);
    if (peak) locs.push({ lat: peak.lat, lng: peak.lng, alt: peak.elevation });

    return locs;
  }, [value, peak]);

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <h3 className="text-muted-foreground text-sm font-medium">
          Where was this taken?
        </h3>
        <div className="flex items-center justify-center">
          <Tooltip>
            <TooltipTrigger asChild>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => onChange?.(originalValue)}
                disabled={!hasValueChanged()}
                className="cursor-pointer opacity-75 hover:opacity-100"
              >
                <RotateCcw className="size-4" />
              </Button>
            </TooltipTrigger>
            <TooltipContent>Reset</TooltipContent>
          </Tooltip>
          <Tooltip>
            <TooltipTrigger asChild>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => onChange?.(undefined)}
                disabled={!value}
                className="cursor-pointer opacity-75 hover:opacity-100"
              >
                <Eraser className="size-4" />
              </Button>
            </TooltipTrigger>
            <TooltipContent>Clear</TooltipContent>
          </Tooltip>
        </div>
      </div>
      <div className="rounded-lg">
        <InteractiveMap locations={locations} hideLocationMarkers>
          <MapLocationPicker onLocationSelect={onChange} />
          {value && (
            <LocationMarker location={value} text="Selected location" />
          )}
          {peak && <PeakMarker peak={peak} />}
          <LocationsLine locations={locations} />
        </InteractiveMap>
      </div>
    </div>
  );
}
