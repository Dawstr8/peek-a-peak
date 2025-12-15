import type { Peak } from "@/lib/peaks/types";
import { WeatherRecord } from "@/lib/weather/types";

export interface SummitPhoto {
  id?: string;

  peakId?: string;
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
  id: string;
  lat?: number;
  lng?: number;
  alt?: number;
}

export interface SummitPhotoDate {
  id: string;
  capturedAt: string;
}

export interface SummitPhotoCreate {
  capturedAt: string;
  lat?: number;
  lng?: number;
  alt?: number;
  peakId?: string;
}

export enum PhotoDetailsKeys {
  ALTITUDE = "altitude",
}
