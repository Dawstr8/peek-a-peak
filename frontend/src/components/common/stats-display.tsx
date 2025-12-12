import { useMemo } from "react";

import { cn, getMinMax, getRangeDisplay } from "@/lib/utils";

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
  icon: Icon,
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
    <div className={cn("flex items-center space-x-1", className)}>
      {Icon && <Icon className="size-4" />}
      <span>
        {getRangeDisplay(min, max)}
        {suffix}
      </span>
    </div>
  );
}
