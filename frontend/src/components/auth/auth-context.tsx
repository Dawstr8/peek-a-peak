"use client";

import { createContext, useContext, useEffect, useState } from "react";

import { AuthClient } from "@/lib/auth/client";
import type { User } from "@/lib/users/types";

interface AuthContextType {
  user: User | undefined;
  isLoading: boolean;
  login: (user: User) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | undefined>(undefined);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    checkMe();
  }, []);

  useEffect(() => {
    const handleUnauthorized = () => {
      setUser(undefined);
    };

    window.addEventListener("unauthorized", handleUnauthorized);
    return () => {
      window.removeEventListener("unauthorized", handleUnauthorized);
    };
  }, []);

  const checkMe = async () => {
    try {
      const user = await AuthClient.me();
      setUser(user);
    } catch {
      setUser(undefined);
    } finally {
      setIsLoading(false);
    }
  };

  const login = (user: User) => {
    setUser(user);
  };

  const logout = () => {
    setUser(undefined);
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }

  return context;
};
