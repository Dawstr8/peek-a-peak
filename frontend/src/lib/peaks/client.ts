/**
 * API client for interacting with the photo endpoints
 */
import { ApiClient } from "@/lib/common/api-client";

import { API_ENDPOINTS } from "@/config/api";

import type { Peak, PeakWithDistance } from "./types";

/**
 * PeakClient class for handling peak-related API requests
 */
export class PeakClient extends ApiClient {
  static async getCount(): Promise<number> {
    return this.get<number>(API_ENDPOINTS.peaks.getCount);
  }

  static async searchPeaks(
    limit: number = 20,
    nameFilter?: string,
    sortBy?: string,
    order?: "asc" | "desc",
  ): Promise<Peak[]> {
    return this.get<Peak[]>(
      API_ENDPOINTS.peaks.search(limit, nameFilter, sortBy, order),
    );
  }

  static async findNearbyPeaks(
    lat: number,
    lng: number,
    limit: number = 5,
    nameFilter?: string,
    maxDistance?: number,
  ): Promise<PeakWithDistance[]> {
    return this.get<PeakWithDistance[]>(
      API_ENDPOINTS.peaks.nearby(lat, lng, limit, nameFilter, maxDistance),
    );
  }
}
