import { format } from "date-fns";

import { photoDetailsFormatter } from "@/lib/photos/formatter";
import { SummitPhoto } from "@/lib/photos/types";

import { SummitPhotoHoverableCard } from "@/components/photos/summit-photo-hoverable-card";

interface GroupProps {
  date: string;
  photos: SummitPhoto[];
}

export function Group({ date, photos }: GroupProps) {
  return (
    <div className="space-y-2">
      <div className="text-sm font-medium">{format(new Date(date), "PPP")}</div>
      <div className="grid grid-cols-2 gap-1 sm:grid-cols-3 xl:grid-cols-4 xl:gap-2">
        {photos.map((summitPhoto) => (
          <SummitPhotoHoverableCard
            key={summitPhoto.id}
            summitPhoto={summitPhoto}
            formatter={photoDetailsFormatter}
          />
        ))}
      </div>
    </div>
  );
}
