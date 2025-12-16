import { Marker, Popup } from "react-leaflet";

import { DetailType } from "@/lib/common/types";
import { formatByType } from "@/lib/common/utils";
import { createPeakIcon } from "@/lib/leaflet";
import { Peak } from "@/lib/peaks/types";

interface PeakMarkerProps {
  peak: Peak;
}

export function PeakMarker({ peak }: PeakMarkerProps) {
  return (
    <Marker
      key={peak.id}
      position={{ lat: peak.lat, lng: peak.lng }}
      icon={createPeakIcon(18, "green")}
    >
      <Popup>
        <strong>{peak.name}</strong>
        <br />
        {formatByType(DetailType.DISTANCE, peak.elevation)}
      </Popup>
    </Marker>
  );
}
