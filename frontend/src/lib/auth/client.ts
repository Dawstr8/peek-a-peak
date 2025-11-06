import { ApiClient } from "@/lib/common/api-client";
import type { User, UserCreate } from "@/lib/users/types";

import { API_ENDPOINTS } from "@/config/api";

/**
 * AuthClient class for handling user-related API requests
 */
export class AuthClient extends ApiClient {
  static async login(emailOrUsername: string, password: string): Promise<User> {
    const formData = new FormData();
    formData.append("email_or_username", emailOrUsername);
    formData.append("password", password);

    await this.post(API_ENDPOINTS.auth.login, formData);
    return this.me();
  }

  static async register(userCreate: UserCreate): Promise<User> {
    return this.post<User>(API_ENDPOINTS.auth.register, userCreate);
  }

  static async me(): Promise<User> {
    return this.get<User>(API_ENDPOINTS.auth.me);
  }

  static async logout(): Promise<void> {
    return this.post(API_ENDPOINTS.auth.logout);
  }
}
