export interface UserCreate {
  email: string;
  username: string;
  password: string;
}

export interface UserUpdate {
  isPrivate?: boolean;
}

export interface User {
  email: string;
  username: string;
  usernameDisplay: string;
  isPrivate: boolean;
}
