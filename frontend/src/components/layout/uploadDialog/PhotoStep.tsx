"use client";

import { useMutation } from "@tanstack/react-query";
import { Upload } from "lucide-react";
import { useDropzone } from "react-dropzone";

import { exifMetadataExtractor } from "@/lib/metadata/extractor";
import type { PhotoMetadata } from "@/lib/metadata/types";
import type { SummitPhotoCreate } from "@/lib/photos/types";
import { cn } from "@/lib/utils";

import { MessageBlock } from "@/components/common/MessageBlock";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";

interface PhotoStepProps {
  onAccept: (summitPhotoCreate: SummitPhotoCreate, file: File) => void;
}

export function PhotoStep({ onAccept }: PhotoStepProps) {
  const { mutate, isPending } = useMutation({
    mutationFn: (file: File) => exifMetadataExtractor.extract(file),
    onSuccess: (metadata: PhotoMetadata, file: File) => {
      onAccept({ ...metadata }, file);
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
