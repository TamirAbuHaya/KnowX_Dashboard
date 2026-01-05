import React from "react";
import { Link, Outlet } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export default function AppLayout() {
  const { user, logout } = useAuth();

  return (
    <div style={{ display: "grid", gridTemplateColumns: "240px 1fr", minHeight: "100vh" }}>
      <aside style={{ borderRight: "1px solid #ddd", padding: 16 }}>
        <h2 style={{ marginTop: 0 }}>Dashboard</h2>
        <div style={{ fontSize: 14, opacity: 0.8, marginBottom: 12 }}>
          {user?.full_name ?? user?.email}
          <div style={{ marginTop: 6, fontSize: 12, opacity: 0.8 }}>
            Role: {user?.role ?? "—"} • Battalion: {user?.battalion ?? "—"}
          </div>
        </div>

        <nav style={{ display: "grid", gap: 8 }}>
          <Link to="/app">Home</Link>
          {/* Later: render extra links/buttons based on privileges */}
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
