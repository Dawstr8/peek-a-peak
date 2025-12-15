import { useMemo } from "react";

import {
  ArrowUp,
  Mountain,
  Sunrise,
  Sunset,
  Thermometer,
  Wind,
} from "lucide-react";

import { photoDetailsFormatter } from "@/lib/photos/formatter";
import { PhotoDetailsKeys, SummitPhoto } from "@/lib/photos/types";
import {
  countUniquePeaks,
  getAltitudes,
  getSunrises,
  getSunsets,
  getTemperatures,
  getWindSpeeds,
} from "@/lib/photos/utils";
import { cn } from "@/lib/utils";
import { weatherRecordDetailsFormatter } from "@/lib/weather/formatter";
import { WeatherRecordDetailsKeys } from "@/lib/weather/types";

import { StatsDisplay } from "@/components/common/stats-display";

const statsConfig = {
  [WeatherRecordDetailsKeys.TEMPERATURE]: {
    icon: Thermometer,
    format: (temp: number) =>
      weatherRecordDetailsFormatter.formatByKey(
        WeatherRecordDetailsKeys.TEMPERATURE,
        temp,
      ),
  },
  [WeatherRecordDetailsKeys.WIND_SPEED]: {
    icon: Wind,
    format: (speed: number) =>
      weatherRecordDetailsFormatter.formatByKey(
        WeatherRecordDetailsKeys.WIND_SPEED,
        speed,
      ),
  },
  [PhotoDetailsKeys.ALTITUDE]: {
    icon: ArrowUp,
    format: (alt: number) =>
      photoDetailsFormatter.formatByKey(PhotoDetailsKeys.ALTITUDE, alt),
  },
  [WeatherRecordDetailsKeys.SUNRISE]: {
    icon: Sunrise,
    format: (sunrise: string) =>
      weatherRecordDetailsFormatter.formatByKey(
        WeatherRecordDetailsKeys.SUNRISE,
        sunrise,
      ),
  },
  [WeatherRecordDetailsKeys.SUNSET]: {
    icon: Sunset,
    format: (sunset: string) =>
      weatherRecordDetailsFormatter.formatByKey(
        WeatherRecordDetailsKeys.SUNRISE,
        sunset,
      ),
  },
};
interface GroupStatsProps {
  photos: SummitPhoto[];
  className?: string;
}

export function GroupStats({ photos, className }: GroupStatsProps) {
  const { peaksCount, stats } = useMemo(() => {
    return {
      peaksCount: countUniquePeaks(photos),
      stats: {
        [WeatherRecordDetailsKeys.TEMPERATURE]: getTemperatures(photos),
        [WeatherRecordDetailsKeys.WIND_SPEED]: getWindSpeeds(photos),
        [PhotoDetailsKeys.ALTITUDE]: getAltitudes(photos),
        [WeatherRecordDetailsKeys.SUNRISE]: getSunrises(photos),
        [WeatherRecordDetailsKeys.SUNSET]: getSunsets(photos),
      },
    };
  }, [photos]);

  return (
    <div className={cn("flex items-center gap-2 divide-x", className)}>
      {peaksCount > 0 && (
        <div className="flex items-center space-x-1 pr-2">
          <Mountain className="size-4" />
          <span>
            {peaksCount} summit{peaksCount > 1 ? "s" : ""}
          </span>
        </div>
      )}

      {Object.entries(stats).map(([key, values]) => {
        const config = statsConfig[key as keyof typeof statsConfig];

        return (
          <StatsDisplay
            key={key}
            stats={values}
            format={config.format as (value: (typeof values)[number]) => string}
            icon={config.icon}
            className="pr-2"
          />
        );
      })}
    </div>
  );
}
