import React, { useMemo, useRef } from "react";

import { format } from "date-fns";
import CalendarHeatmap from "react-calendar-heatmap";
import "react-calendar-heatmap/dist/styles.css";

import { Tooltip, TooltipContent, TooltipTrigger } from "../ui/tooltip";

interface ActivityCalendarProps {
  values: { date: string; count: number }[];
}

export function ActivityCalendar({ values }: ActivityCalendarProps) {
  const startDateRef = useRef<string | null>(null);

  if (!startDateRef.current) {
    const d = new Date();
    d.setMonth(d.getMonth() - 6);
    startDateRef.current = format(d, "yyyy-MM-dd");
  }

  const buckets = useMemo(() => {
    const counts = values.map((v) => v.count);
    const maxCount = Math.max(...counts, 0);

    const bucketSize = maxCount / 4;

    return [bucketSize, bucketSize * 2, bucketSize * 3, maxCount];
  }, [values]);

  return (
    <CalendarHeatmap
      values={values}
      startDate={startDateRef.current!}
      endDate={format(new Date(), "yyyy-MM-dd")}
      showWeekdayLabels
      classForValue={(value?: { date: string; count: number }) => {
        if (!value) return "color-empty";

        if (value.count <= buckets[0]) return "fill-primary/50";
        if (value.count <= buckets[1]) return "fill-primary/67";
        if (value.count <= buckets[2]) return "fill-primary/83";

        return "fill-primary";
      }}
      transformDayElement={(
        element: React.ReactElement,
        value: { date: string; count: number } | undefined,
        index: number,
      ) => {
        if (!value?.date) return element;

        return (
          <Tooltip key={index}>
            <TooltipTrigger asChild>
              <g>{element}</g>
            </TooltipTrigger>
            <TooltipContent side="top">
              {`${value.count} photo${value.count !== 1 ? "s" : ""} taken on ${format(new Date(value.date), "MMMM do")}`}
            </TooltipContent>
          </Tooltip>
        );
      }}
    />
  );
}
