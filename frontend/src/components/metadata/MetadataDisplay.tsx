import { Camera, Clock, MapPin, Mountain } from "lucide-react";

import type {
  PhotoMetadata,
  PhotoMetadataFormatter,
} from "@/lib/metadata/types";

import { MetadataItem } from "@/components/metadata/MetadataItem";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface MetadataDisplayProps {
  metadata: PhotoMetadata;
  formatter: PhotoMetadataFormatter;
  className?: string;
}

export function MetadataDisplay({
  metadata,
  formatter,
  className,
}: MetadataDisplayProps) {
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Camera className="text-primary h-5 w-5" />
          Photo metadata
        </CardTitle>
      </CardHeader>
      <CardContent className="grid grid-cols-1 gap-3 md:grid-cols-2">
        <MetadataItem
          icon={<MapPin />}
          title="Latitude"
          description={formatter.formatLatitude(metadata.latitude)}
        />
        <MetadataItem
          icon={<MapPin />}
          title="Longitude"
          description={formatter.formatLongitude(metadata.longitude)}
        />
        <MetadataItem
          icon={<Mountain />}
          title="Altitude"
          description={formatter.formatAltitude(metadata.altitude)}
        />
        <MetadataItem
          icon={<Clock />}
          title="Captured"
          description={formatter.formatCapturedAt(metadata.capturedAt)}
        />
      </CardContent>
    </Card>
  );
}
