"use client";

import dynamic from "next/dynamic";

import { DialogTitle } from "@radix-ui/react-dialog";

import { DetailType } from "@/lib/common/types";
import { formatByType } from "@/lib/common/utils";

import { PeakItem } from "@/components/peaks/peak-item";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import { Separator } from "@/components/ui/separator";
import { UserLink } from "@/components/users/user-link";
import { WeatherConditionsList } from "@/components/weather/weather-conditions-list";

import { UPLOADS_BASE_URL } from "@/config/api";

import { PhotoAspectRatio } from "./photo-aspect-ratio";
import { useSummitPhotoDialog } from "./summit-photo-dialog-context";
import { SummitPhotoDialogDetailsList } from "./summit-photo-dialog/details-list";

const SummitPhotoMap = dynamic(
  () => import("./summit-photo-map").then((mod) => mod.SummitPhotoMap),
  { ssr: false },
);

export function SummitPhotoDialog() {
  const { isOpen, closeDialog, selectedPhoto } = useSummitPhotoDialog();

  return (
    <Dialog open={isOpen} onOpenChange={closeDialog}>
      <DialogContent className="max-h-[calc(90vh)] overflow-auto lg:!max-w-5xl">
        <DialogTitle className="sr-only">Summit Photo</DialogTitle>
        {selectedPhoto && (
          <div className="flex flex-col gap-6 lg:flex-row">
            <div className="flex-1">
              <PhotoAspectRatio
                src={`${UPLOADS_BASE_URL}${selectedPhoto.fileName}`}
                alt={`Summit photo ${selectedPhoto.id}`}
              />
            </div>
            <div className="flex-1 space-y-4 overflow-auto">
              <div className="flex items-center justify-between space-x-2">
                <UserLink user={selectedPhoto.owner} />
                <span className="text-muted-foreground text-xs">
                  added{" "}
                  {formatByType(
                    DetailType.DATE_DISTANCE,
                    selectedPhoto.createdAt,
                  )}
                </span>
              </div>
              <SummitPhotoDialogDetailsList
                className="flex flex-wrap gap-x-2 gap-y-4 divide-x text-sm"
                summitPhoto={selectedPhoto}
              />
              <Separator />
              <WeatherConditionsList
                className="flex items-center gap-1.5 text-xs"
                conditions={selectedPhoto.weatherRecord?.conditions}
              />
              {selectedPhoto.lat && selectedPhoto.lng && (
                <SummitPhotoMap summitPhoto={selectedPhoto} />
              )}
              {selectedPhoto.peak && <PeakItem peak={selectedPhoto.peak} />}
            </div>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
