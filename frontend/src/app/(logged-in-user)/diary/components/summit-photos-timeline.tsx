import { useMemo } from "react";

import { useInfiniteQuery } from "@tanstack/react-query";

import { PaginatedResponse } from "@/lib/pagination/types";
import { groupPhotosByDate } from "@/lib/photos/service";
import { SummitPhoto } from "@/lib/photos/types";
import { UsersClient } from "@/lib/users/client";
import { User } from "@/lib/users/types";
import { cn } from "@/lib/utils";

import { InfiniteScroller } from "@/components/pagination/infinite-scroller";

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
  const {
    data: paginatedSummitPhotos,
    isLoading,
    isFetchingNextPage,
    fetchNextPage,
    hasNextPage,
  } = useInfiniteQuery<PaginatedResponse<SummitPhoto>>({
    queryKey: ["users", user?.username, "photos", "capturedAt", "desc"],
    queryFn: ({ pageParam = 1 }) => {
      const page =
        typeof pageParam === "number" ? pageParam : Number(pageParam) || 1;
      return UsersClient.getPhotosByUser(
        user!.username,
        "capturedAt",
        "desc",
        page,
      );
    },
    initialPageParam: 1,
    getNextPageParam: (last) => last.nextPage,
    enabled: !!user,
  });

  const summitPhotosGrouped = useMemo<
    Map<string, SummitPhoto[]> | undefined
  >(() => {
    const allSummitPhotos = paginatedSummitPhotos?.pages.flatMap(
      (page) => page.items,
    );

    return allSummitPhotos ? groupPhotosByDate(allSummitPhotos) : undefined;
  }, [paginatedSummitPhotos]);

  return (
    <div className={cn("space-y-4", className)}>
      {isLoading && <Skeleton />}
      {summitPhotosGrouped && (
        <>
          {summitPhotosGrouped.size === 0 && <Empty />}
          <InfiniteScroller
            loadMore={fetchNextPage}
            isLoading={isFetchingNextPage}
            hasMore={hasNextPage}
          >
            {Array.from(summitPhotosGrouped).map(([date, photos]) => (
              <Group key={date} date={date} photos={photos} />
            ))}
          </InfiniteScroller>
        </>
      )}
    </div>
  );
}
