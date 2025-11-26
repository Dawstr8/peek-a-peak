"use client";

import { useMemo } from "react";

import { useQuery } from "@tanstack/react-query";

import { PeakClient } from "@/lib/peaks/client";

import CircularProgress from "@/components/common/circular-progress";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

export default function SummitProgress() {
  const { data: summitedByUserCount, isLoading: isSummitedByUserCountLoading } =
    useQuery({
      queryKey: ["peaks", "count", "me"],
      queryFn: () => PeakClient.getSummitedByUserCount(),
    });

  const { data: totalPeaks, isLoading: isPeaksCountLoading } = useQuery({
    queryKey: ["peaks", "count"],
    queryFn: () => PeakClient.getCount(),
  });

  const progress = useMemo(() => {
    if (!summitedByUserCount || !totalPeaks) return 0;

    return Math.round((summitedByUserCount / totalPeaks) * 100);
  }, [summitedByUserCount, totalPeaks]);

  const progressTitle = `${summitedByUserCount} / ${totalPeaks ?? 0}`;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Summits completed</CardTitle>
      </CardHeader>
      <CardContent>
        {isPeaksCountLoading || isSummitedByUserCountLoading ? (
          <Skeleton className="mx-auto size-32" />
        ) : (
          <CircularProgress value={progress} title={progressTitle} />
        )}
      </CardContent>
    </Card>
  );
}
