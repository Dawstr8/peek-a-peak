import type { User } from "@/lib/users/types";
import { cn } from "@/lib/utils";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";

import { Skeleton } from "../ui/skeleton";

interface UserPreviewProps {
  user: User | null;
  className?: string;
  children?: React.ReactNode;
}

export default function UserPreview({
  user,
  className,
  children,
}: UserPreviewProps) {
  if (!user)
    return (
      <>
        <Skeleton className="size-8 rounded-full" />
        <div className="grid flex-1 text-left text-sm leading-tight">
          <Skeleton className="h-4 w-20 rounded-md" />
        </div>
      </>
    );

  const avatarInitial = user.username.charAt(0).toUpperCase();

  return (
    <>
      <Avatar className={cn(className, "rounded-lg")}>
        <AvatarFallback className="rounded-lg">{avatarInitial}</AvatarFallback>
      </Avatar>
      <div className="grid flex-1 text-left text-sm leading-tight">
        <span className="truncate font-medium">{user.username}</span>
        {children}
      </div>
    </>
  );
}
