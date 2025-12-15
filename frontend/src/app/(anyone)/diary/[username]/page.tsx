"use client";

import { use } from "react";

import { useQuery } from "@tanstack/react-query";

import { UserAccessState } from "@/lib/authorization/types";
import { UsersClient } from "@/lib/users/client";

import { Spinner } from "@/components/ui/spinner";
import { UserHeader } from "@/components/users/user-header";
import { UserNotFoundEmpty } from "@/components/users/user-not-found-empty";
import { UserPrivateEmpty } from "@/components/users/user-private-empty";

import { useUserAccess } from "@/hooks/use-user-access";

import SummitPhotosHeatmap from "../components/summit-photos-heatmap";
import SummitPhotosMap from "../components/summit-photos-map";
import SummitPhotosTimeline from "../components/summit-photos-timeline";
import SummitProgress from "../components/summit-progress";

interface DiaryPageProps {
  params: Promise<{
    username: string;
  }>;
}

export default function DiaryPage({ params }: DiaryPageProps) {
  const { username } = use(params);
  const userAccessState = useUserAccess(username);

  const { data: user, isLoading } = useQuery({
    queryKey: ["users", username],
    queryFn: () => UsersClient.getUser(username),
    enabled: userAccessState !== UserAccessState.Loading,
  });

  if (userAccessState === UserAccessState.Loading) {
    return (
      <div className="absolute inset-0 flex items-center justify-center">
        <Spinner className="size-8" />
      </div>
    );
  }

  if (userAccessState === UserAccessState.UserNotFound) {
    return <UserNotFoundEmpty />;
  }

  return (
    <div className="flex flex-col gap-8 lg:flex-row">
      <div className="flex-2 space-y-6">
        <UserHeader user={user} isLoading={isLoading} />
        {userAccessState === UserAccessState.HasAccess ? (
          <SummitPhotosTimeline username={username} />
        ) : (
          <UserPrivateEmpty />
        )}
      </div>

      {userAccessState === UserAccessState.HasAccess && (
        <div className="flex-1 space-y-4">
          <SummitProgress username={username} />
          <SummitPhotosHeatmap username={username} />
          <SummitPhotosMap username={username} />
        </div>
      )}
    </div>
  );
}
