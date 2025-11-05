"use client";

import { useState } from "react";

import { Upload } from "lucide-react";

import type { PhotoMetadata } from "@/lib/metadata/types";
import type { Peak } from "@/lib/peaks/types";
import type { SummitPhotoCreate } from "@/lib/photos/types";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

import { useStepper } from "@/hooks/use-stepper";

import { MetadataStep } from "./components/MetadataStep";
import { PeakStep } from "./components/PeakStep";
import { SelectStep } from "./components/SelectStep";
import { UploadStep } from "./components/UploadStep";

export default function UploadPage() {
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
    <div className="container mx-auto py-10">
      <h1 className="text-primary mb-8 text-center text-3xl font-bold">
        Upload Summit Photo
      </h1>

      <Card className="border-border mx-auto max-w-3xl shadow-md">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Upload className="h-6 w-6" />
            <span>Share Your Mountain Adventure</span>
          </CardTitle>
        </CardHeader>
        <CardContent>{renderStep()}</CardContent>
      </Card>
    </div>
  );
}
