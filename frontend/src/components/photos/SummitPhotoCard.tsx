"use client";

import { formatDistance } from "date-fns";
import { ArrowUp, MapPin, Mountain } from "lucide-react";

import type { PhotoMetadataFormatter } from "@/lib/metadata/types";
import type { SummitPhoto } from "@/lib/photos/types";

import { PhotoAspectRatio } from "@/components/photos/PhotoAspectRatio";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Item,
  ItemContent,
  ItemDescription,
  ItemMedia,
  ItemTitle,
} from "@/components/ui/item";

import { UPLOADS_BASE_URL } from "@/config/api";

interface SummitPhotoCardProps {
  summitPhoto: SummitPhoto;
  formatter: PhotoMetadataFormatter;
  className?: string;
  uploadsBaseUrl?: string;
}

export function SummitPhotoCard({
  summitPhoto,
  formatter,
  className,
  uploadsBaseUrl = UPLOADS_BASE_URL,
}: SummitPhotoCardProps) {
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>#{summitPhoto.id}</CardTitle>
        <CardDescription>
          {summitPhoto.captured_at &&
            formatDistance(new Date(summitPhoto.captured_at), new Date(), {
              addSuffix: true,
            })}
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-4">
        <PhotoAspectRatio
          src={`${uploadsBaseUrl}${summitPhoto.file_name}`}
          alt={`Summit photo ${summitPhoto.id}`}
        />
        {summitPhoto.altitude && (
          <Item className="p-0">
            <ItemMedia>
              <ArrowUp />
            </ItemMedia>
            <ItemContent>
              <ItemTitle className="font-mono text-base">
                {formatter.formatAltitude(summitPhoto.altitude)}
              </ItemTitle>
            </ItemContent>
          </Item>
        )}
        {summitPhoto.latitude && summitPhoto.longitude && (
          <Item className="p-0">
            <ItemMedia>
              <MapPin />
            </ItemMedia>
            <ItemContent>
              <ItemTitle className="font-mono text-base">
                {formatter.formatLatitude(summitPhoto.latitude)},{" "}
                {formatter.formatLongitude(summitPhoto.longitude)}
              </ItemTitle>
            </ItemContent>
          </Item>
        )}
        {summitPhoto.peak && (
          <Item className="p-0">
            <ItemMedia>
              <Mountain />
            </ItemMedia>
            <ItemContent>
              <ItemTitle className="font-mono text-base">
                {summitPhoto.peak.name}
              </ItemTitle>
              <ItemDescription className="flex w-full justify-between">
                <span>{summitPhoto.peak.mountain_range.name}</span>
                <span>
                  {formatter.formatAltitude(summitPhoto.peak.elevation)}
                </span>
              </ItemDescription>
            </ItemContent>
          </Item>
        )}
      </CardContent>
    </Card>
  );
}
