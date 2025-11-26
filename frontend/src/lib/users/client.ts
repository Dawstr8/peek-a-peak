import { ApiClient } from "@/lib/common/api-client";
import type { SummitPhoto } from "@/lib/photos/types";

import { API_ENDPOINTS } from "@/config/api";

export class UsersClient extends ApiClient {
  static async getPhotosByUser(
    username: string,
    sortBy: string | null = null,
    order: "asc" | "desc" | null = null,
  ): Promise<SummitPhoto[]> {
    return this.get<SummitPhoto[]>(
      API_ENDPOINTS.users.getPhotosByUser(username, sortBy, order),
    );
  }

  static async getSummitedPeaksCountByUser(username: string): Promise<number> {
    return this.get<number>(
      API_ENDPOINTS.users.getSummitedPeaksCountByUser(username),
    );
  }
}
