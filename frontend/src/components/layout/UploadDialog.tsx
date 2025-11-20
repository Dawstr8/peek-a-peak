"use client";

import { useState } from "react";

import { Check, Upload } from "lucide-react";

import type { Peak } from "@/lib/peaks/types";
import type { SummitPhotoCreate } from "@/lib/photos/types";

import { MessageBlock } from "@/components/common/MessageBlock";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

import { useStepper } from "@/hooks/use-stepper";

import { useUploadDialog } from "./UploadDialogContext";
import { PhotoStep } from "./uploadDialog/PhotoStep";
import { ReviewStep } from "./uploadDialog/ReviewStep";
import { UploadStep } from "./uploadDialog/UploadStep";

export default function UploadDialog() {
  const { isOpen, closeDialog } = useUploadDialog();

  const [file, setFile] = useState<File | null>(null);
  const [summitPhotoCreate, setSummitPhotoCreate] =
    useState<SummitPhotoCreate | null>(null);
  const [selectedPeak, setSelectedPeak] = useState<Peak | null>(null);
  const { step, next, back, reset } = useStepper(5);

  const resetDialogState = () => {
    setFile(null);
    setSummitPhotoCreate(null);
    setSelectedPeak(null);
    reset();
  };

  const handleOpenChange = () => {
    closeDialog();
    resetDialogState();
  };

  const renderStep = () => {
    switch (step) {
      case 0:
        return (
          <PhotoStep
            onAccept={(summitPhotoCreate: SummitPhotoCreate, file: File) => {
              setSummitPhotoCreate(summitPhotoCreate);
              setFile(file);
              next();
            }}
          />
        );
      case 1:
        return (
          <>
            {file && (
              <ReviewStep
                file={file}
                summitPhotoCreate={summitPhotoCreate!}
                onAccept={(
                  summitPhotoCreate: SummitPhotoCreate,
                  peak: Peak | null,
                ) => {
                  setSummitPhotoCreate(summitPhotoCreate);
                  setSelectedPeak(peak);
                  next();
                }}
                back={back}
              />
            )}
          </>
        );
      case 2:
        return (
          <>
            {file && summitPhotoCreate && (
              <UploadStep
                file={file}
                summitPhotoCreate={summitPhotoCreate}
                selectedPeak={selectedPeak}
                back={back}
                next={next}
              />
            )}
          </>
        );
      case 3:
        return (
          <MessageBlock
            iconComponent={Check}
            title="Upload Successful!"
            description="Your photo has been uploaded successfully."
            className="my-8"
          />
        );
      default:
        return null;
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={handleOpenChange}>
      <DialogContent className="px-0 lg:!max-w-5xl">
        <DialogHeader className="px-6">
          <DialogTitle className="flex items-center gap-2">
            <Upload className="size-6" />
            <span>Share Your Mountain Adventure</span>
          </DialogTitle>
        </DialogHeader>
        <div className="max-h-[calc(90vh-80px)] overflow-auto px-6">
          {renderStep()}
        </div>
      </DialogContent>
    </Dialog>
  );
}
