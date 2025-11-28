"use client";

import { useMutation } from "@tanstack/react-query";
import { Upload } from "lucide-react";
import { useDropzone } from "react-dropzone";
import { useFormContext } from "react-hook-form";

import { exifMetadataExtractor } from "@/lib/metadata/extractor";
import type { PhotoMetadata } from "@/lib/metadata/types";
import { cn } from "@/lib/utils";

import { MessageBlock } from "@/components/common/message-block";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";

import type { UploadPhotoFormData } from "../upload-dialog";

interface PhotoStepProps {
  next: () => void;
}

export function PhotoStep({ next }: PhotoStepProps) {
  const { setValue } = useFormContext<UploadPhotoFormData>();

  const { mutate, isPending } = useMutation<PhotoMetadata, unknown, File>({
    mutationFn: (file: File) => exifMetadataExtractor.extract(file),
    onSuccess: (metadata: PhotoMetadata, file: File) => {
      setValue("file", file);
      if (metadata.capturedAt) setValue("capturedAt", metadata.capturedAt);
      if (metadata.lat) setValue("lat", metadata.lat);
      if (metadata.lng) setValue("lng", metadata.lng);
      if (metadata.alt) setValue("alt", metadata.alt);

      next();
    },
  });

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: (acceptedFiles: File[]) => {
      const file = acceptedFiles[0];
      if (!file) return;

      mutate(file);
    },
    accept: { "image/*": [] },
    multiple: false,
    disabled: isPending,
  });

  return (
    <div
      {...getRootProps()}
      className={cn(
        "flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed p-12 transition-colors",
        isDragActive ? "border-primary bg-primary/10" : "border-border",
        isPending && "cursor-not-allowed opacity-50",
      )}
    >
      <MessageBlock
        iconComponent={Upload}
        title={
          isPending
            ? "Extracting metadata..."
            : "Drag and drop or click to upload"
        }
        description="Support for JPG, PNG files. Metadata will be extracted automatically."
        className="mb-4"
      />

      <Button disabled={isPending}>
        {isPending && <Spinner />}
        {isPending ? "Processing..." : "Select File"}
      </Button>
      <input {...getInputProps()} />
    </div>
  );
}
