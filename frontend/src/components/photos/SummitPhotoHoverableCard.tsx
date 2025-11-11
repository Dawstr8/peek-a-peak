"use client";

import Image from "next/image";

import { AspectRatio } from "@radix-ui/react-aspect-ratio";
import { ArrowUp, MapPin, Mountain } from "lucide-react";

import type { PhotoMetadataFormatter } from "@/lib/metadata/types";
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

interface SummitPhotoHoverableCardProps {
  summitPhoto: SummitPhoto;
  formatter: PhotoMetadataFormatter;
  className?: string;
  uploadsBaseUrl?: string;
}

export function SummitPhotoHoverableCard({
  summitPhoto,
  formatter,
  className,
  uploadsBaseUrl = UPLOADS_BASE_URL,
}: SummitPhotoHoverableCardProps) {
  return (
    <AspectRatio className={cn("group", className)} ratio={3 / 4}>
      <div className="relative h-full w-full">
        <Image
          src={`${uploadsBaseUrl}${summitPhoto.file_name}`}
          alt={`Summit photo ${summitPhoto.id}`}
          fill
          className="object-cover"
        />
      </div>
      <div className="text-background absolute inset-0 hidden flex-col justify-end space-y-4 bg-black/75 p-2 group-hover:flex">
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
              <ItemDescription className="text-background flex w-full justify-between">
                <span>{summitPhoto.peak.range}</span>
                <span>
                  {formatter.formatAltitude(summitPhoto.peak.elevation)}
                </span>
              </ItemDescription>
            </ItemContent>
          </Item>
        )}
      </div>
    </AspectRatio>
  );
}
