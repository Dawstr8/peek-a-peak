"use client";

import { useAuth } from "@/components/auth/AuthContext";
import UserAvatar from "@/components/users/UserAvatar";

export default function ProfilePage() {
  const { user, isLoading } = useAuth();

  return (
    <div className="container max-w-5xl py-8">
      {!isLoading && user && (
        <div className="flex items-center gap-12">
          <UserAvatar user={user} className="size-32" />
          <div className="text-left text-sm leading-tight">
            <h2 className="text-2xl font-bold">{user.username}</h2>
            <p className="truncate text-xs">{user.email}</p>
          </div>
        </div>
      )}
    </div>
  );
}
