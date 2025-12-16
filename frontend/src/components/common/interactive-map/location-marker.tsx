import { Marker, Popup } from "react-leaflet";

import { DetailType } from "@/lib/common/types";
import { Location } from "@/lib/common/types";
import { formatByType } from "@/lib/common/utils";

interface LocationMarkerProps {
  location: Location;
  text?: string;
}

export function LocationMarker({ location, text }: LocationMarkerProps) {
  return (
    <Marker position={location}>
      <Popup>
        {text && (
          <>
            <strong>{text}</strong>
            <br />
          </>
        )}
        Latitude: {formatByType(DetailType.COORDINATE, location.lat)}
        <br />
        Longitude: {formatByType(DetailType.COORDINATE, location.lng)}
        <br />
        Altitude: {formatByType(DetailType.DISTANCE, location.alt)}
      </Popup>
    </Marker>
  );
}
