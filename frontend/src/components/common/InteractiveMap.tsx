"use client";

import { useEffect } from "react";

import { LatLng } from "leaflet";
import "leaflet/dist/leaflet.css";
import {
  MapContainer,
  Marker,
  Popup,
  TileLayer,
  useMap,
  useMapEvents,
} from "react-leaflet";

import { MAP_CONFIG, initializeLeafletIcons } from "@/lib/leaflet";
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

function MapCenterUpdater({ center }: { center: LatLng }) {
  const map = useMap();

  useEffect(() => {
    map.setView(center);
  }, [map, center]);

  return null;
}

function ZoomUpdater({ location }: { location?: LatLng }) {
  const map = useMap();

  useEffect(() => {
    if (!location) {
      map.setZoom(MAP_CONFIG.DEFAULT_WIDE_ZOOM);
    }
  }, [map, location]);

  return null;
}

interface InteractiveMapProps {
  location?: LatLng;
  onLocationSelect?: (location: LatLng) => void;
  zoom?: number;
  height?: string;
  className?: string;
  clickable?: boolean;
}

export function InteractiveMap({
  location,
  onLocationSelect,
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

        <MapCenterUpdater center={mapCenter} />
        <ZoomUpdater location={location} />

        {clickable && (
          <LocationClickHandler onLocationSelect={onLocationSelect} />
        )}

        {location && (
          <Marker position={location}>
            <Popup>
              Selected location:
              <br />
              Latitude: {photoDetailsFormatter.formatLat(location.lat)}
              <br />
              Longitude: {photoDetailsFormatter.formatLng(location.lng)}
              <br />
              Altitude: {photoDetailsFormatter.formatAlt(location.alt)}
            </Popup>
          </Marker>
        )}
      </MapContainer>
    </div>
  );
}
