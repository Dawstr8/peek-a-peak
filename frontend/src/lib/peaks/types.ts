import { MountainRange } from "@/lib/mountain-ranges/types";

export interface Peak {
  id: string;
  name: string;
  elevation: number;
  lat: number;
  lng: number;

  mountainRange: MountainRange;
}

export interface PeakWithDistance {
  peak: Peak;
  distance?: number;
}
