"use client";

import { useQuery } from "@tanstack/react-query";

import { photoMetadataService } from "@/lib/metadata/service";
import { PhotoClient } from "@/lib/photos/client";

import { useAuth } from "@/components/auth/AuthContext";
import { SummitPhotosGrid } from "@/components/photos/SummitPhotosGrid";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import UserAvatar from "@/components/users/UserAvatar";

export default function ProfilePage() {
  const { user, isLoading } = useAuth();

  const summitPhotosQuery = useQuery({
    queryKey: ["photos", "user", user?.username],
    queryFn: () =>
      PhotoClient.getPhotosByUser(user!.username, "captured_at", "desc"),
    enabled: !!user,
  });

  return (
    <div className="container mx-auto max-w-5xl space-y-8 py-8">
      {isLoading && (
        <div className="flex items-center gap-12">
          <Skeleton className="size-32 rounded-full" />
          <div className="space-y-1.5 text-left text-sm leading-tight">
            <Skeleton className="h-6 w-48" />
            <Skeleton className="h-3 w-64" />
          </div>
        </div>
      )}
      {!isLoading && user && (
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-12">
            <UserAvatar user={user} className="size-32" />
            <div className="text-left text-sm leading-tight">
              <h2 className="text-2xl font-bold">{user.username}</h2>
              <p className="truncate text-xs">{user.email}</p>
            </div>
          </div>
        </div>
      )}
      <Separator />
      <SummitPhotosGrid
        summitPhotos={summitPhotosQuery.data}
        isLoading={!summitPhotosQuery.isEnabled || summitPhotosQuery.isLoading}
        formatter={photoMetadataService.getFormatter()}
      />
    </div>
  );
}
