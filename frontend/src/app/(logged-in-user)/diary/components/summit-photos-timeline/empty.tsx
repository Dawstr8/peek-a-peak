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

import { useAuthenticatedUser } from "@/hooks/use-authenticated-user";

interface EmptyProps {
  username: string;
}

export function Empty({ username }: EmptyProps) {
  const { openDialog } = useUploadDialog();
  const user = useAuthenticatedUser();

  const isOwnDiary = user?.username === username;

  return (
    <EmptyUI>
      <EmptyHeader>
        <EmptyMedia variant="icon">
          <Camera />
        </EmptyMedia>
        <EmptyTitle>No photos uploaded yet.</EmptyTitle>
        <EmptyDescription>
          {isOwnDiary ? "Your" : "This user's"} summit photo timeline is empty.
        </EmptyDescription>
      </EmptyHeader>
      {isOwnDiary && (
        <EmptyContent>
          <Button onClick={openDialog}>
            <Plus />
            Add your first trip
          </Button>
        </EmptyContent>
      )}
    </EmptyUI>
  );
}
