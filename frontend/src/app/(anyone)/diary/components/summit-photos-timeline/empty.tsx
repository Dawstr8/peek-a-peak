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
        <EmptyTitle>No photos uploaded yet.</EmptyTitle>
        <EmptyDescription>
          This user&apos;s summit photo timeline is empty.
        </EmptyDescription>
      </EmptyHeader>
    </EmptyUI>
  );
}
