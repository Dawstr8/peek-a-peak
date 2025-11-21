import type { Peak } from "@/lib/peaks/types";

export interface SummitPhoto {
  id?: number;
  file_name: string;
  uploaded_at: string;
  captured_at?: string;
  lat?: number;
  lng?: number;
  alt?: number;
  peak_id?: number;
  peak?: Peak;
}

export interface SummitPhotoCreate {
  captured_at?: string;
  lat?: number;
  lng?: number;
  alt?: number;
  peak_id?: number;
}

export interface PhotoDetailsFormatter {
  formatLat(lat?: number): string;
  formatLng(lng?: number): string;
  formatAlt(alt?: number): string;
  formatCapturedAt(capturedAt?: string): string;
}
