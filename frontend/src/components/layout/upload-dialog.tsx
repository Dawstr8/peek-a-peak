"use client";

import { useState } from "react";

import { zodResolver } from "@hookform/resolvers/zod";
import { Camera, Check } from "lucide-react";
import { FormProvider, useForm } from "react-hook-form";
import z from "zod";

import type { Peak } from "@/lib/peaks/types";

import { MessageBlock } from "@/components/common/message-block";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

import { useStepper } from "@/hooks/use-stepper";

import { useUploadDialog } from "./upload-dialog-context";
import { PhotoStep } from "./upload-dialog/photo-step";
import { ReviewStep } from "./upload-dialog/review-step";
import { UploadStep } from "./upload-dialog/upload-step";

const uploadPhotoSchema = z.object({
  file: z.instanceof(File).refine((file) => file.size > 0, {
    message: "Photo file is required",
  }),
  capturedAt: z.iso.datetime("Captured date and time is required"),
  lat: z.number().optional(),
  lng: z.number().optional(),
  alt: z.number().optional(),
  peakId: z.string().optional(),
});

export type UploadPhotoFormData = z.infer<typeof uploadPhotoSchema>;

export default function UploadDialog() {
  const { isOpen, closeDialog } = useUploadDialog();

  const form = useForm<UploadPhotoFormData>({
    resolver: zodResolver(uploadPhotoSchema),
    defaultValues: {
      file: undefined,
      capturedAt: undefined,
      lat: undefined,
      lng: undefined,
      alt: undefined,
      peakId: undefined,
    },
  });

  const [peakToDisplay, setPeakToDisplay] = useState<Peak | null>(null);
  const { step, next, back, reset } = useStepper(5);

  const resetDialogState = () => {
    form.reset();
    setPeakToDisplay(null);
    reset();
  };

  const handleOpenChange = () => {
    closeDialog();
    resetDialogState();
  };

  return (
    <Dialog open={isOpen} onOpenChange={handleOpenChange}>
      <DialogContent className="px-0 lg:!max-w-5xl">
        <DialogHeader className="px-6">
          <DialogTitle className="flex items-center gap-2">
            <Camera className="size-6" />
            <span>Add new memory</span>
          </DialogTitle>
        </DialogHeader>
        <div className="max-h-[calc(90vh-80px)] overflow-auto px-6">
          <FormProvider {...form}>
            {step === 0 && <PhotoStep next={next} />}
            {step === 1 && (
              <ReviewStep
                setPeakToDisplay={setPeakToDisplay}
                back={back}
                next={next}
              />
            )}
            {step === 2 && (
              <UploadStep
                peakToDisplay={peakToDisplay}
                back={back}
                next={next}
              />
            )}
            {step === 3 && (
              <MessageBlock
                iconComponent={Check}
                title="Upload Successful!"
                description="Your photo has been uploaded successfully."
                className="my-8"
              />
            )}
          </FormProvider>
        </div>
      </DialogContent>
    </Dialog>
  );
}
