// App.jsx - Root component: wires together AnalyzerForm and ResultCard

import { useState } from "react";
import { analyzeMessage } from "./api.js";
import AnalyzerForm from "./components/AnalyzerForm.jsx";
import ResultCard from "./components/ResultCard.jsx";

const styles = {
  wrapper: {
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    padding: "40px 16px",
    backgroundColor: "#f0f4f8",
  },
  card: {
    width: "100%",
    maxWidth: "680px",
    backgroundColor: "#fff",
    borderRadius: "14px",
    boxShadow: "0 4px 24px rgba(0,0,0,0.08)",
    padding: "32px",
  },
  heading: {
    fontSize: "1.6rem",
    fontWeight: "800",
    color: "#1a202c",
    marginBottom: "4px",
  },
  subtitle: {
    fontSize: "0.95rem",
    color: "#718096",
    marginBottom: "24px",
  },
  error: {
    marginTop: "16px",
    padding: "12px",
    backgroundColor: "#fff5f5",
    border: "1.5px solid #fc8181",
    borderRadius: "8px",
    color: "#c53030",
    fontSize: "0.9rem",
  },
};

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleAnalyze(text) {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await analyzeMessage(text);
      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={styles.wrapper}>
      <div style={styles.card}>
        <h1 style={styles.heading}>🔍 Fake Recruiter Detector</h1>
        <p style={styles.subtitle}>
          Paste a recruiter message to check it for common scam patterns.
        </p>

        <AnalyzerForm onSubmit={handleAnalyze} loading={loading} />

        {error && <div style={styles.error}>⚠ {error}</div>}

        {result && <ResultCard result={result} />}
      </div>
    </div>
  );
}
