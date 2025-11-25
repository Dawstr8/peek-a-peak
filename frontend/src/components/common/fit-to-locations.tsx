import { useEffect } from "react";

import { LatLng, LatLngBounds } from "leaflet";
import { useMap } from "react-leaflet";

import { MAP_CONFIG } from "@/lib/leaflet";

const { DEFAULT_CENTER, DEFAULT_ZOOM, DEFAULT_WIDE_ZOOM } = MAP_CONFIG;

export function FitToLocations({ locations }: { locations?: LatLng[] }) {
  const map = useMap();

  useEffect(() => {
    if (!locations || locations.length === 0) {
      map.setView(DEFAULT_CENTER, DEFAULT_WIDE_ZOOM);
      return;
    }

    const bounds = new LatLngBounds(locations);
    const center = bounds.getCenter();
    const zoom = Math.min(map.getBoundsZoom(bounds, false), DEFAULT_ZOOM);

    map.setView(center, zoom);
    return;
  }, [map, locations]);

  return null;
}
