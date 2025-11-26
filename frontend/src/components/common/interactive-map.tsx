"use client";

import { useEffect } from "react";

import { LatLng } from "leaflet";
import "leaflet/dist/leaflet.css";
import { MapContainer, TileLayer } from "react-leaflet";

import { MAP_CONFIG, initializeLeafletIcons } from "@/lib/leaflet";
import { cn } from "@/lib/utils";

const { DEFAULT_CENTER, DEFAULT_ZOOM, DEFAULT_WIDE_ZOOM, DEFAULT_HEIGHT } =
  MAP_CONFIG;

interface InteractiveMapProps {
  location?: LatLng;
  zoom?: number;
  height?: string;
  className?: string;
  children?: React.ReactNode;
}

export function InteractiveMap({
  location,
  zoom = location ? DEFAULT_ZOOM : DEFAULT_WIDE_ZOOM,
  height = DEFAULT_HEIGHT,
  className = "",
  children,
}: InteractiveMapProps) {
  const mapCenter = location || DEFAULT_CENTER;

  useEffect(() => {
    initializeLeafletIcons();
  }, []);

  return (
    <div
      className={cn(
        "border-border overflow-hidden rounded-lg border",
        className,
      )}
    >
      <MapContainer
        center={mapCenter}
        zoom={zoom}
        style={{ height, width: "100%" }}
        zoomControl={true}
      >
        <TileLayer
          attribution={MAP_CONFIG.TILE_LAYER_ATTRIBUTION}
          url={MAP_CONFIG.TILE_LAYER_URL}
        />

        {children}
      </MapContainer>
    </div>
  );
}
