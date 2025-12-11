import type { Peak } from "@/lib/peaks/types";
import { WeatherRecord } from "@/lib/weather/types";

export interface SummitPhoto {
  id?: number;

  peakId?: number;
  peak?: Peak;

  weatherRecord?: WeatherRecord;

  fileName: string;
  createdAt: string;
  capturedAt: string;
  lat?: number;
  lng?: number;
  alt?: number;
}

export interface SummitPhotoLocation {
  id: number;
  lat?: number;
  lng?: number;
  alt?: number;
}

export interface SummitPhotoDate {
  id: number;
  capturedAt: string;
}

export interface SummitPhotoCreate {
  capturedAt: string;
  lat?: number;
  lng?: number;
  alt?: number;
  peakId?: number;
}

export interface PhotoDetailsFormatter {
  formatLat(lat?: number): string;
  formatLng(lng?: number): string;
  formatAlt(alt?: number): string;
  formatCapturedAt(capturedAt: string): string;
}
