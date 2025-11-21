import * as exifr from "exifr";

import type { PhotoMetadata, PhotoMetadataExtractor } from "./types";

class ExifMetadataExtractor implements PhotoMetadataExtractor {
  async extract(file: File): Promise<PhotoMetadata> {
    try {
      const exif = await exifr.parse(file, {
        gps: true,
        tiff: true,
        exif: true,
        ifd1: false,
      });

      return {
        lat: exif?.latitude,
        lng: exif?.longitude,
        alt: exif?.GPSAltitude,
        capturedAt: exif?.DateTimeOriginal
          ? new Date(exif.DateTimeOriginal).toISOString()
          : undefined,
      };
    } catch (error) {
      console.warn("Failed to extract EXIF metadata:", error);
      return {};
    }
  }
}

export const exifMetadataExtractor = new ExifMetadataExtractor();
