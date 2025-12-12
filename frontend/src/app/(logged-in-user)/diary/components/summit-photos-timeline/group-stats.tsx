import { useMemo } from "react";

import {
  ArrowUp,
  Mountain,
  Sunrise,
  Sunset,
  Thermometer,
  Wind,
} from "lucide-react";

import { DetailType } from "@/lib/common/types";
import { formatByType } from "@/lib/common/utils";
import { SummitPhoto } from "@/lib/photos/types";
import {
  countUniquePeaks,
  getAltitudes,
  getSunrises,
  getSunsets,
  getTemperatures,
  getWindSpeeds,
} from "@/lib/photos/utils";
import { cn } from "@/lib/utils";

import { StatsDisplay } from "@/components/common/stats-display";

const statsConfig = {
  temperatures: {
    icon: Thermometer,
    format: (temp: number) => formatByType(DetailType.TEMPERATURE, temp),
  },
  windSpeeds: {
    icon: Wind,
    format: (speed: number) => formatByType(DetailType.SPEED, speed),
  },
  altitudes: {
    icon: ArrowUp,
    format: (alt: number) => formatByType(DetailType.DISTANCE, alt),
  },
  sunrises: {
    icon: Sunrise,
    format: (sunrise: string) => formatByType(DetailType.TIME, sunrise),
  },
  sunsets: {
    icon: Sunset,
    format: (sunset: string) => formatByType(DetailType.TIME, sunset),
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
        temperatures: getTemperatures(photos),
        windSpeeds: getWindSpeeds(photos),
        altitudes: getAltitudes(photos),
        sunrises: getSunrises(photos),
        sunsets: getSunsets(photos),
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
