import type { Peak } from "@/lib/peaks/types";
import type { User } from "@/lib/users/types";
import type { WeatherRecord } from "@/lib/weather/types";

export interface SummitPhoto {
  id?: string;

  ownerId: string;
  owner: User;

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
