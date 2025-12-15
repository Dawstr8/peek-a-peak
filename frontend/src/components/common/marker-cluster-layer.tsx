import { useEffect } from "react";

import L from "leaflet";
import "leaflet.markercluster";
import "leaflet.markercluster/dist/MarkerCluster.Default.css";
import "leaflet.markercluster/dist/MarkerCluster.css";
import { useMap } from "react-leaflet";

import { Location } from "@/lib/common/types";

export function MarkerClusterLayer({
  locations = [],
}: {
  locations?: Location[];
}) {
  const map = useMap();

  useEffect(() => {
    if (!map || locations.length === 0) return;

    const clusterGroup = new L.MarkerClusterGroup();

    locations.forEach((location) => {
      clusterGroup.addLayer(L.marker(location));
    });

    map.addLayer(clusterGroup);

    return () => {
      map.removeLayer(clusterGroup);
    };
  }, [map, locations]);

  return null;
}
