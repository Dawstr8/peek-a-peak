"use client";

import {
  ArrowUp,
  Clock,
  Cloud,
  Droplets,
  Eye,
  Mountain,
  Sunrise,
  Sunset,
  Thermometer,
  Wind,
} from "lucide-react";

import { DetailType } from "@/lib/common/types";
import { formatByType } from "@/lib/common/utils";
import type { SummitPhoto } from "@/lib/photos/types";
import { cn } from "@/lib/utils";

import { Detail } from "@/components/common/detail";
import { WeatherConditionsList } from "@/components/weather/weather-conditions-list";

import { UPLOADS_BASE_URL } from "@/config/api";

import { PhotoAspectRatio } from "./photo-aspect-ratio";

interface SummitPhotoHoverableCardProps {
  summitPhoto: SummitPhoto;
  className?: string;
  uploadsBaseUrl?: string;
}

export function SummitPhotoHoverableCard({
  summitPhoto,
  className,
  uploadsBaseUrl = UPLOADS_BASE_URL,
}: SummitPhotoHoverableCardProps) {
  const { weatherRecord, peak } = summitPhoto;

  return (
    <PhotoAspectRatio
      className={cn("group", className)}
      src={`${uploadsBaseUrl}${summitPhoto.fileName}`}
      alt={`Summit photo ${summitPhoto.id}`}
    >
      <div className="absolute inset-0 hidden flex-col justify-between bg-gradient-to-t from-black/90 to-black/60 p-3 text-white group-hover:flex">
        <div>
          {peak && (
            <div className="flex items-start gap-2">
              <Mountain className="mt-0.5 size-4 shrink-0" />
              <div className="flex-1 overflow-hidden">
                <div className="truncate text-sm font-semibold">
                  {peak.name}
                </div>
                <div className="flex items-center justify-between gap-2 text-xs opacity-90">
                  <span className="truncate">{peak.mountainRange.name}</span>
                  <span className="shrink-0">
                    {formatByType(DetailType.DISTANCE, peak.elevation)}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="grid grid-cols-2 gap-2 text-sm">
          <Detail
            icon={Clock}
            text={formatByType(DetailType.TIME, summitPhoto.capturedAt)}
          />
          <Detail
            icon={ArrowUp}
            text={formatByType(DetailType.DISTANCE, summitPhoto?.alt)}
          />
          <Detail
            icon={Droplets}
            text={formatByType(DetailType.PERCENTAGE, weatherRecord?.humidity)}
          />
          <Detail
            icon={Cloud}
            text={formatByType(DetailType.PERCENTAGE, weatherRecord?.clouds)}
          />
          <Detail
            icon={Sunrise}
            text={formatByType(DetailType.TIME, weatherRecord?.sunrise)}
          />
          <Detail
            icon={Sunset}
            text={formatByType(DetailType.TIME, weatherRecord?.sunset)}
          />
          <Detail
            icon={Eye}
            text={formatByType(DetailType.DISTANCE, weatherRecord?.visibility)}
          />
        </div>

        <div className="space-y-2 text-sm">
          <Detail
            icon={Thermometer}
            text={`${formatByType(DetailType.TEMPERATURE, weatherRecord?.temp)} (feels like ${formatByType(DetailType.TEMPERATURE, weatherRecord?.feelsLike)})`}
            className="col-span-2"
          />
          <Detail
            icon={Wind}
            text={formatByType(DetailType.SPEED, weatherRecord?.windSpeed)}
            className="col-span-2"
          >
            {weatherRecord?.windDeg !== undefined &&
              weatherRecord?.windDeg !== null && (
                <ArrowUp
                  className="size-4"
                  style={{ transform: `rotate(${weatherRecord?.windDeg}deg)` }}
                />
              )}
          </Detail>
        </div>
        <WeatherConditionsList
          conditions={weatherRecord?.conditions}
          className="flex flex-wrap items-center gap-1.5 text-xs"
        />
      </div>
    </PhotoAspectRatio>
  );
}
