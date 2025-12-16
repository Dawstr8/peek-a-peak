import { Camera } from "lucide-react";

import {
  EmptyDescription,
  EmptyHeader,
  EmptyMedia,
  EmptyTitle,
  Empty as EmptyUI,
} from "@/components/ui/empty";

export function Empty() {
  return (
    <EmptyUI>
      <EmptyHeader>
        <EmptyMedia variant="icon">
          <Camera />
        </EmptyMedia>
        <EmptyTitle>No memories added yet</EmptyTitle>
        <EmptyDescription>
          Memories from this user&apos;s hikes will appear here once they start
          sharing them.
        </EmptyDescription>
      </EmptyHeader>
    </EmptyUI>
  );
}
