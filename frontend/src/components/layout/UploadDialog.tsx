"use client";

import { useState } from "react";

import { Check, Upload } from "lucide-react";

import type { PhotoMetadata } from "@/lib/metadata/types";
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
import { MetadataStep } from "./uploadDialog/MetadataStep";
import { PeakStep } from "./uploadDialog/PeakStep";
import { SelectStep } from "./uploadDialog/SelectStep";
import { UploadStep } from "./uploadDialog/UploadStep";

export default function UploadDialog() {
  const { isOpen, closeDialog } = useUploadDialog();

  const [file, setFile] = useState<File | null>(null);
  const [metadata, setMetadata] = useState<PhotoMetadata>({});
  const [summitPhotoCreate, setSummitPhotoCreate] =
    useState<SummitPhotoCreate | null>(null);
  const [selectedPeak, setSelectedPeak] = useState<Peak | null>(null);
  const { step, next, back, reset, goTo } = useStepper(5);

  const resetDialogState = () => {
    setFile(null);
    setMetadata({});
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
          <SelectStep setFile={setFile} setMetadata={setMetadata} next={next} />
        );
      case 1:
        return (
          <MetadataStep
            metadata={metadata}
            setSummitPhotoCreate={setSummitPhotoCreate}
            back={back}
            next={next}
            goTo={goTo}
          />
        );
      case 2:
        return (
          <PeakStep
            summitPhotoCreate={summitPhotoCreate}
            setSummitPhotoCreate={setSummitPhotoCreate}
            setSelectedPeak={setSelectedPeak}
            back={back}
            next={next}
          />
        );
      case 3:
        return (
          <>
            {file && summitPhotoCreate && (
              <UploadStep
                file={file}
                summitPhotoCreate={summitPhotoCreate}
                selectedPeak={selectedPeak}
                back={() => {
                  if (!metadata.latitude || !metadata.longitude) {
                    goTo(1);
                  } else {
                    back();
                  }
                }}
                next={next}
              />
            )}
          </>
        );
      case 4:
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
      <DialogContent className="max-w-5xl">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Upload className="h-6 w-6" />
            <span>Share Your Mountain Adventure</span>
          </DialogTitle>
        </DialogHeader>
        <div>{renderStep()}</div>
      </DialogContent>
    </Dialog>
  );
}
