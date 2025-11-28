"use client";

import { useMemo } from "react";

import { useQuery } from "@tanstack/react-query";
import { format } from "date-fns/format";

import { UsersClient } from "@/lib/users/client";
import { User } from "@/lib/users/types";

import { ActivityCalendar } from "@/components/common/activity-calendar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface SummitPhotosHeatmapProps {
  user?: User;
  className?: string;
}

export default function SummitPhotosHeatmap({
  user,
  className,
}: SummitPhotosHeatmapProps) {
  const { data: summitPhotosDates } = useQuery({
    queryKey: ["users", user?.username, "photos", "dates"],
    queryFn: () => UsersClient.getPhotosDatesByUser(user!.username),
    enabled: !!user,
  });

  const values = useMemo(() => {
    if (!summitPhotosDates) return [];

    const dateCountMap: Record<string, number> = {};
    summitPhotosDates.forEach((summitPhotoDate) => {
      if (!summitPhotoDate.capturedAt) return;

      const date = format(new Date(summitPhotoDate.capturedAt), "yyyy-MM-dd");
      dateCountMap[date] = (dateCountMap[date] || 0) + 1;
    });

    return Object.entries(dateCountMap).map(([date, count]) => ({
      date,
      count,
    }));
  }, [summitPhotosDates]);

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>
          {summitPhotosDates
            ? `${summitPhotosDates.length} photo${summitPhotosDates.length !== 1 ? "s" : ""} taken`
            : "Loading photos..."}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ActivityCalendar values={values} />
      </CardContent>
    </Card>
  );
}
