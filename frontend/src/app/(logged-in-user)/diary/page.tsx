"use client";

import { useAuth } from "@/components/auth/auth-context";
import { UserHeader } from "@/components/users/user-header";

import SummitPhotosHeatmap from "./components/summit-photos-heatmap";
import SummitPhotosMap from "./components/summit-photos-map";
import SummitProgress from "./components/summit-progress";

export default function DiaryPage() {
  const { user, isLoading } = useAuth();

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3">
      <div className="row-span-1 pb-4 sm:col-span-2">
        <UserHeader user={user} isLoading={isLoading} />
      </div>

      <SummitProgress user={user} />
      <div className="row-span-3 sm:col-span-2"></div>
      <SummitPhotosHeatmap user={user} />
      <SummitPhotosMap user={user} />
    </div>
  );
}
