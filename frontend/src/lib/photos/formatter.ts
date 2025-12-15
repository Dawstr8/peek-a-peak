import { DefaultDetailsFormatter } from "@/lib/common/formatter";

import { PhotoDetailsKeys } from "./types";

export class DefaultPhotoDetailsFormatter extends DefaultDetailsFormatter {
  formatByKey(
    key: PhotoDetailsKeys,
    value: number | string | undefined,
  ): string {
    switch (key) {
      case PhotoDetailsKeys.ALTITUDE:
        return this.formatNumber(value as number | undefined, " m");

      default:
        return this.NOT_AVAILABLE;
    }
  }

  formatLat(lat?: number): string {
    return this.formatCoordinate(lat);
  }

  formatLng(lng?: number): string {
    return this.formatCoordinate(lng);
  }

  formatCapturedAt(capturedAt?: string): string {
    if (!capturedAt) return this.NOT_AVAILABLE;

    try {
      const date = new Date(capturedAt);
      return date.toLocaleString();
    } catch {
      return this.NOT_AVAILABLE;
    }
  }
}

export const photoDetailsFormatter = new DefaultPhotoDetailsFormatter();
