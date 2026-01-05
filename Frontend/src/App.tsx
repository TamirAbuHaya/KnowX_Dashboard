import { useEffect, useState } from "react";

export default function App() {
  const [status, setStatus] = useState("loading...");

  useEffect(() => {
    fetch("/api/health/")
      .then((r) => r.json())
      .then((data) => setStatus(data.status ?? "unknown"))
      .catch(() => setStatus("error"));
  }, []);

  return (
    <div style={{ padding: 24, fontFamily: "system-ui" }}>
      <h1>Django API + Vite SPA</h1>
      <p>Backend health: {status}</p>
    </div>
  );
}
