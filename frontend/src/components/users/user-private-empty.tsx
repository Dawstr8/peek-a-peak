import { Lock } from "lucide-react";

import {
  Empty,
  EmptyDescription,
  EmptyHeader,
  EmptyMedia,
  EmptyTitle,
} from "@/components/ui/empty";

export function UserPrivateEmpty() {
  return (
    <Empty>
      <EmptyHeader>
        <EmptyMedia variant="icon">
          <Lock />
        </EmptyMedia>
        <EmptyTitle>Private profile</EmptyTitle>
        <EmptyDescription>
          This user&apos;s diary is private and cannot be viewed.
        </EmptyDescription>
      </EmptyHeader>
    </Empty>
  );
}
