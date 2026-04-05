import React, { useState } from "react";

function App() {
  const [target, setTarget] = useState("");
  const [logs, setLogs] = useState([]);
  const API_BASE = "http://localhost:8000";

 const startScan = async () => {
  try {
    const res = await fetch(`${API_BASE}/scan?target=${target}`, {
      method: "POST"
    });

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }

    const data = await res.json();

    const ws = new WebSocket(`ws://localhost:8000/ws/${data.scan_id}`);

    ws.onmessage = (event) => {
      setLogs((prev) => [...prev, event.data]);
    };

  } catch (err) {
    console.error("ERROR:", err);
  }
};

  return (
    <div style={{ padding: 20 }}>
      <h2>Recon Dashboard</h2>

      <input
        value={target}
        onChange={(e) => setTarget(e.target.value)}
        placeholder="example.com"
      />

      <button onClick={startScan}>Start Scan</button>

      <div style={{ marginTop: 20 }}>
        <h3>Live Updates</h3>
        <pre>
          {logs.map((log, i) => (
            <div key={i}>{log}</div>
          ))}
        </pre>
      </div>
    </div>
  );
}

export default App;