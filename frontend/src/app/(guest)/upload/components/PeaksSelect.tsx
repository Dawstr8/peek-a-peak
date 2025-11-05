import { AlertCircleIcon, Ruler, SearchX } from "lucide-react";

import type { PeakWithDistance } from "@/lib/peaks/types";
import { cn } from "@/lib/utils";

import { PeakCard } from "@/components/peaks/PeakCard";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Spinner } from "@/components/ui/spinner";

interface PeakSelectProps {
  peaksWithDistance: PeakWithDistance[];
  isLoading: boolean;
  error: Error | null;
  selectedId: number | null;
  onSelect: (peakWithDistance: PeakWithDistance) => void;
}

export function PeakSelect({
  peaksWithDistance,
  isLoading,
  error,
  selectedId,
  onSelect,
}: PeakSelectProps) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center gap-2 py-8">
        <Spinner className="size-8" />
        <span className="text-muted-foreground">Finding nearby peaks...</span>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertCircleIcon />
        <AlertTitle>Error Loading Peaks</AlertTitle>
        <AlertDescription>
          Failed to load nearby peaks. Please try again later.
        </AlertDescription>
      </Alert>
    );
  }

  if (!peaksWithDistance || peaksWithDistance.length === 0) {
    return (
      <Alert>
        <SearchX />
        <AlertTitle>No Peaks Found</AlertTitle>
        <AlertDescription>
          No peaks found near this location. You can still proceed without
          assigning a peak.
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {peaksWithDistance.map(({ peak, distance }) => {
        const isHighlighted = selectedId === peak.id;
        return (
          <PeakCard
            key={peak.id}
            peak={peak}
            className={cn(
              "hover:bg-accent/5 cursor-pointer transition-all",
              isHighlighted &&
                "ring-primary border-primary bg-accent/10 ring-2",
            )}
            onClick={() => onSelect({ peak, distance })}
          >
            <div className="text-muted-foreground flex items-center gap-2 text-sm">
              <Ruler className="h-3 w-3" />
              <span>{distance.toFixed(1)}m away</span>
            </div>
            <Badge
              variant={isHighlighted ? "default" : "secondary"}
              className="mt-2 w-full justify-center"
            >
              {isHighlighted ? "Selected" : "Select"}
            </Badge>
          </PeakCard>
        );
      })}
    </div>
  );
}
