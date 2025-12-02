"use client";

import { ReactNode, useEffect } from "react";

import { redirect, usePathname } from "next/navigation";

import { useAuth } from "@/components/auth/auth-context";

import { Spinner } from "../ui/spinner";

interface RequireAuthProps {
  children: ReactNode;
}

export function RequireAuth({ children }: RequireAuthProps) {
  const pathname = usePathname();
  const { user, isLoading } = useAuth();

  useEffect(() => {
    if (isLoading || user) return;

    const searchParams = new URLSearchParams();
    searchParams.set("returnTo", pathname);
    redirect(`/login?${searchParams.toString()}`);
  }, [user, isLoading, pathname]);

  if (isLoading) {
    return (
      <div className="absolute inset-0 flex items-center justify-center">
        <Spinner className="size-8" />
      </div>
    );
  }

  return <>{children}</>;
}
