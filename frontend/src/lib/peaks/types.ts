import { MountainRange } from "@/lib/mountain_ranges/types";

export interface Peak {
  id: number;
  name: string;
  elevation: number;
  latitude: number;
  longitude: number;

  mountain_range: MountainRange;
}

export interface PeakWithDistance {
  peak: Peak;
  distance: number;
}
