"use client";

import { useEffect } from "react";

import { LatLng, LatLngBounds } from "leaflet";
import "leaflet/dist/leaflet.css";
import {
  MapContainer,
  Marker,
  Polyline,
  Popup,
  TileLayer,
  useMap,
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

const KRAKOW: LatLng = new LatLng(50.06143, 19.93658);

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

function FitToLocationsUpdater({
  location,
  targetLocation,
}: {
  location?: LatLng;
  targetLocation?: LatLng;
}) {
  const map = useMap();

  useEffect(() => {
    try {
      if (location && targetLocation) {
        const avgLat = (location.lat + targetLocation.lat) / 2;
        const avgLng = (location.lng + targetLocation.lng) / 2;
        const center = new LatLng(avgLat, avgLng);

        const bounds = new LatLngBounds([
          new LatLng(location.lat, location.lng),
          new LatLng(targetLocation.lat, targetLocation.lng),
        ]);

        const rawZoom = map.getBoundsZoom(bounds, false);
        const maxZoom = 18;
        const zoom = Math.min(rawZoom, maxZoom);

        map.setView(center, zoom);
        return;
      }

      if (location) {
        map.setView(location, MAP_CONFIG.DEFAULT_ZOOM);
        return;
      }

      if (targetLocation) {
        map.setView(targetLocation, MAP_CONFIG.DEFAULT_ZOOM);
        return;
      }

      map.setView(KRAKOW, MAP_CONFIG.DEFAULT_WIDE_ZOOM);
    } catch {}
  }, [map, location, targetLocation]);

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
  zoom = location ? MAP_CONFIG.DEFAULT_ZOOM : MAP_CONFIG.DEFAULT_WIDE_ZOOM,
  height = MAP_CONFIG.DEFAULT_HEIGHT,
  className = "",
  clickable = false,
}: InteractiveMapProps) {
  const mapCenter = location || KRAKOW;

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

        <FitToLocationsUpdater
          location={location}
          targetLocation={targetLocation}
        />

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
