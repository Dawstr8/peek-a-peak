"use client";

import { LogOut } from "lucide-react";

import { AuthClient } from "@/lib/auth/client";
import { cn } from "@/lib/utils";

import { useAuth } from "@/components/auth/AuthContext";

export interface LogoutButtonProps {
  className?: string;
}

export default function LogoutButton({ className }: LogoutButtonProps) {
  const { logout } = useAuth();

  const handleSignOut = async () => {
    await AuthClient.logout();
    logout();
  };
  return (
    <button
      className={cn("flex items-center justify-center gap-2", className)}
      onClick={handleSignOut}
    >
      <LogOut className="h-4 w-4" />
      Sign Out
    </button>
  );
}
