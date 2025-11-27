"use client";

import { useAuth } from "@/components/auth/auth-context";
import { UserHeader } from "@/components/users/user-header";

import SummitPhotosHeatmap from "./components/summit-photos-heatmap";
import SummitPhotosMap from "./components/summit-photos-map";
import SummitPhotosTimeline from "./components/summit-photos-timeline";
import SummitProgress from "./components/summit-progress";

export default function DiaryPage() {
  const { user, isLoading } = useAuth();

  return (
    <div className="flex flex-col gap-8 lg:flex-row">
      <div className="flex-2 space-y-6">
        <UserHeader user={user} isLoading={isLoading} />
        <SummitPhotosTimeline user={user} />
      </div>

      <div className="flex-1 space-y-4">
        <SummitProgress user={user} />
        <SummitPhotosHeatmap user={user} />
        <SummitPhotosMap user={user} />
      </div>
    </div>
  );
}
