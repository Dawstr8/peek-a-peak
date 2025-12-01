import { ApiError, AuthorizationApiError, ValidationApiError } from "./types";

export class ApiClient {
  protected static async request<T>(
    method: string,
    url: string,
    data?: unknown,
    options?: RequestInit,
  ): Promise<T> {
    const isFormData = data instanceof FormData;

    const headers: HeadersInit = {
      ...(!isFormData ? { "Content-Type": "application/json" } : {}),
      Accept: "application/json",
      ...options?.headers,
    };

    const response = await fetch(url, {
      method,
      credentials: "include",
      headers,
      body: data ? (isFormData ? data : JSON.stringify(data)) : undefined,
      ...options,
    });

    if (!response.ok) {
      throw await this.handleError(response);
    }

    if (response.status === 204) {
      return {} as T;
    }

    return response.json();
  }

  protected static async handleError(response: Response): Promise<Error> {
    const defaultMessage = `Request failed with status: ${response.status}`;

    if (response.status === 401) {
      window.dispatchEvent(new CustomEvent("unauthorized"));
    }

    const contentType = response.headers.get("content-type") ?? "";

    try {
      if (!contentType.includes("application/json")) {
        const text = await response.text().catch(() => "");
        return new ApiError(text || defaultMessage, response.status);
      }

      const errorData = await response.json().catch(() => null);
      if (errorData && typeof errorData.detail === "string") {
        return new AuthorizationApiError(errorData.detail, response.status);
      }

      if (errorData && Array.isArray(errorData.detail)) {
        return new ValidationApiError(
          "Validation failed",
          response.status,
          errorData.detail.map(
            (error: { loc: string[]; msg: string; type: string }) => {
              return {
                loc: error.loc,
                msg: error.msg,
                type:
                  typeof error.type === "string" ? error.type : "validation",
              };
            },
          ),
        );
      }

      const message =
        (errorData && (errorData.message || errorData.detail)) ||
        (errorData ? JSON.stringify(errorData) : defaultMessage);

      return new ApiError(String(message), response.status);
    } catch {
      return new ApiError(defaultMessage, response.status);
    }
  }

  protected static async get<T>(
    url: string,
    options?: RequestInit,
  ): Promise<T> {
    return this.request<T>("GET", url, undefined, options);
  }

  protected static async post<T>(
    url: string,
    data?: unknown,
    options?: RequestInit,
  ): Promise<T> {
    return this.request<T>("POST", url, data, options);
  }

  protected static async patch<T>(
    url: string,
    data: unknown,
    options?: RequestInit,
  ): Promise<T> {
    return this.request<T>("PATCH", url, data, options);
  }

  protected static async delete<T = void>(
    url: string,
    options?: RequestInit,
  ): Promise<T> {
    return this.request<T>("DELETE", url, undefined, options);
  }
}
