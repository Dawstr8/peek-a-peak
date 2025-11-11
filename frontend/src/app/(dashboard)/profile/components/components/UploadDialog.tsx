"use client";

import { useState } from "react";

import { Upload } from "lucide-react";

import type { PhotoMetadata } from "@/lib/metadata/types";
import type { Peak } from "@/lib/peaks/types";
import type { SummitPhotoCreate } from "@/lib/photos/types";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

import { useStepper } from "@/hooks/use-stepper";

import { MetadataStep } from "./MetadataStep";
import { PeakStep } from "./PeakStep";
import { SelectStep } from "./SelectStep";
import { UploadStep } from "./UploadStep";

interface UploadDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export default function UploadDialog({
  open,
  onOpenChange,
}: UploadDialogProps) {
  const [file, setFile] = useState<File | null>(null);
  const [metadata, setMetadata] = useState<PhotoMetadata>({});
  const [summitPhotoCreate, setSummitPhotoCreate] =
    useState<SummitPhotoCreate | null>(null);
  const [selectedPeak, setSelectedPeak] = useState<Peak | null>(null);
  const { step, next, back } = useStepper(4);

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
                back={back}
              />
            )}
          </>
        );
      default:
        return null;
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogTrigger asChild>
        <Button>
          <Upload className="size-4" />
          Upload Summit Photo
        </Button>
      </DialogTrigger>
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
