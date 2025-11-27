import { format } from "date-fns";

import { SummitPhoto } from "./types";

export const groupPhotosByDate = (
  photos: SummitPhoto[],
): Map<string, SummitPhoto[]> => {
  const map = new Map<string, SummitPhoto[]>();

  photos.forEach((photo) => {
    if (!photo.capturedAt) return;

    const date = new Date(photo.capturedAt);
    const key = format(date, "yyyy-MM-dd");
    if (!map.has(key)) map.set(key, []);

    map.get(key)!.push(photo);
  });

  return map;
};
