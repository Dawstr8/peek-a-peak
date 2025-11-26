"use client";

import { useMemo } from "react";

import { useQuery } from "@tanstack/react-query";

import { PeakClient } from "@/lib/peaks/client";
import { UsersClient } from "@/lib/users/client";
import { User } from "@/lib/users/types";

import CircularProgress from "@/components/common/circular-progress";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

interface SummitProgressProps {
  user?: User;
}

export default function SummitProgress({ user }: SummitProgressProps) {
  const { data: summitedByUserCount, isLoading: isSummitedByUserCountLoading } =
    useQuery({
      queryKey: ["users", user?.username, "peaks", "count"],
      queryFn: () => UsersClient.getSummitedPeaksCountByUser(user!.username),
      enabled: !!user,
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
