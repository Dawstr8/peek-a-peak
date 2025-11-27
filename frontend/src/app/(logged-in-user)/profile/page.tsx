"use client";

import { useQuery } from "@tanstack/react-query";

import { photoDetailsFormatter } from "@/lib/photos/formatter";
import { UsersClient } from "@/lib/users/client";

import { useAuth } from "@/components/auth/auth-context";
import { SummitPhotosGrid } from "@/components/photos/summit-photos-grid";
import { Separator } from "@/components/ui/separator";
import { UserHeader } from "@/components/users/user-header";

export default function ProfilePage() {
  const { user, isLoading } = useAuth();

  const summitPhotosQuery = useQuery({
    queryKey: ["users", user?.username, "photos", "capturedAt", "desc"],
    queryFn: () =>
      UsersClient.getPhotosByUser(user!.username, "capturedAt", "desc"),
    enabled: !!user,
  });

  return (
    <div className="container mx-auto max-w-5xl space-y-8 py-8">
      <UserHeader user={user} isLoading={isLoading} showEmail />
      <Separator />
      <SummitPhotosGrid
        summitPhotos={summitPhotosQuery.data}
        isLoading={!summitPhotosQuery.isEnabled || summitPhotosQuery.isLoading}
        formatter={photoDetailsFormatter}
      />
    </div>
  );
}
