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

export const countUniquePeaks = (photos: SummitPhoto[]): number => {
  const uniquePeaks = new Set<string>();
  photos.forEach((photo) => {
    if (photo.peakId) uniquePeaks.add(photo.peakId);
  });

  return uniquePeaks.size;
};

export const getTemperatures = (photos: SummitPhoto[]): number[] =>
  photos
    .map((photo) => photo.weatherRecord?.temp)
    .filter((temp) => temp != null);

export const getAltitudes = (photos: SummitPhoto[]): number[] =>
  photos.map((photo) => photo.alt).filter((alt) => alt != null);

export const getSunrises = (photos: SummitPhoto[]): string[] =>
  photos
    .map((photo) => photo.weatherRecord?.sunrise)
    .filter((sunrise) => sunrise != null);

export const getSunsets = (photos: SummitPhoto[]): string[] =>
  photos
    .map((photo) => photo.weatherRecord?.sunset)
    .filter((sunset) => sunset != null);

export const getWindSpeeds = (photos: SummitPhoto[]): number[] =>
  photos
    .map((photo) => photo.weatherRecord?.windSpeed)
    .filter((windSpeed) => windSpeed != null);
