import { UserX } from "lucide-react";

import {
  Empty,
  EmptyDescription,
  EmptyHeader,
  EmptyMedia,
  EmptyTitle,
} from "@/components/ui/empty";

export function UserNotFoundEmpty() {
  return (
    <Empty>
      <EmptyHeader>
        <EmptyMedia variant="icon">
          <UserX />
        </EmptyMedia>
        <EmptyTitle>User not found</EmptyTitle>
        <EmptyDescription>
          The user does not exist or has been removed.
        </EmptyDescription>
      </EmptyHeader>
    </Empty>
  );
}
