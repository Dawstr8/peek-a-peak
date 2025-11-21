/**
 * API configuration
 * Centralized place for all API URLs and configuration
 */

/**
 * Base API URL
 * @description This is the base URL for all API requests
 */
export const API_BASE_URL = "/api";

export const UPLOADS_BASE_URL = "/uploads/";

/**
 * API endpoints
 * @description These are the API endpoints used throughout the application
 */
export const API_ENDPOINTS = {
  auth: {
    login: `${API_BASE_URL}/auth/login`,
    register: `${API_BASE_URL}/auth/register`,
    me: `${API_BASE_URL}/auth/me`,
    logout: `${API_BASE_URL}/auth/logout`,
  },
  photos: {
    getAll: (
      sort_by: string | null = null,
      order: "asc" | "desc" | null = null,
    ) => {
      const params = new URLSearchParams();

      if (sort_by) {
        params.append("sort_by", sort_by);
      }

      if (order) {
        params.append("order", order);
      }

      return `${API_BASE_URL}/photos?${params.toString()}`;
    },
    getByUser: (
      username: string,
      sort_by: string | null = null,
      order: "asc" | "desc" | null = null,
    ) => {
      const params = new URLSearchParams();

      if (sort_by) {
        params.append("sort_by", sort_by);
      }

      if (order) {
        params.append("order", order);
      }

      return `${API_BASE_URL}/photos/user/${username}?${params.toString()}`;
    },
    post: `${API_BASE_URL}/photos`,
  },
  peaks: {
    find: (
      lat: number,
      lng: number,
      limit: number = 5,
      name_filter?: string,
      max_distance?: number,
    ) => {
      const params = new URLSearchParams({
        lat: lat.toString(),
        lng: lng.toString(),
        limit: limit.toString(),
      });

      if (max_distance !== undefined) {
        params.append("max_distance", max_distance.toString());
      }

      if (name_filter !== undefined && name_filter.trim() !== "") {
        params.append("name_filter", name_filter);
      }

      return `${API_BASE_URL}/peaks/find?${params.toString()}`;
    },
  },
} as const;
