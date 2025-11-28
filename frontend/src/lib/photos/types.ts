import type { Peak } from "@/lib/peaks/types";

export interface SummitPhoto {
  id?: number;
  fileName: string;
  uploadedAt: string;
  capturedAt: string;
  lat?: number;
  lng?: number;
  alt?: number;
  peakId?: number;
  peak?: Peak;
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
