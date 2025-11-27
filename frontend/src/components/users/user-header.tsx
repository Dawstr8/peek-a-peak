"use client";

import React from "react";

import { User } from "@/lib/users/types";

import { Skeleton } from "@/components/ui/skeleton";
import UserAvatar from "@/components/users/user-avatar";

type UserHeaderProps = {
  user?: User;
  isLoading?: boolean;
  showEmail?: boolean;
  avatarClassName?: string;
};

export function UserHeader({
  user,
  isLoading,
  showEmail = false,
  avatarClassName = "size-32",
}: UserHeaderProps) {
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
        <div className="flex items-center gap-12">
          <UserAvatar user={user} className={avatarClassName} />
          <div className="text-left text-sm leading-tight">
            <h2 className="text-2xl font-bold">{user.usernameDisplay}</h2>
            {showEmail && <p className="truncate text-xs">{user.email}</p>}
          </div>
        </div>
      )}
    </div>
  );
}
