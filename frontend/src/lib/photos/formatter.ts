import { PhotoDetailsFormatter } from "./types";

const NOT_AVAILABLE = "N/A";

class DefaultPhotoDetailsFormatter implements PhotoDetailsFormatter {
  formatLat(lat?: number): string {
    return this.formatCoordinate(lat);
  }

  formatLng(lng?: number): string {
    return this.formatCoordinate(lng);
  }

  formatAlt(alt?: number): string {
    if (alt === undefined || alt === null) return NOT_AVAILABLE;

    return `${alt.toFixed(1)}m`;
  }

  formatCapturedAt(capturedAt?: string): string {
    if (!capturedAt) return NOT_AVAILABLE;

    try {
      const date = new Date(capturedAt);
      return date.toLocaleString();
    } catch {
      return NOT_AVAILABLE;
    }
  }

  private formatCoordinate(value?: number): string {
    if (value === undefined || value === null) return NOT_AVAILABLE;

    return `${value.toFixed(6)}°`;
  }
}

export const photoDetailsFormatter = new DefaultPhotoDetailsFormatter();
