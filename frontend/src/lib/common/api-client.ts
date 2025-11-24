interface ApiErrorResponse {
  message?: string;
  errors?: Record<string, string[]>;
  [key: string]: unknown;
}

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
    let errorMessage = `Request failed with status: ${response.status}`;

    if (response.status === 401) {
      window.dispatchEvent(new CustomEvent("unauthorized"));
    }

    try {
      const errorData = (await response.json()) as ApiErrorResponse;

      if (errorData.message) {
        errorMessage = errorData.message;
      } else if (errorData.errors) {
        const errorMessages = Object.entries(errorData.errors)
          .map(([field, messages]) => `${field}: ${messages.join(", ")}`)
          .join("; ");

        errorMessage = errorMessages || errorMessage;
      }
    } catch {}

    return new Error(errorMessage);
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

  protected static async put<T>(
    url: string,
    data: unknown,
    options?: RequestInit,
  ): Promise<T> {
    return this.request<T>("PUT", url, data, options);
  }

  protected static async delete<T = void>(
    url: string,
    options?: RequestInit,
  ): Promise<T> {
    return this.request<T>("DELETE", url, undefined, options);
  }
}
