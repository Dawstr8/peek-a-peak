"use client";

import { useMemo } from "react";

import Link from "next/link";

import { useInfiniteQuery } from "@tanstack/react-query";
import { Settings } from "lucide-react";

import { UsersClient } from "@/lib/users/client";

import { InfiniteScroller } from "@/components/pagination/infinite-scroller";
import { SummitPhotosGrid } from "@/components/photos/summit-photos-grid";
import { Separator } from "@/components/ui/separator";
import { UserHeader } from "@/components/users/user-header";

import { useAuthenticatedUser } from "@/hooks/use-authenticated-user";

export default function ProfilePage() {
  const user = useAuthenticatedUser();
  const { username } = user;

  const {
    data: paginatedSummitPhotos,
    isLoading: isLoadingSummitPhotos,
    isEnabled,
    isFetchingNextPage,
    fetchNextPage,
    hasNextPage,
  } = useInfiniteQuery({
    queryKey: ["users", username, "photos", "createdAt", "desc"],
    queryFn: ({ pageParam = 1 }) => {
      const page =
        typeof pageParam === "number" ? pageParam : Number(pageParam) || 1;
      return UsersClient.getPhotosByUser(username, "createdAt", "desc", page);
    },
    initialPageParam: 1,
    getNextPageParam: (last) => last.nextPage,
  });

  const summitPhotos = useMemo(() => {
    return paginatedSummitPhotos?.pages.flatMap((page) => page.items);
  }, [paginatedSummitPhotos]);

  return (
    <div className="container mx-auto max-w-5xl space-y-8 py-8">
      <UserHeader user={user} showEmail>
        <Link
          href="/settings"
          className="cursor-pointer opacity-75 hover:opacity-100"
        >
          <Settings className="size-8" />
        </Link>
      </UserHeader>
      <Separator />
      <InfiniteScroller
        loadMore={fetchNextPage}
        isLoading={isFetchingNextPage}
        hasMore={hasNextPage}
      >
        <SummitPhotosGrid
          summitPhotos={summitPhotos}
          isLoading={!isEnabled || isLoadingSummitPhotos}
        />
      </InfiniteScroller>
    </div>
  );
}
