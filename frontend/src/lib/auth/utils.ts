/** Utility functions for authentication */
import { cookies } from "next/headers";

export async function checkIfAuthenticated(): Promise<boolean> {
  const cookieStore = await cookies();
  const sessionCookie = cookieStore.get("session_id");
  if (!sessionCookie) return false;

  const response = await fetch("http://backend:8000/api/auth/me", {
    headers: {
      Cookie: `session_id=${sessionCookie.value}`,
    },
  });

  if (!response.ok) return false;

  const user = await response.json();
  return !!user;
}
