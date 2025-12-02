"use client";

import { useQuery } from "@tanstack/react-query";

import { UserAccessState } from "@/lib/authorization/types";
import { ApiError } from "@/lib/common/types";
import { UsersClient } from "@/lib/users/client";

export function useUserAccess(username: string): UserAccessState {
  const { isLoading, error } = useQuery({
    queryKey: ["users", username, "access"],
    queryFn: () => UsersClient.checkUserAccess(username),
    retry: false,
  });

  const apiError = error as ApiError | null;

  if (isLoading) return UserAccessState.Loading;
  if (!apiError) return UserAccessState.HasAccess;
  if (apiError.status === 404) return UserAccessState.UserNotFound;
  if (apiError.status === 403) return UserAccessState.AccessUnauthorized;

  return UserAccessState.HasAccess;
}
