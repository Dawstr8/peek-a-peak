"use client";

import {
  ArrowUp,
  Calendar,
  Clock,
  Cloud,
  Droplets,
  Eye,
  Sunrise,
  Sunset,
  Thermometer,
  Wind,
} from "lucide-react";

import { DetailType } from "@/lib/common/types";
import { formatByType } from "@/lib/common/utils";
import { SummitPhoto } from "@/lib/photos/types";

import { Detail } from "@/components/common/detail";

interface SummitPhotoDialogDetailsListProps {
  summitPhoto: SummitPhoto;
  className?: string;
}

export function SummitPhotoDialogDetailsList({
  summitPhoto,
  className,
}: SummitPhotoDialogDetailsListProps) {
  const { weatherRecord } = summitPhoto;

  return (
    <ul className={className}>
      <li>
        <Detail
          icon={Calendar}
          text={formatByType(DetailType.DATE_DISTANCE, summitPhoto.capturedAt)}
          className="pr-2"
        />
      </li>
      <li>
        <Detail
          icon={Clock}
          text={formatByType(DetailType.TIME, summitPhoto.capturedAt)}
          className="pr-2"
        />
      </li>
      <li>
        <Detail
          icon={Sunrise}
          text={formatByType(DetailType.TIME, weatherRecord?.sunrise)}
          className="pr-2"
        />
      </li>
      <li>
        <Detail
          icon={Sunset}
          text={formatByType(DetailType.TIME, weatherRecord?.sunset)}
          className="pr-2"
        />
      </li>
      <li>
        <Detail
          icon={Eye}
          text={formatByType(DetailType.DISTANCE, weatherRecord?.visibility)}
          className="pr-2"
        />
      </li>
      <li>
        <Detail
          icon={Droplets}
          text={formatByType(DetailType.PERCENTAGE, weatherRecord?.humidity)}
          className="pr-2"
        />
      </li>
      <li>
        <Detail
          icon={Cloud}
          text={formatByType(DetailType.PERCENTAGE, weatherRecord?.clouds)}
          className="pr-2"
        />
      </li>
      <li>
        <Detail
          icon={Thermometer}
          text={`${formatByType(DetailType.TEMPERATURE, weatherRecord?.temp)} (feels like ${formatByType(DetailType.TEMPERATURE, weatherRecord?.feelsLike)})`}
          className="pr-2"
        />
      </li>
      <li>
        <Detail
          icon={Wind}
          text={formatByType(DetailType.SPEED, weatherRecord?.windSpeed)}
          className="pr-2"
        >
          {weatherRecord?.windDeg !== undefined &&
            weatherRecord?.windDeg !== null && (
              <ArrowUp
                className="size-4"
                style={{
                  transform: `rotate(${weatherRecord?.windDeg}deg)`,
                }}
              />
            )}
        </Detail>
      </li>
    </ul>
  );
}
