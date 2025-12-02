/** Utility functions for authentication */
import { cookies } from "next/headers";

import { User } from "../users/types";

export async function getCurrentUser(): Promise<User | undefined> {
  const cookieStore = await cookies();
  const sessionCookie = cookieStore.get("session_id");
  if (!sessionCookie) return undefined;

  const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const response = await fetch(`${baseUrl}/api/auth/me`, {
    headers: {
      Cookie: `session_id=${sessionCookie.value}`,
    },
  });

  if (!response.ok) return undefined;

  const user = await response.json();
  return user;
}
