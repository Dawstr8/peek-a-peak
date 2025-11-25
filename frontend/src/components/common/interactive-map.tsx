"use client";

import { useEffect, useMemo } from "react";

import { LatLng } from "leaflet";
import "leaflet/dist/leaflet.css";
import {
  MapContainer,
  Marker,
  Polyline,
  Popup,
  TileLayer,
  useMapEvents,
} from "react-leaflet";

import {
  MAP_CONFIG,
  createPeakIcon,
  initializeLeafletIcons,
} from "@/lib/leaflet";
import { Peak } from "@/lib/peaks/types";
import { photoDetailsFormatter } from "@/lib/photos/formatter";
import { cn } from "@/lib/utils";

import { FitToLocations } from "./fit-to-locations";

const { DEFAULT_CENTER, DEFAULT_ZOOM, DEFAULT_WIDE_ZOOM, DEFAULT_HEIGHT } =
  MAP_CONFIG;

function LocationClickHandler({
  onLocationSelect,
}: {
  onLocationSelect?: (location: LatLng) => void;
}) {
  useMapEvents({
    click: (e) => onLocationSelect?.(e.latlng),
  });

  return null;
}

interface InteractiveMapProps {
  location?: LatLng;
  onLocationSelect?: (location: LatLng) => void;
  targetLocation: LatLng;
  peaks: Peak[];
  zoom?: number;
  height?: string;
  className?: string;
  clickable?: boolean;
}

export function InteractiveMap({
  location,
  onLocationSelect,
  targetLocation,
  peaks = [],
  zoom = location ? DEFAULT_ZOOM : DEFAULT_WIDE_ZOOM,
  height = DEFAULT_HEIGHT,
  className = "",
  clickable = false,
}: InteractiveMapProps) {
  const mapCenter = location || DEFAULT_CENTER;

  const locations = useMemo(() => {
    const locs = [];
    if (location) locs.push(location);
    if (targetLocation) locs.push(targetLocation);

    return locs;
  }, [location, targetLocation]);

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

        <FitToLocations locations={locations} />

        {clickable && (
          <LocationClickHandler onLocationSelect={onLocationSelect} />
        )}

        {location && (
          <Marker position={location}>
            <Popup>
              <strong>Selected location</strong>
              <br />
              Latitude: {photoDetailsFormatter.formatLat(location.lat)}
              <br />
              Longitude: {photoDetailsFormatter.formatLng(location.lng)}
              <br />
              Altitude: {photoDetailsFormatter.formatAlt(location.alt)}
            </Popup>
          </Marker>
        )}

        {peaks.map((peak) => (
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
        ))}

        {location && targetLocation && (
          <Polyline
            positions={[location, targetLocation]}
            pathOptions={{
              dashArray: "1 8",
            }}
          />
        )}
      </MapContainer>
    </div>
  );
}
