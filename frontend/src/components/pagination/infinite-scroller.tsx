import { useEffect, useRef } from "react";

import { Spinner } from "../ui/spinner";

interface InfiniteScrollerProps {
  loadMore: () => void;
  isLoading: boolean;
  hasMore: boolean;
  rootMargin?: string;
  children: React.ReactNode;
}

export function InfiniteScroller({
  loadMore,
  hasMore,
  isLoading,
  children,
  rootMargin = "300px",
}: InfiniteScrollerProps) {
  const sentinelRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!hasMore) return;
    if (!sentinelRef.current) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !isLoading) loadMore();
      },
      { rootMargin },
    );

    const el = sentinelRef.current;
    observer.observe(el);

    return () => observer.unobserve(el);
  }, [hasMore, isLoading, loadMore, rootMargin]);

  return (
    <>
      {children}
      <div ref={sentinelRef} />
      {isLoading && <Spinner className="mx-auto size-6" />}
    </>
  );
}
