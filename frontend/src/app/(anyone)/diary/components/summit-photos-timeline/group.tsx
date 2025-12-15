import { format } from "date-fns";
import { Calendar } from "lucide-react";

import { SummitPhoto } from "@/lib/photos/types";

import { SummitPhotoHoverableCard } from "@/components/photos/summit-photo-hoverable-card";
import { Separator } from "@/components/ui/separator";

import { GroupStats } from "./group-stats";

interface GroupProps {
  date: string;
  photos: SummitPhoto[];
}

export function Group({ date, photos }: GroupProps) {
  return (
    <div className="space-y-2">
      <div className="flex items-center space-x-2">
        <Calendar />
        <time className="text-md font-medium" dateTime={date}>
          {format(new Date(date), "PPP")}
        </time>
      </div>
      <GroupStats className="flex-wrap text-sm" photos={photos} />
      <Separator />
      <div className="grid grid-cols-2 gap-1 sm:grid-cols-3 xl:grid-cols-4 xl:gap-2">
        {photos.map((summitPhoto) => (
          <SummitPhotoHoverableCard
            key={summitPhoto.id}
            summitPhoto={summitPhoto}
          />
        ))}
      </div>
    </div>
  );
}
