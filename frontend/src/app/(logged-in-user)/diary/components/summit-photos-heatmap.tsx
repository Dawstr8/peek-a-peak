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
  const { data: summitPhotos } = useQuery({
    queryKey: ["users", user?.username, "photos"],
    queryFn: () => UsersClient.getPhotosByUser(user!.username),
    enabled: !!user,
  });

  const values = useMemo(() => {
    if (!summitPhotos) return [];

    const dateCountMap: Record<string, number> = {};
    summitPhotos.forEach((photo) => {
      if (!photo.capturedAt) return;

      const date = format(new Date(photo.capturedAt), "yyyy-MM-dd");
      dateCountMap[date] = (dateCountMap[date] || 0) + 1;
    });

    return Object.entries(dateCountMap).map(([date, count]) => ({
      date,
      count,
    }));
  }, [summitPhotos]);

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>
          {summitPhotos
            ? `${summitPhotos.length} photo${summitPhotos.length !== 1 ? "s" : ""} taken`
            : "Loading photos..."}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ActivityCalendar values={values} />
      </CardContent>
    </Card>
  );
}
