import React, { createContext, useContext, useEffect, useMemo, useState } from "react";
import { api } from "../api/client";
import { tokenStorage } from "./tokenStorage";
import type { MeResponse } from "./types";

type AuthStatus = "booting" | "authenticated" | "unauthenticated";

type AuthContextValue = {
  status: AuthStatus;
  user: MeResponse | null;

  login: (email: string, password: string) => Promise<MeResponse>;
  logout: () => Promise<void>;

  refetchMe: () => Promise<MeResponse>;
  isAdmin: boolean;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

function computeIsAdmin(user: MeResponse | null) {
  if (!user) return false;
  return Boolean(user.is_superuser || user.is_staff || user.role === "ADMIN");
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [status, setStatus] = useState<AuthStatus>("booting");
  const [user, setUser] = useState<MeResponse | null>(null);

  const isAdmin = useMemo(() => computeIsAdmin(user), [user]);

  async function refetchMe(): Promise<MeResponse> {
    const res = await api.get("/api/auth/me/");
    const me = res.data as MeResponse;
    setUser(me);
    setStatus("authenticated");
    return me;
  }

  async function boot() {
    const access = tokenStorage.getAccess();
    const refresh = tokenStorage.getRefresh();

    if (!access || !refresh) {
      setUser(null);
      setStatus("unauthenticated");
      return;
    }

    try {
      await refetchMe();
    } catch {
      // If /me fails even after interceptor refresh attempt, we go unauthenticated
      tokenStorage.clear();
      setUser(null);
      setStatus("unauthenticated");
    }
  }

  useEffect(() => {
    void boot();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function login(email: string, password: string): Promise<MeResponse> {
    const res = await api.post("/api/auth/token/", { email, password });
    const { access, refresh } = res.data as { access: string; refresh: string };
    tokenStorage.setTokens(access, refresh);

    const me = await refetchMe();
    return me;
  }

  async function logout(): Promise<void> {
    // If you have /api/auth/logout/, we try it, but we always clear tokens.
    try {
      await api.post("/api/auth/logout/");
    } catch {
      // ignore
    } finally {
      tokenStorage.clear();
      setUser(null);
      setStatus("unauthenticated");
    }
  }

  const value: AuthContextValue = {
    status,
    user,
    login,
    logout,
    refetchMe,
    isAdmin,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}
