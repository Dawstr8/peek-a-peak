import { useAuth } from "@/components/auth";

export function useAuthenticatedUser() {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    throw new Error(
      "useAuthenticatedUser must not be called while auth is still loading",
    );
  }

  if (!user) {
    throw new Error("useAuthenticatedUser must be used inside <RequireAuth>");
  }

  return user;
}
