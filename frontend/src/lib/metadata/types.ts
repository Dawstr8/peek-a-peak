export interface PhotoMetadata {
  latitude?: number;
  longitude?: number;
  altitude?: number;
  capturedAt?: string; // ISO string
}

export interface PhotoMetadataExtractor {
  extract(file: File): Promise<PhotoMetadata>;
}
