"use client";

import { LatLng } from "leaflet";
import { Eraser, RotateCcw } from "lucide-react";

import { Peak } from "@/lib/peaks/types";
import { latLngEqual } from "@/lib/utils";

import { Button } from "@/components/ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

import { useValueChange } from "@/hooks/use-value-change";

import { InteractiveMap } from "./InteractiveMap";

interface LocationPickerProps {
  value?: LatLng;
  onChange?: (value: LatLng | undefined) => void;
  targetLocation?: LatLng;
  peaks?: Peak[];
}

export function LocationPicker({
  value,
  onChange,
  targetLocation,
  peaks = [],
}: LocationPickerProps) {
  const { originalValue, hasValueChanged } = useValueChange<LatLng | undefined>(
    value,
    latLngEqual,
  );

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
        <InteractiveMap
          location={value}
          onLocationSelect={(newLocation) => onChange?.(newLocation)}
          targetLocation={targetLocation!}
          peaks={peaks}
          clickable={true}
        />
      </div>
    </div>
  );
}
