import React from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "./AuthContext";

export function RequireAuth() {
  const { status } = useAuth();
  const location = useLocation();

  if (status === "booting") {
    return <div style={{ padding: 24 }}>Loading…</div>;
  }

  if (status === "unauthenticated") {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  return <Outlet />;
}

export function RequireMustChangePassword() {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;

  if (!user.must_change_password) {
    // If they already changed password, send to correct home
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}

export function RequirePasswordChanged() {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;

  if (user.must_change_password) {
    return <Navigate to="/change-password" replace />;
  }

  return <Outlet />;
}

export function RequireAdmin() {
  const { isAdmin } = useAuth();
  if (!isAdmin) return <Navigate to="/app" replace />;
  return <Outlet />;
}

export function RequireNonAdmin() {
  const { isAdmin } = useAuth();
  if (isAdmin) return <Navigate to="/admin" replace />;
  return <Outlet />;
}
