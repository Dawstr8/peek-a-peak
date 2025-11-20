import type { Peak } from "@/lib/peaks/types";

export interface SummitPhoto {
  id?: number;
  file_name: string;
  uploaded_at: string;
  captured_at?: string;
  latitude?: number;
  longitude?: number;
  altitude?: number;
  peak_id?: number;
  peak?: Peak;
}

export interface SummitPhotoCreate {
  captured_at?: string;
  latitude?: number;
  longitude?: number;
  altitude?: number;
  peak_id?: number;
}

export interface PhotoDetailsFormatter {
  formatLatitude(latitude?: number): string;
  formatLongitude(longitude?: number): string;
  formatAltitude(altitude?: number): string;
  formatCapturedAt(capturedAt?: string): string;
}
