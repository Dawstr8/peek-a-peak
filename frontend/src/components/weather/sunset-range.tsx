import { Sunset } from "lucide-react";

import { TimeRange } from "./time-range";

interface SunsetRangeProps {
  sunsets: string[];
  className?: string;
}

export function SunsetRange({ sunsets, className }: SunsetRangeProps) {
  return (
    <TimeRange
      times={sunsets}
      icon={<Sunset className="size-4" />}
      className={className}
    />
  );
}
