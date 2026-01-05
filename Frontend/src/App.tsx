import React from "react";
import { Navigate, Route, Routes } from "react-router-dom";

import LoginPage from "./pages/LoginPage";
import ChangePasswordPage from "./pages/ChangePasswordPage";

import AdminLayout from "./layouts/AdminLayout";
import AppLayout from "./layouts/AppLayout";

import AdminDashboard from "./pages/AdminDashboard";
import AppDashboard from "./pages/AppDashboard";

import {
  RequireAuth,
  RequireAdmin,
  RequireMustChangePassword,
  RequireNonAdmin,
  RequirePasswordChanged,
} from "./auth/guards";

export default function App() {
  return (
    <Routes>
      {/* Public */}
      <Route path="/login" element={<LoginPage />} />

      {/* Change password: must be authenticated AND must_change_password must be true */}
      <Route element={<RequireAuth />}>
        <Route element={<RequireMustChangePassword />}>
          <Route path="/change-password" element={<ChangePasswordPage />} />
        </Route>
      </Route>

      {/* Admin routes */}
      <Route element={<RequireAuth />}>
        <Route element={<RequirePasswordChanged />}>
          <Route element={<RequireAdmin />}>
            <Route path="/admin" element={<AdminLayout />}>
              <Route index element={<AdminDashboard />} />
            </Route>
          </Route>
        </Route>
      </Route>

      {/* Shared staff/cadet routes */}
      <Route element={<RequireAuth />}>
        <Route element={<RequirePasswordChanged />}>
          <Route element={<RequireNonAdmin />}>
            <Route path="/app" element={<AppLayout />}>
              <Route index element={<AppDashboard />} />
            </Route>
          </Route>
        </Route>
      </Route>

      {/* Home redirect */}
      <Route path="/" element={<Navigate to="/app" replace />} />

      {/* Catch-all */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
