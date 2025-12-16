"use client";

import { useState } from "react";

import { MoreVerticalIcon, TrashIcon } from "lucide-react";
import { toast } from "sonner";

import { PhotoClient } from "@/lib/photos/client";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

import { useSummitPhotoDialog } from "../summit-photo-dialog-context";

interface SettingsProps {
  photoId: string;
}

export function Settings({ photoId }: SettingsProps) {
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const { closeDialog: closeSummitPhotoDialog } = useSummitPhotoDialog();

  const handleDelete = async () => {
    try {
      await PhotoClient.deletePhoto(photoId);
      closeSummitPhotoDialog();
      toast.success("Photo deleted successfully");
    } catch {
      toast.error("Failed to delete photo");
    } finally {
      setIsDeleteDialogOpen(false);
    }
  };

  return (
    <>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="ghost" size="icon" className="size-8">
            <MoreVerticalIcon className="size-4" />
            <span className="sr-only">Photo settings</span>
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end">
          <DropdownMenuItem
            variant="destructive"
            onSelect={() => setIsDeleteDialogOpen(true)}
          >
            <TrashIcon />
            Delete photo
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>

      <Dialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Delete memory</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete this memory? This action cannot be
              undone.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <DialogClose asChild>
              <Button variant="outline">Cancel</Button>
            </DialogClose>
            <Button variant="destructive" onClick={handleDelete}>
              Delete
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
