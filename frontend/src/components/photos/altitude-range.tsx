import { ArrowUp } from "lucide-react";

import { Range } from "@/components/common/range";

interface AltitudeRangeProps {
  altitudes: number[];
  className?: string;
}

export function AltitudeRange({ altitudes, className }: AltitudeRangeProps) {
  if (altitudes.length === 0) {
    return <></>;
  }

  const minAlt = Math.min(...altitudes);
  const maxAlt = Math.max(...altitudes);

  return (
    <Range
      className={className}
      icon={<ArrowUp className="size-4" />}
      start={minAlt.toFixed(1)}
      end={maxAlt.toFixed(1)}
      suffix=" m"
    />
  );
}
