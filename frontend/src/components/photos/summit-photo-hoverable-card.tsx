"use client";

import { ArrowUp, MapPin, Mountain, Thermometer } from "lucide-react";

import { DefaultPhotoDetailsFormatter } from "@/lib/photos/formatter";
import { PhotoDetailsKeys } from "@/lib/photos/types";
import type { SummitPhoto } from "@/lib/photos/types";
import { cn } from "@/lib/utils";

import {
  Item,
  ItemContent,
  ItemDescription,
  ItemMedia,
  ItemTitle,
} from "@/components/ui/item";

import { UPLOADS_BASE_URL } from "@/config/api";

import { PhotoAspectRatio } from "./photo-aspect-ratio";

interface SummitPhotoHoverableCardProps {
  summitPhoto: SummitPhoto;
  formatter: DefaultPhotoDetailsFormatter;
  className?: string;
  uploadsBaseUrl?: string;
}

export function SummitPhotoHoverableCard({
  summitPhoto,
  formatter,
  className,
  uploadsBaseUrl = UPLOADS_BASE_URL,
}: SummitPhotoHoverableCardProps) {
  const { lat, lng, alt } = summitPhoto;

  return (
    <PhotoAspectRatio
      className={cn("group", className)}
      src={`${uploadsBaseUrl}${summitPhoto.fileName}`}
      alt={`Summit photo ${summitPhoto.id}`}
    >
      <div className="text-background absolute inset-0 hidden flex-col justify-end space-y-4 bg-black/75 p-2 group-hover:flex">
        {alt && (
          <Item className="p-0">
            <ItemMedia>
              <ArrowUp />
            </ItemMedia>
            <ItemContent>
              <ItemTitle className="font-mono text-base">
                {formatter.formatByKey(PhotoDetailsKeys.ALTITUDE, alt)}
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
                {formatter.formatLat(lat)}, {formatter.formatLng(lng)}
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
              <ItemDescription className="text-background flex w-full justify-between">
                <span>{summitPhoto.peak.mountainRange.name}</span>
                <span>
                  {formatter.formatByKey(
                    PhotoDetailsKeys.ALTITUDE,
                    summitPhoto.peak.elevation,
                  )}
                </span>
              </ItemDescription>
            </ItemContent>
          </Item>
        )}
        {summitPhoto.weatherRecord?.temp && (
          <Item className="p-0">
            <ItemMedia>
              <Thermometer />
            </ItemMedia>
            <ItemContent>
              <ItemTitle className="font-mono text-base">
                <span>{summitPhoto.weatherRecord.temp}°C</span>
              </ItemTitle>
            </ItemContent>
          </Item>
        )}
      </div>
    </PhotoAspectRatio>
  );
}
