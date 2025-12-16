import { Polyline } from "react-leaflet/Polyline";

import { Location } from "@/lib/common/types";

interface LocationsLineProps {
  locations: Location[];
}

export function LocationsLine(props: LocationsLineProps) {
  const { locations } = props;

  return <Polyline positions={locations} pathOptions={{ dashArray: "1 8" }} />;
}
