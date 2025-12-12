import { useMemo } from "react";

import { Mountain } from "lucide-react";

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

import { AltitudeRange } from "@/components/photos/altitude-range";
import { SunriseRange } from "@/components/weather/sunrise-range";
import { SunsetRange } from "@/components/weather/sunset-range";
import { TemperatureRange } from "@/components/weather/temperature-range";
import { WindSpeedRange } from "@/components/weather/wind-speed-range";

interface GroupStatsProps {
  photos: SummitPhoto[];
  className?: string;
}

export function GroupStats({ photos, className }: GroupStatsProps) {
  const { peaksCount, temperatures, altitudes, sunrises, sunsets, windSpeeds } =
    useMemo(() => {
      return {
        peaksCount: countUniquePeaks(photos),
        temperatures: getTemperatures(photos),
        altitudes: getAltitudes(photos),
        sunrises: getSunrises(photos),
        sunsets: getSunsets(photos),
        windSpeeds: getWindSpeeds(photos),
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
      <TemperatureRange temperatures={temperatures} className="pr-2" />
      <WindSpeedRange windSpeeds={windSpeeds} className="pr-2" />
      <AltitudeRange altitudes={altitudes} className="pr-2" />
      <SunriseRange sunrises={sunrises} className="pr-2" />
      <SunsetRange sunsets={sunsets} className="pr-2" />
    </div>
  );
}
