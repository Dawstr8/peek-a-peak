import { ApiClient } from "@/lib/common/api-client";
import type {
  SummitPhoto,
  SummitPhotoDate,
  SummitPhotoLocation,
} from "@/lib/photos/types";

import { API_ENDPOINTS } from "@/config/api";

import { PaginatedResponse } from "../pagination/types";
import { User, UserUpdate } from "./types";

export class UsersClient extends ApiClient {
  static async updateUser(
    username: string,
    userUpdate: UserUpdate,
  ): Promise<User> {
    return this.patch<User>(
      API_ENDPOINTS.users.updateUser(username),
      userUpdate,
    );
  }

  static async getPhotosByUser(
    username: string,
    sortBy: string | null = null,
    order: "asc" | "desc" | null = null,
    page: number | null = null,
    perPage: number | null = null,
  ): Promise<PaginatedResponse<SummitPhoto>> {
    const data = await this.get<PaginatedResponse<SummitPhoto>>(
      API_ENDPOINTS.users.getPhotosByUser(
        username,
        sortBy,
        order,
        page,
        perPage,
      ),
    );

    return new PaginatedResponse<SummitPhoto>(data);
  }
  static async getPhotosLocationsByUser(
    username: string,
  ): Promise<SummitPhotoLocation[]> {
    return this.get<SummitPhotoLocation[]>(
      API_ENDPOINTS.users.getPhotosLocationsByUser(username),
    );
  }

  static async getPhotosDatesByUser(
    username: string,
  ): Promise<SummitPhotoDate[]> {
    return this.get<SummitPhotoDate[]>(
      API_ENDPOINTS.users.getPhotosDatesByUser(username),
    );
  }

  static async getSummitedPeaksCountByUser(username: string): Promise<number> {
    return this.get<number>(
      API_ENDPOINTS.users.getSummitedPeaksCountByUser(username),
    );
  }
}
