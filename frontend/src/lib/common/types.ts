export class ApiError extends Error {
  name: string = "ApiError";

  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

export class AuthorizationApiError extends ApiError {
  name: string = "AuthorizationApiError";
}

export class ValidationApiError extends ApiError {
  name: string = "ValidationApiError";

  errors: { loc: string[]; msg: string; type: string }[];

  constructor(
    message: string,
    status: number,
    errors: { loc: string[]; msg: string; type: string }[],
  ) {
    super(message, status);
    this.errors = errors;
  }
}
