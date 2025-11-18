"use client";

import { useCallback, useState } from "react";

import { useQuery } from "@tanstack/react-query";
import { millisecondsInMinute } from "date-fns/constants";
import { Check, MapPin } from "lucide-react";

import { PeakClient } from "@/lib/peaks/client";
import type { PeakWithDistance } from "@/lib/peaks/types";
import { cn } from "@/lib/utils";

import { PeakListItem, PeakListItemSkeleton } from "@/components/peaks";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

import { useDebounce } from "@/hooks/use-debounce";

interface PeakSearchInputProps {
  latitude: number;
  longitude: number;
  onSelect: (peakWithDistance: PeakWithDistance | null) => void;
  limit?: number;
}

export function PeakSearchInput({
  latitude,
  longitude,
  onSelect,
  limit = 8,
}: PeakSearchInputProps) {
  const [open, setOpen] = useState(false);
  const [selectedPeakWithDistance, setSelectedPeakWithDistance] =
    useState<PeakWithDistance | null>(null);

  const [searchQuery, setSearchQuery] = useState("");
  const debouncedQuery = useDebounce(searchQuery);

  const {
    data: peaksWithDistance = [],
    isLoading,
    error,
  } = useQuery({
    queryKey: ["peak-search", latitude, longitude, debouncedQuery, limit],
    queryFn: () =>
      PeakClient.findNearbyPeaks(
        latitude,
        longitude,
        limit,
        debouncedQuery.trim() || undefined,
      ),
    enabled: !!latitude && !!longitude,
    staleTime: 5 * millisecondsInMinute,
  });

  const handleSelect = useCallback(
    (peakWithDistance: PeakWithDistance) => {
      setOpen(false);

      if (selectedPeakWithDistance === peakWithDistance) {
        setSelectedPeakWithDistance(null);
        setSearchQuery("");
        onSelect(null);
        return;
      }

      setSelectedPeakWithDistance(peakWithDistance);
      setSearchQuery(peakWithDistance.peak.name);
      onSelect(peakWithDistance);
    },
    [onSelect, selectedPeakWithDistance],
  );

  const displayValue = selectedPeakWithDistance
    ? selectedPeakWithDistance.peak.name
    : "";

  return (
    <Popover open={open} onOpenChange={setOpen} modal={true}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-full cursor-pointer justify-between"
        >
          <span className={cn(!displayValue && "text-foreground/75")}>
            {displayValue || "Select where this photo was taken..."}
          </span>
          <MapPin className="size-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent
        className="w-[var(--radix-popover-trigger-width)] p-0"
        align="start"
      >
        <Command shouldFilter={false}>
          <CommandInput
            placeholder="Search for a peak..."
            value={searchQuery}
            onValueChange={setSearchQuery}
          />
          <CommandList>
            {error && (
              <CommandEmpty>
                An error occurred while fetching peaks. Please try again.
              </CommandEmpty>
            )}

            {!error && !isLoading && peaksWithDistance.length === 0 && (
              <CommandEmpty>No peaks found matching your search.</CommandEmpty>
            )}

            {!error &&
              isLoading &&
              Array.from({ length: 4 }).map((_, index) => (
                <PeakListItemSkeleton
                  key={`skeleton-${index}`}
                  className="w-full"
                >
                  <div className="ml-auto size-4"></div>
                </PeakListItemSkeleton>
              ))}

            {peaksWithDistance.length > 0 && (
              <CommandGroup heading="Nearby peaks">
                {peaksWithDistance.map((peakWithDistance) => (
                  <CommandItem
                    key={peakWithDistance.peak.id}
                    value={peakWithDistance.peak.name}
                    onSelect={() => handleSelect(peakWithDistance)}
                    className="cursor-pointer p-0"
                  >
                    <PeakListItem
                      peakWithDistance={peakWithDistance}
                      className="w-full"
                    >
                      <Check
                        className={cn(
                          "text-primary ml-auto size-4",
                          selectedPeakWithDistance?.peak.id ===
                            peakWithDistance.peak.id
                            ? "opacity-100"
                            : "opacity-0",
                        )}
                      />
                    </PeakListItem>
                  </CommandItem>
                ))}
              </CommandGroup>
            )}
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
