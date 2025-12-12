import { useMemo } from "react";

import { getMinMax, getRangeDisplay } from "@/lib/utils";

import { Detail } from "./detail";

interface StatsDisplayProps<T> {
  stats: T[];
  suffix?: string;
  format?: (value: T) => string;
  icon?: React.ElementType;
  className?: string;
}

export function StatsDisplay<T>({
  stats,
  suffix,
  format,
  icon,
  className,
}: StatsDisplayProps<T>) {
  const { min, max } = useMemo(() => {
    const [minStat, maxStat] = getMinMax(stats);

    return {
      min: format && minStat !== undefined ? format(minStat) : minStat,
      max: format && maxStat !== undefined ? format(maxStat) : maxStat,
    };
  }, [stats, format]);

  if (stats.length === 0) {
    return null;
  }

  return (
    <Detail
      icon={icon}
      text={getRangeDisplay(min, max) + (suffix ?? "")}
      className={className}
    />
  );
}
