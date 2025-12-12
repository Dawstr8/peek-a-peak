import { Sunrise } from "lucide-react";

import { TimeRange } from "./time-range";

interface SunriseRangeProps {
  sunrises: string[];
  className?: string;
}

export function SunriseRange({ sunrises, className }: SunriseRangeProps) {
  return (
    <TimeRange
      times={sunrises}
      icon={<Sunrise className="size-4" />}
      className={className}
    />
  );
}
