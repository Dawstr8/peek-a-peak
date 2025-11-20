"use client";

import { LatLng } from "leaflet";
import { Eraser, RotateCcw } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

import { InteractiveMap } from "./InteractiveMap";

interface LocationPickerProps {
  originalValue?: LatLng;
  value?: LatLng;
  onChange?: (value: LatLng | undefined) => void;
}

export function LocationPicker({
  originalValue,
  value,
  onChange,
}: LocationPickerProps) {
  const hasLocationChanged = () => {
    if (!value && !originalValue) return false;
    if (!value || !originalValue) return true;

    return !value.equals(originalValue);
  };

  const handleResetLocation = () => {
    onChange?.(originalValue);
  };

  const handleClearLocation = () => {
    onChange?.(undefined);
  };

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
                onClick={handleResetLocation}
                disabled={!hasLocationChanged()}
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
                onClick={handleClearLocation}
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
          onLocationSelect={onChange}
          clickable={true}
        />
      </div>
    </div>
  );
}
