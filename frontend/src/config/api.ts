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
      sortBy: string | null = null,
      order: "asc" | "desc" | null = null,
    ) => buildUrl(`/photos`, { sortBy, order }),
    post: buildUrl(`/photos`),
  },
  peaks: {
    getCount: buildUrl(`/peaks/count`),
    find: (
      lat: number,
      lng: number,
      limit: number = 5,
      nameFilter?: string,
      maxDistance?: number,
    ) =>
      buildUrl(`/peaks/find`, {
        lat,
        lng,
        limit,
        nameFilter,
        maxDistance,
      }),
  },
  users: {
    checkAccess: (username: string) => buildUrl(`/users/${username}/access`),
    getUser: (username: string) => buildUrl(`/users/${username}`),
    updateUser: (username: string) => buildUrl(`/users/${username}`),
    getPhotosByUser: (
      username: string,
      sortBy: string | null = null,
      order: "asc" | "desc" | null = null,
      page: number | null = null,
      perPage: number | null = null,
    ) =>
      buildUrl(`/users/${username}/photos`, { sortBy, order, page, perPage }),
    getPhotosLocationsByUser: (username: string) =>
      buildUrl(`/users/${username}/photos/locations`),
    getPhotosDatesByUser: (username: string) =>
      buildUrl(`/users/${username}/photos/dates`),
    getSummitedPeaksCountByUser: (username: string) =>
      buildUrl(`/users/${username}/peaks/count`),
  },
} as const;
