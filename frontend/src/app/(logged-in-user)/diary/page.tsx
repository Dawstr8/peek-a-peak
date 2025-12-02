"use client";

import { useQuery } from "@tanstack/react-query";

import { UsersClient } from "@/lib/users/client";

import { useAuth } from "@/components/auth/auth-context";
import { UserHeader } from "@/components/users/user-header";

import SummitPhotosHeatmap from "./components/summit-photos-heatmap";
import SummitPhotosMap from "./components/summit-photos-map";
import SummitPhotosTimeline from "./components/summit-photos-timeline";
import SummitProgress from "./components/summit-progress";

export default function DiaryPage() {
  const { user: currentUser } = useAuth();
  const username = currentUser?.username || undefined;

  const { data: user, isLoading } = useQuery({
    queryKey: ["users", username],
    queryFn: () => UsersClient.getUser(username!),
    enabled: !!username,
  });

  return (
    <div className="flex flex-col gap-8 lg:flex-row">
      <div className="flex-2 space-y-6">
        <UserHeader user={user} isLoading={isLoading} />
        <SummitPhotosTimeline username={username} />
      </div>

      <div className="flex-1 space-y-4">
        <SummitProgress username={username} />
        <SummitPhotosHeatmap username={username} />
        <SummitPhotosMap username={username} />
      </div>
    </div>
  );
}
