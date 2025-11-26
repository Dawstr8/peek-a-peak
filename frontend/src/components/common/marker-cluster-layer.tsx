import { useEffect } from "react";

import L, { LatLng } from "leaflet";
import "leaflet.markercluster";
import "leaflet.markercluster/dist/MarkerCluster.Default.css";
import "leaflet.markercluster/dist/MarkerCluster.css";
import { useMap } from "react-leaflet";

export function MarkerClusterLayer({
  locations = [],
}: {
  locations?: LatLng[];
}) {
  const map = useMap();

  useEffect(() => {
    if (!map || locations.length === 0) return;

    const clusterGroup = new L.MarkerClusterGroup();

    locations.forEach((latlng) => {
      clusterGroup.addLayer(L.marker(latlng));
    });

    map.addLayer(clusterGroup);

    return () => {
      map.removeLayer(clusterGroup);
    };
  }, [map, locations]);

  return null;
}
