import { useMapEvents } from "react-leaflet";

import { Location } from "@/lib/common/types";

export function MapLocationPicker({
  onLocationSelect,
}: {
  onLocationSelect?: (location: Location) => void;
}) {
  useMapEvents({
    click: (e) => onLocationSelect?.(e.latlng),
  });

  return null;
}
