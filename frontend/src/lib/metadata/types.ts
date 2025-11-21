export interface PhotoMetadata {
  lat?: number;
  lng?: number;
  alt?: number;
  capturedAt?: string; // ISO string
}

export interface PhotoMetadataExtractor {
  extract(file: File): Promise<PhotoMetadata>;
}
