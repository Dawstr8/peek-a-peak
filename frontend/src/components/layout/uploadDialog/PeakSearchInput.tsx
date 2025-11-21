"use client";

import { useCallback, useEffect, useState } from "react";

import { useQuery } from "@tanstack/react-query";
import { millisecondsInMinute } from "date-fns/constants";
import { Check, Mountain } from "lucide-react";

import { PeakClient } from "@/lib/peaks/client";
import type { Peak } from "@/lib/peaks/types";
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
  lat: number;
  lng: number;
  onSelect: (peakWithDistance: Peak | null) => void;
  limit?: number;
  disabled?: boolean;
}

export function PeakSearchInput({
  lat,
  lng,
  onSelect,
  limit = 8,
  disabled = false,
}: PeakSearchInputProps) {
  const [open, setOpen] = useState(false);
  const [selectedPeak, setSelectedPeak] = useState<Peak | null>(null);

  const [searchQuery, setSearchQuery] = useState("");
  const debouncedQuery = useDebounce(searchQuery);

  const {
    data: peaksWithDistance = [],
    isLoading,
    error,
  } = useQuery({
    queryKey: ["peak-search", lat, lng, debouncedQuery, limit],
    queryFn: () =>
      PeakClient.findNearbyPeaks(
        lat,
        lng,
        limit,
        debouncedQuery.trim() || undefined,
      ),
    enabled: !!lat && !!lng,
    staleTime: 5 * millisecondsInMinute,
  });

  useEffect(() => {
    if (disabled && open) {
      setOpen(false);
    }
  }, [disabled, open]);

  const handleSelect = useCallback(
    (peak: Peak) => {
      setOpen(false);

      if (selectedPeak?.id === peak.id) {
        setSelectedPeak(null);
        setSearchQuery("");
        onSelect(null);
        return;
      }

      setSelectedPeak(peak);
      setSearchQuery(peak.name);
      onSelect(peak);
    },
    [onSelect, selectedPeak],
  );

  const displayValue = selectedPeak ? selectedPeak.name : "";

  return (
    <Popover open={open} onOpenChange={setOpen} modal={true}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          disabled={disabled}
          className="w-full cursor-pointer justify-between"
        >
          <span className={cn(!displayValue && "text-muted-foreground")}>
            {displayValue || "Which peak is this?"}
          </span>
          <Mountain className="size-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent
        className="w-[var(--radix-popover-trigger-width)] p-0"
        align="start"
      >
        <Command shouldFilter={false}>
          <CommandInput
            placeholder="Search peaks..."
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
                    onSelect={() => handleSelect(peakWithDistance.peak)}
                    className="cursor-pointer p-0"
                  >
                    <PeakListItem
                      peakWithDistance={peakWithDistance}
                      className="w-full"
                    >
                      <Check
                        className={cn(
                          "text-primary ml-auto size-4",
                          selectedPeak?.id === peakWithDistance.peak.id
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
