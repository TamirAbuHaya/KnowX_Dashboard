import React from "react";
import { Link, Outlet } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export default function AdminLayout() {
  const { user, logout } = useAuth();

  return (
    <div style={{ display: "grid", gridTemplateColumns: "240px 1fr", minHeight: "100vh" }}>
      <aside style={{ borderRight: "1px solid #ddd", padding: 16 }}>
        <h2 style={{ marginTop: 0 }}>Admin Panel</h2>
        <div style={{ fontSize: 14, opacity: 0.8, marginBottom: 12 }}>
          {user?.full_name ?? user?.email}
        </div>

        <nav style={{ display: "grid", gap: 8 }}>
          <Link to="/admin">Dashboard</Link>
        </nav>

        <div style={{ marginTop: 16 }}>
          <button onClick={() => void logout()}>Logout</button>
        </div>
      </aside>

      <main style={{ padding: 24 }}>
        <Outlet />
      </main>
    </div>
  );
}
