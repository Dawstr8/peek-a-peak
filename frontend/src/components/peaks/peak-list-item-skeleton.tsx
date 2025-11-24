"use client";

import { cn } from "@/lib/utils";

import { Skeleton } from "@/components/ui/skeleton";

interface PeakListItemSkeletonProps {
  className?: string;
  children?: React.ReactNode;
}

export function PeakListItemSkeleton({
  className,
  children,
}: PeakListItemSkeletonProps) {
  return (
    <div
      className={cn(
        "flex items-center gap-3 rounded-md p-3 text-left",
        className,
      )}
    >
      <Skeleton className="flex size-8 items-center justify-center rounded-full" />
      <div className="min-w-0 flex-1">
        <Skeleton className="mb-2 h-4 w-32" />
        <div className="flex items-center gap-4">
          <Skeleton className="h-3 w-16" />
          <Skeleton className="h-3 w-12" />
          <Skeleton className="h-5 w-20 rounded-full" />
        </div>
      </div>
      {children}
    </div>
  );
}
