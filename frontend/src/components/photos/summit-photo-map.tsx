"use client";

import { useMemo } from "react";

import { Location } from "@/lib/common/types";
import { SummitPhoto } from "@/lib/photos/types";

import { InteractiveMap } from "@/components/common/interactive-map";
import { LocationMarker } from "@/components/common/interactive-map/location-marker";
import { LocationsLine } from "@/components/common/interactive-map/locations-line";
import { PeakMarker } from "@/components/peaks/peak-marker";

interface SummitPhotoMapProps {
  summitPhoto: SummitPhoto;
}

export function SummitPhotoMap({ summitPhoto }: SummitPhotoMapProps) {
  const { lat, lng, alt, peak } = summitPhoto;

  const locations = useMemo(() => {
    const locs: Location[] = [];
    if (lat && lng) locs.push({ lat, lng, alt });

    if (peak)
      locs.push({
        lat: peak.lat,
        lng: peak.lng,
        alt: peak.elevation,
      });

    return locs;
  }, [lat, lng, alt, peak]);

  return (
    <div className="rounded-lg">
      <InteractiveMap locations={locations} hideLocationMarkers>
        {lat && lng && (
          <LocationMarker
            location={{ lat, lng, alt }}
            text="Summit photo location"
          />
        )}
        {peak && <PeakMarker peak={peak} />}
        <LocationsLine locations={locations} />
      </InteractiveMap>
    </div>
  );
}
