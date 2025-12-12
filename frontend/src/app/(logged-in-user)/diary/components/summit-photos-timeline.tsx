import { useMemo } from "react";

import { useInfiniteQuery } from "@tanstack/react-query";

import { PaginatedResponse } from "@/lib/pagination/types";
import { SummitPhoto } from "@/lib/photos/types";
import { groupPhotosByDate } from "@/lib/photos/utils";
import { UsersClient } from "@/lib/users/client";
import { cn } from "@/lib/utils";

import { InfiniteScroller } from "@/components/pagination/infinite-scroller";

import { Empty } from "./summit-photos-timeline/empty";
import { Group } from "./summit-photos-timeline/group";
import { Skeleton } from "./summit-photos-timeline/skeleton";

interface SummitPhotosTimelineProps {
  username: string;
  className?: string;
}

export default function SummitPhotosTimeline({
  username,
  className,
}: SummitPhotosTimelineProps) {
  const {
    data: paginatedSummitPhotos,
    isLoading,
    isFetchingNextPage,
    fetchNextPage,
    hasNextPage,
  } = useInfiniteQuery<PaginatedResponse<SummitPhoto>>({
    queryKey: ["users", username, "photos", "capturedAt", "desc"],
    queryFn: ({ pageParam = 1 }) => {
      const page =
        typeof pageParam === "number" ? pageParam : Number(pageParam) || 1;
      return UsersClient.getPhotosByUser(username, "capturedAt", "desc", page);
    },
    initialPageParam: 1,
    getNextPageParam: (last) => last.nextPage,
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
    <div className={cn("space-y-8", className)}>
      {isLoading && <Skeleton />}
      {summitPhotosGrouped && (
        <>
          {summitPhotosGrouped.size === 0 && <Empty username={username} />}
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
