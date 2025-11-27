import { Skeleton as SkeletonUI } from "@/components/ui/skeleton";

const skeletonsGrouped = Array.from({ length: 3 }, () =>
  Array.from({ length: Math.ceil(Math.random() * 4) + 1 }),
);

export function Skeleton() {
  return (
    <>
      {skeletonsGrouped.map((group, i) => (
        <div key={`group_${i}`} className="space-y-2">
          <SkeletonUI className="h-5 w-32" />
          <div className="grid grid-cols-2 gap-1 sm:grid-cols-3 xl:grid-cols-4 xl:gap-2">
            {group.map((_, j) => (
              <SkeletonUI key={`skeleton_${i}_${j}`} className="aspect-3/4" />
            ))}
          </div>
        </div>
      ))}
    </>
  );
}
