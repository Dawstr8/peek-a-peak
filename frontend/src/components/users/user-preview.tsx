import type { User } from "@/lib/users/types";
import { cn } from "@/lib/utils";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";

interface UserPreviewProps {
  user: User;
  className?: string;
  children?: React.ReactNode;
}

export default function UserPreview({
  user,
  className,
  children,
}: UserPreviewProps) {
  const avatarInitial = user.usernameDisplay.charAt(0);

  return (
    <>
      <Avatar className={cn(className, "rounded-lg")}>
        <AvatarFallback className="rounded-lg">{avatarInitial}</AvatarFallback>
      </Avatar>
      <div className="grid flex-1 text-left text-sm leading-tight">
        <span className="truncate font-medium">{user.usernameDisplay}</span>
        {children}
      </div>
    </>
  );
}
