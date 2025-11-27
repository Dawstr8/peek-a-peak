"use client";

import { useMemo } from "react";

import { useInfiniteQuery } from "@tanstack/react-query";

import { photoDetailsFormatter } from "@/lib/photos/formatter";
import { UsersClient } from "@/lib/users/client";

import { useAuth } from "@/components/auth/auth-context";
import { InfiniteScroller } from "@/components/pagination/infinite-scroller";
import { SummitPhotosGrid } from "@/components/photos/summit-photos-grid";
import { Separator } from "@/components/ui/separator";
import { UserHeader } from "@/components/users/user-header";

export default function ProfilePage() {
  const { user, isLoading } = useAuth();

  const {
    data: paginatedSummitPhotos,
    isLoading: isLoadingSummitPhotos,
    isEnabled,
    isFetchingNextPage,
    fetchNextPage,
    hasNextPage,
  } = useInfiniteQuery({
    queryKey: ["users", user?.username, "photos", "uploadedAt", "desc"],
    queryFn: ({ pageParam = 1 }) => {
      const page =
        typeof pageParam === "number" ? pageParam : Number(pageParam) || 1;
      return UsersClient.getPhotosByUser(
        user!.username,
        "uploadedAt",
        "desc",
        page,
      );
    },
    initialPageParam: 1,
    getNextPageParam: (last) => last.nextPage,
    enabled: !!user,
  });

  const summitPhotos = useMemo(() => {
    return paginatedSummitPhotos?.pages.flatMap((page) => page.items);
  }, [paginatedSummitPhotos]);

  return (
    <div className="container mx-auto max-w-5xl space-y-8 py-8">
      <UserHeader user={user} isLoading={isLoading} showEmail />
      <Separator />
      <InfiniteScroller
        loadMore={fetchNextPage}
        isLoading={isFetchingNextPage}
        hasMore={hasNextPage}
      >
        <SummitPhotosGrid
          summitPhotos={summitPhotos}
          isLoading={!isEnabled || isLoadingSummitPhotos}
          formatter={photoDetailsFormatter}
        />
      </InfiniteScroller>
    </div>
  );
}
