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
    background: "linear-gradient(135deg, #fdf2f8 0%, #f0fdf4 100%)",
  },
  card: {
    width: "100%",
    maxWidth: "680px",
    backgroundColor: "#fff",
    borderRadius: "16px",
    boxShadow: "0 10px 40px rgba(236, 72, 153, 0.1), 0 5px 20px rgba(16, 185, 129, 0.08)",
    padding: "32px",
    border: "1px solid rgba(236, 72, 153, 0.1)",
  },
  heading: {
    fontSize: "1.8rem",
    fontWeight: "900",
    background: "linear-gradient(135deg, #ec4899 0%, #10b981 100%)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    backgroundClip: "text",
    marginBottom: "4px",
  },
  subtitle: {
    fontSize: "0.95rem",
    color: "#6b7280",
    marginBottom: "24px",
  },
  error: {
    marginTop: "16px",
    padding: "12px",
    backgroundColor: "#fecdd3",
    border: "1.5px solid #ec4899",
    borderRadius: "8px",
    color: "#be185d",
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