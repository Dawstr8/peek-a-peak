/**
 * API client for interacting with the photo endpoints
 */
import { ApiClient } from "@/lib/common/api-client";

import { API_ENDPOINTS } from "@/config/api";

import type { PeakWithDistance } from "./types";

/**
 * PeakClient class for handling peak-related API requests
 */
export class PeakClient extends ApiClient {
  /**
   * Find nearby peaks based on latitude and longitude
   * @param lat The latitude of the location
   * @param lng The longitude of the location
   * @param max_distance The maximum distance in meters to search for peaks (optional)
   * @param limit The maximum number of peaks to return (default is 5)
   * @param name_filter Optional substring to filter peak names (case-insensitive)
   * @returns A list of nearby peaks with their distances
   * @throws Error if the request fails
   */
  static async findNearbyPeaks(
    lat: number,
    lng: number,
    limit: number = 5,
    name_filter?: string,
    max_distance?: number,
  ): Promise<PeakWithDistance[]> {
    return this.get<PeakWithDistance[]>(
      API_ENDPOINTS.peaks.find(lat, lng, limit, name_filter, max_distance),
    );
  }
}
