import { useMemo } from "react";

import { format } from "date-fns/format";

import { maxDate, minDate } from "@/lib/utils";

import { Range } from "@/components/common/range";

interface TimeRangeProps {
  times: string[];
  icon?: React.ReactNode;
  className?: string;
}

export function TimeRange({ times, icon, className }: TimeRangeProps) {
  const { minTime, maxTime } = useMemo(() => {
    const timesDates = times.map((s) => new Date(s));

    const minTime = minDate(timesDates);
    const maxTime = maxDate(timesDates);

    return { minTime, maxTime };
  }, [times]);

  if (times.length === 0) {
    return <></>;
  }

  return (
    <Range
      className={className}
      icon={icon}
      start={format(minTime, "HH:mm")}
      end={format(maxTime, "HH:mm")}
    />
  );
}
