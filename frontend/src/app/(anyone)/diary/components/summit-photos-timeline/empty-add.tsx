import { Camera, Plus } from "lucide-react";

import { useUploadDialog } from "@/components/layout/upload-dialog-context";
import { Button } from "@/components/ui/button";
import {
  EmptyContent,
  EmptyDescription,
  EmptyHeader,
  EmptyMedia,
  EmptyTitle,
  Empty as EmptyUI,
} from "@/components/ui/empty";

export function EmptyAdd() {
  const { openDialog } = useUploadDialog();

  return (
    <EmptyUI>
      <EmptyHeader>
        <EmptyMedia variant="icon">
          <Camera />
        </EmptyMedia>
        <EmptyTitle>No memories added yet</EmptyTitle>
        <EmptyDescription>
          Memories from your hikes will appear here once you start sharing them.
        </EmptyDescription>
      </EmptyHeader>
      <EmptyContent>
        <Button onClick={openDialog}>
          <Plus />
          Add your first memory
        </Button>
      </EmptyContent>
    </EmptyUI>
  );
}
