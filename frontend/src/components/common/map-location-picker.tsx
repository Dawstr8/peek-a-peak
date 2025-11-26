import { LatLng } from "leaflet";
import { useMapEvents } from "react-leaflet";

export function MapLocationPicker({
  onLocationSelect,
}: {
  onLocationSelect?: (location: LatLng) => void;
}) {
  useMapEvents({
    click: (e) => onLocationSelect?.(e.latlng),
  });

  return null;
}
