"use client";

import { ArrowUp, Mountain } from "lucide-react";

import type { PeakWithDistance } from "@/lib/peaks/types";
import { cn } from "@/lib/utils";

import { Badge } from "@/components/ui/badge";

interface PeakListItemProps {
  peakWithDistance: PeakWithDistance;
  className?: string;
  children?: React.ReactNode;
}

export function PeakListItem({
  peakWithDistance,
  className,
  children,
}: PeakListItemProps) {
  const { peak, distance } = peakWithDistance;

  return (
    <div
      className={cn(
        "flex items-center gap-3 rounded-md p-3 text-left",
        className,
      )}
    >
      <div className="bg-muted flex size-8 items-center justify-center rounded-full">
        <Mountain className="size-4" />
      </div>
      <div className="min-w-0 flex-1">
        <p className="truncate text-sm font-medium">{peak.name}</p>
        <div className="text-muted-foreground flex items-center gap-4 text-xs">
          <span>{(distance / 1000).toFixed(1)}km away</span>
          <span className="flex items-center gap-1">
            <ArrowUp className="size-3" />
            {peak.elevation}m
          </span>
          <Badge variant="secondary" className="text-xs">
            {peak.mountain_range.name}
          </Badge>
        </div>
      </div>
      {children}
    </div>
  );
}
