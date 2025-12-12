import { useMemo } from "react";

import { format } from "date-fns/format";
import {
  ArrowUp,
  Mountain,
  Sunrise,
  Sunset,
  Thermometer,
  Wind,
} from "lucide-react";

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
    type: "number",
    icon: Thermometer,
    suffix: "°C",
    format: (temp: number) => temp.toFixed(1),
  },
  windSpeeds: {
    type: "number",
    icon: Wind,
    suffix: " m/s",
    format: (speed: number) => speed.toFixed(1),
  },
  altitudes: {
    type: "number",
    icon: ArrowUp,
    suffix: " m",
    format: (alt: number) => alt.toFixed(1),
  },
  sunrises: {
    type: "date",
    icon: Sunrise,
    suffix: undefined,
    format: (date: Date) => format(date, "HH:mm"),
  },
  sunsets: {
    type: "date",
    icon: Sunset,
    suffix: undefined,
    format: (date: Date) => format(date, "HH:mm"),
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
            suffix={config.suffix}
            icon={config.icon}
            className="pr-2"
          />
        );
      })}
    </div>
  );
}
