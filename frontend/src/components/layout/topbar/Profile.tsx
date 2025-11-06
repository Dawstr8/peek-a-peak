"use client";

import Link from "next/link";

import { ChevronDown, LogIn, User as UserIcon } from "lucide-react";

import type { User } from "@/lib/users/types";

import LogoutButton from "@/components/layout/LogoutButton";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

interface ProfileProps {
  user: User | null;
  className?: string;
}

export default function Profile({ user }: ProfileProps) {
  if (!user) {
    return (
      <Button asChild variant="outline">
        <Link href="/login">
          <LogIn className="h-4 w-4" />
          Sign In
        </Link>
      </Button>
    );
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="flex items-center gap-2">
          <UserIcon className="h-4 w-4" />
          <span className="text-sm">{user.username}</span>
          <ChevronDown className="h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem>
          <LogoutButton />
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
