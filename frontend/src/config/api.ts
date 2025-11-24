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

export function buildUrl(
  path: string,
  params?: Record<string, string | number | boolean | null | undefined>,
) {
  const searchParams = new URLSearchParams();

  Object.entries(params || {}).forEach(([k, v]) => {
    if (v === undefined || v === null) return;

    searchParams.append(k, String(v));
  });

  const queryString = searchParams.toString();
  return `${API_BASE_URL}${path}${queryString ? `?${queryString}` : ""}`;
}

/**
 * API endpoints
 * @description These are the API endpoints used throughout the application
 */
export const API_ENDPOINTS = {
  auth: {
    login: buildUrl(`/auth/login`),
    register: buildUrl(`/auth/register`),
    me: buildUrl(`/auth/me`),
    logout: buildUrl(`/auth/logout`),
  },
  photos: {
    getAll: (
      sort_by: string | null = null,
      order: "asc" | "desc" | null = null,
    ) => buildUrl(`/photos`, { sort_by, order }),
    getByUser: (
      username: string,
      sort_by: string | null = null,
      order: "asc" | "desc" | null = null,
    ) => buildUrl(`/photos/user/${username}`, { sort_by, order }),
    post: buildUrl(`/photos`),
  },
  peaks: {
    find: (
      lat: number,
      lng: number,
      limit: number = 5,
      name_filter?: string,
      max_distance?: number,
    ) =>
      buildUrl(`/peaks/find`, {
        lat,
        lng,
        limit,
        name_filter,
        max_distance,
      }),
  },
} as const;
