import type { User } from "@/lib/users/types";
import { cn } from "@/lib/utils";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";

interface UserAvatarProps {
  user: User;
  className?: string;
}

export default function UserAvatar({ user, className }: UserAvatarProps) {
  const avatarInitial = user.username.charAt(0).toUpperCase();

  return (
    <Avatar className={cn(className, "rounded-lg")}>
      <AvatarFallback className="rounded-lg">{avatarInitial}</AvatarFallback>
    </Avatar>
  );
}
