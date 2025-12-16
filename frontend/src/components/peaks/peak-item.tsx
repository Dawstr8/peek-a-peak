import { Mountain } from "lucide-react";

import { DetailType } from "@/lib/common/types";
import { formatByType } from "@/lib/common/utils";
import { Peak } from "@/lib/peaks/types";

interface PeakItemProps {
  peak: Peak;
}

export function PeakItem({ peak }: PeakItemProps) {
  return (
    <div className="flex items-center gap-2">
      <Mountain className="size-4 shrink-0" />
      <div className="flex-1 space-y-1 overflow-hidden">
        <div className="truncate text-sm font-semibold">{peak.name}</div>
        <div className="flex items-center justify-between gap-2 text-xs opacity-90">
          <span className="truncate">{peak.mountainRange.name}</span>
          <span className="shrink-0">
            {formatByType(DetailType.DISTANCE, peak.elevation)}
          </span>
        </div>
      </div>
    </div>
  );
}
