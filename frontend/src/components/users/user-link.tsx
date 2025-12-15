import Link from "next/link";

import { User } from "@/lib/users/types";
import { cn } from "@/lib/utils";

interface UserLinkProps {
  user: User;
  className?: string;
}

export function UserLink({ user, className }: UserLinkProps) {
  const { usernameDisplay } = user;

  return (
    <Link
      href={`/diary/${usernameDisplay}`}
      className={cn("cursor-pointer font-semibold", className)}
    >
      {usernameDisplay}
    </Link>
  );
}
