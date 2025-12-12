import { Thermometer } from "lucide-react";

import { Range } from "@/components/common/range";

interface TemperatureRangeProps {
  temperatures: number[];
  className?: string;
}

export function TemperatureRange({
  temperatures,
  className,
}: TemperatureRangeProps) {
  if (temperatures.length === 0) {
    return <></>;
  }

  const minTemp = Math.min(...temperatures);
  const maxTemp = Math.max(...temperatures);

  return (
    <Range
      className={className}
      icon={<Thermometer className="size-4" />}
      start={minTemp.toFixed(1)}
      end={maxTemp.toFixed(1)}
      suffix="°C"
    />
  );
}
