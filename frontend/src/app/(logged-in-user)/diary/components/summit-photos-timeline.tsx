import { useMemo } from "react";

import { useQuery } from "@tanstack/react-query";

import { groupPhotosByDate } from "@/lib/photos/service";
import { SummitPhoto } from "@/lib/photos/types";
import { UsersClient } from "@/lib/users/client";
import { User } from "@/lib/users/types";
import { cn } from "@/lib/utils";

import { Empty } from "./summit-photos-timeline/empty";
import { Group } from "./summit-photos-timeline/group";
import { Skeleton } from "./summit-photos-timeline/skeleton";

interface SummitPhotosTimelineProps {
  user?: User;
  className?: string;
}

export default function SummitPhotosTimeline({
  user,
  className,
}: SummitPhotosTimelineProps) {
  const { data: summitPhotos, isLoading } = useQuery<SummitPhoto[]>({
    queryKey: ["users", user?.username, "photos", "capturedAt", "desc"],
    queryFn: () =>
      UsersClient.getPhotosByUser(user!.username, "capturedAt", "desc"),
    enabled: !!user,
  });

  const summitPhotosGrouped = useMemo<
    Map<string, SummitPhoto[]> | undefined
  >(() => {
    return summitPhotos ? groupPhotosByDate(summitPhotos) : undefined;
  }, [summitPhotos]);

  return (
    <div className={cn("space-y-4", className)}>
      {isLoading && <Skeleton />}
      {summitPhotosGrouped && (
        <>
          {summitPhotosGrouped.size === 0 && <Empty />}
          {Array.from(summitPhotosGrouped).map(([date, photos]) => (
            <Group key={date} date={date} photos={photos} />
          ))}
        </>
      )}
    </div>
  );
}
