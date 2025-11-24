import { MountainRange } from "@/lib/mountainRanges/types";

export interface Peak {
  id: number;
  name: string;
  elevation: number;
  lat: number;
  lng: number;

  mountainRange: MountainRange;
}

export interface PeakWithDistance {
  peak: Peak;
  distance: number;
}
