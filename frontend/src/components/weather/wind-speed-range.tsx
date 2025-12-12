import { Wind } from "lucide-react";

import { Range } from "@/components/common/range";

interface WindSpeedRangeProps {
  windSpeeds: number[];
  className?: string;
}

export function WindSpeedRange({ windSpeeds, className }: WindSpeedRangeProps) {
  if (windSpeeds.length === 0) {
    return <></>;
  }

  const minWindSpeed = Math.min(...windSpeeds);
  const maxWindSpeed = Math.max(...windSpeeds);

  return (
    <Range
      className={className}
      icon={<Wind className="size-4" />}
      start={minWindSpeed.toFixed(1)}
      end={maxWindSpeed.toFixed(1)}
      suffix=" m/s"
    />
  );
}
