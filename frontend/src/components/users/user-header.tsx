"use client";

import React from "react";

import { useQuery } from "@tanstack/react-query";

import { UsersClient } from "@/lib/users/client";

import { Skeleton } from "@/components/ui/skeleton";
import UserAvatar from "@/components/users/user-avatar";

type UserHeaderProps = {
  username?: string;
  showEmail?: boolean;
  avatarClassName?: string;
  children?: React.ReactNode;
};

export function UserHeader({
  username,
  showEmail = false,
  avatarClassName = "size-32",
  children,
}: UserHeaderProps) {
  const { data: user, isLoading } = useQuery({
    queryKey: ["users", username],
    queryFn: () => UsersClient.getUser(username!),
    enabled: !!username,
  });

  const loading = isLoading || !user;

  return (
    <div className="flex items-center justify-between">
      {loading ? (
        <div className="flex items-center gap-12">
          <Skeleton className={`${avatarClassName} rounded-full`} />
          <div className="space-y-1.5 text-left text-sm leading-tight">
            <Skeleton className="h-6 w-48" />
            {showEmail && <Skeleton className="h-3 w-64" />}
          </div>
        </div>
      ) : (
        <>
          <div className="flex items-center gap-12">
            <UserAvatar user={user} className={avatarClassName} />
            <div className="text-left text-sm leading-tight">
              <h2 className="text-2xl font-bold">{user.usernameDisplay}</h2>
              {showEmail && <p className="truncate text-xs">{user.email}</p>}
            </div>
          </div>
          {children}
        </>
      )}
    </div>
  );
}
