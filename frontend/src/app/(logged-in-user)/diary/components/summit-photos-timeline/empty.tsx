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

export function Empty() {
  const { openDialog } = useUploadDialog();

  return (
    <EmptyUI>
      <EmptyHeader>
        <EmptyMedia variant="icon">
          <Camera />
        </EmptyMedia>
        <EmptyTitle>No photos uploaded yet.</EmptyTitle>
        <EmptyDescription>
          Your summit photo timeline is empty.
        </EmptyDescription>
      </EmptyHeader>
      <EmptyContent>
        <Button onClick={openDialog}>
          <Plus />
          Add your first trip
        </Button>
      </EmptyContent>
    </EmptyUI>
  );
}
