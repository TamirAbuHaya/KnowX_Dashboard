import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { useAuth } from "../auth/AuthContext";

export default function ChangePasswordPage() {
  const { refetchMe, isAdmin } = useAuth();
  const nav = useNavigate();

  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [err, setErr] = useState<string | null>(null);
  const [ok, setOk] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErr(null);
    setOk(null);

    if (newPassword.length < 6) {
      setErr("New password is too short.");
      return;
    }
    if (newPassword !== confirm) {
      setErr("Passwords do not match.");
      return;
    }

    setLoading(true);
    try {
      await api.post("/api/auth/change-password/", {
        old_password: oldPassword,
        new_password: newPassword,
      });

      const me = await refetchMe();
      setOk("Password updated.");

      // Route based on admin vs non-admin
      const admin = Boolean(me.is_superuser || me.is_staff || me.role === "ADMIN" || isAdmin);
      nav(admin ? "/admin" : "/app", { replace: true });
    } catch (e: any) {
      setErr(e?.response?.data?.detail ?? "Could not change password.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 520, margin: "60px auto", padding: 24 }}>
      <h1 style={{ marginBottom: 6 }}>Change Password</h1>
      <p style={{ marginTop: 0, opacity: 0.75 }}>
        You must change your password before you can access the system.
      </p>

      <form onSubmit={onSubmit} style={{ display: "grid", gap: 12, marginTop: 16 }}>
        <label style={{ display: "grid", gap: 6 }}>
          <span>Temporary / Current Password</span>
          <input
            value={oldPassword}
            onChange={(e) => setOldPassword(e.target.value)}
            type="password"
            autoComplete="current-password"
            required
          />
        </label>

        <label style={{ display: "grid", gap: 6 }}>
          <span>New Password</span>
          <input
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            type="password"
            autoComplete="new-password"
            required
          />
        </label>

        <label style={{ display: "grid", gap: 6 }}>
          <span>Confirm New Password</span>
          <input
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
            type="password"
            autoComplete="new-password"
            required
          />
        </label>

        {err && <div style={{ color: "crimson" }}>{err}</div>}
        {ok && <div style={{ color: "green" }}>{ok}</div>}

        <button type="submit" disabled={loading}>
          {loading ? "Updating…" : "Update password"}
        </button>
      </form>
    </div>
  );
}
