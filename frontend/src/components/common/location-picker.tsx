"use client";

import { useMemo } from "react";

import { LatLng } from "leaflet";
import { Eraser, RotateCcw } from "lucide-react";
import { Marker, Polyline, Popup } from "react-leaflet";

import { createPeakIcon } from "@/lib/leaflet";
import { Peak } from "@/lib/peaks/types";
import { photoDetailsFormatter } from "@/lib/photos/formatter";
import { latLngEqual } from "@/lib/utils";

import { Button } from "@/components/ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

import { useValueChange } from "@/hooks/use-value-change";

import { FitToLocations } from "./fit-to-locations";
import { InteractiveMap } from "./interactive-map";
import { MapLocationPicker } from "./map-location-picker";

interface LocationPickerProps {
  value?: LatLng;
  onChange?: (value: LatLng | undefined) => void;
  peak: Peak | null;
}

export function LocationPicker({ value, onChange, peak }: LocationPickerProps) {
  const { originalValue, hasValueChanged } = useValueChange<LatLng | undefined>(
    value,
    latLngEqual,
  );

  const locations = useMemo(() => {
    const locs = [];
    if (value) locs.push(value);
    if (peak) locs.push(new LatLng(peak.lat, peak.lng, peak.elevation));

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
            <Marker position={value}>
              <Popup>
                <strong>Selected location</strong>
                <br />
                Latitude: {photoDetailsFormatter.formatLat(value.lat)}
                <br />
                Longitude: {photoDetailsFormatter.formatLng(value.lng)}
                <br />
                Altitude: {photoDetailsFormatter.formatAlt(value.alt)}
              </Popup>
            </Marker>
          )}

          {peak && (
            <Marker
              key={peak.id}
              position={new LatLng(peak.lat, peak.lng)}
              icon={createPeakIcon(18, "green")}
            >
              <Popup>
                <strong>{peak.name}</strong>
                <br />
                {photoDetailsFormatter.formatAlt(peak.elevation)}
              </Popup>
            </Marker>
          )}

          {locations.length > 1 && (
            <Polyline
              positions={locations}
              pathOptions={{ dashArray: "1 8" }}
            />
          )}
        </InteractiveMap>
      </div>
    </div>
  );
}
