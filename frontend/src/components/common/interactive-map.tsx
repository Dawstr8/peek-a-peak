"use client";

import { useEffect } from "react";

import "leaflet/dist/leaflet.css";
import { MapContainer, TileLayer } from "react-leaflet";

import { Location } from "@/lib/common/types";
import { MAP_CONFIG, initializeLeafletIcons } from "@/lib/leaflet";
import { cn } from "@/lib/utils";

import { FitToLocations } from "./interactive-map/fit-to-locations";
import { LocationMarker } from "./interactive-map/location-marker";
import { MarkerClusterLayer } from "./interactive-map/marker-cluster-layer";

const { DEFAULT_HEIGHT } = MAP_CONFIG;

interface InteractiveMapProps {
  locations?: Location[];
  hideLocationMarkers?: boolean;
  cluster?: boolean;
  height?: string;
  className?: string;
  children?: React.ReactNode;
}

export function InteractiveMap({
  locations = [],
  hideLocationMarkers = false,
  cluster = false,
  height = DEFAULT_HEIGHT,
  className = "",
  children,
}: InteractiveMapProps) {
  useEffect(() => {
    initializeLeafletIcons();
  }, []);

  return (
    <div
      className={cn(
        "border-border relative z-0 overflow-hidden rounded-lg border",
        className,
      )}
    >
      <MapContainer style={{ height, width: "100%" }} zoomControl={true}>
        <TileLayer
          attribution={MAP_CONFIG.TILE_LAYER_ATTRIBUTION}
          url={MAP_CONFIG.TILE_LAYER_URL}
        />

        <FitToLocations locations={locations} />

        {!hideLocationMarkers &&
          (cluster ? (
            <MarkerClusterLayer locations={locations} />
          ) : (
            locations.map((value, index) => (
              <LocationMarker key={index} location={value} />
            ))
          ))}

        {children}
      </MapContainer>
    </div>
  );
}
