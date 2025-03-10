import { useEffect, useState } from "react";

const LogPage = () => {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const socket = new WebSocket("ws://127.0.0.1:8000/ws/logs");

    socket.onmessage = (event) => {
      setLogs((prevLogs) => [...prevLogs, event.data]);
    };

    return () => socket.close();
  }, []);

  return (
    <div>
      <h2>Backend Logs</h2>
      <div style={{ background: "#222", color: "#0f0", padding: "10px", height: "300px", overflowY: "auto" }}>
        {logs.map((log, index) => (
          <p key={index}>{log}</p>
        ))}
      </div>
    </div>
  );
};

export default LogPage;
