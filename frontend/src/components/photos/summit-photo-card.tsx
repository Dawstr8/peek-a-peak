"use client";

import { formatDistance } from "date-fns";
import { ArrowUp, MapPin, Mountain } from "lucide-react";

import { DefaultDetailsFormatter } from "@/lib/common/formatter";
import { DetailType } from "@/lib/common/types";
import type { SummitPhoto } from "@/lib/photos/types";

import { PhotoAspectRatio } from "@/components/photos/photo-aspect-ratio";
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
  formatter: DefaultDetailsFormatter;
  className?: string;
  uploadsBaseUrl?: string;
}

export function SummitPhotoCard({
  summitPhoto,
  formatter,
  className,
  uploadsBaseUrl = UPLOADS_BASE_URL,
}: SummitPhotoCardProps) {
  const { lat, lng, alt } = summitPhoto;

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>#{summitPhoto.id}</CardTitle>
        <CardDescription>
          {summitPhoto.capturedAt &&
            formatDistance(new Date(summitPhoto.capturedAt), new Date(), {
              addSuffix: true,
            })}
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-4">
        <PhotoAspectRatio
          src={`${uploadsBaseUrl}${summitPhoto.fileName}`}
          alt={`Summit photo ${summitPhoto.id}`}
        />
        {alt && (
          <Item className="p-0">
            <ItemMedia>
              <ArrowUp />
            </ItemMedia>
            <ItemContent>
              <ItemTitle className="font-mono text-base">
                {formatter.formatByType(DetailType.HEIGHT, alt)}
              </ItemTitle>
            </ItemContent>
          </Item>
        )}
        {lat && lng && (
          <Item className="p-0">
            <ItemMedia>
              <MapPin />
            </ItemMedia>
            <ItemContent>
              <ItemTitle className="font-mono text-base">
                {formatter.formatByType(DetailType.COORDINATE, lat)},{" "}
                {formatter.formatByType(DetailType.COORDINATE, lng)}
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
                <span>{summitPhoto.peak.mountainRange.name}</span>
                <span>
                  {formatter.formatByType(
                    DetailType.HEIGHT,
                    summitPhoto.peak.elevation,
                  )}
                </span>
              </ItemDescription>
            </ItemContent>
          </Item>
        )}
      </CardContent>
    </Card>
  );
}
