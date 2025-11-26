"use client";

import { useAuth } from "@/components/auth/auth-context";

import SummitPhotosMap from "./components/summit-photos-map";
import SummitProgress from "./components/summit-progress";

export default function DiaryPage() {
  const { user } = useAuth();

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3">
      <SummitProgress user={user} />
      <div></div>
      <SummitPhotosMap user={user} className="row-span-2" />
    </div>
  );
}
