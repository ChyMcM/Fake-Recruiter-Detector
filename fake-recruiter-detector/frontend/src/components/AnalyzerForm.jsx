// AnalyzerForm.jsx - Textarea input and submit button for the analyzer

import { useState } from "react";

const styles = {
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "12px",
  },
  label: {
    fontWeight: "600",
    fontSize: "0.95rem",
    color: "#2d3748",
  },
  textarea: {
    width: "100%",
    minHeight: "140px",
    padding: "12px",
    borderRadius: "8px",
    border: "1.5px solid #cbd5e0",
    fontSize: "0.95rem",
    resize: "vertical",
    outline: "none",
    fontFamily: "inherit",
  },
  button: {
    alignSelf: "flex-end",
    padding: "10px 28px",
    backgroundColor: "#3182ce",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    fontSize: "1rem",
    fontWeight: "600",
    cursor: "pointer",
  },
  buttonDisabled: {
    backgroundColor: "#90cdf4",
    cursor: "not-allowed",
  },
};

/**
 * AnalyzerForm - Collects the recruiter message and triggers analysis.
 *
 * Props:
 *   onSubmit(text: string) - called when the user submits the form
 *   loading: boolean       - disables button while a request is in flight
 */
export default function AnalyzerForm({ onSubmit, loading }) {
  const [text, setText] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    const trimmed = text.trim();
    if (trimmed) onSubmit(trimmed);
  }

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <label htmlFor="message" style={styles.label}>
        Paste the recruiter message below:
      </label>
      <textarea
        id="message"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="e.g. Hi! We found your profile on LinkedIn and have an exciting opportunity…"
        style={styles.textarea}
        disabled={loading}
      />
      <button
        type="submit"
        disabled={loading || !text.trim()}
        style={{
          ...styles.button,
          ...(loading || !text.trim() ? styles.buttonDisabled : {}),
        }}
      >
        {loading ? "Analyzing…" : "Analyze Message"}
      </button>
    </form>
  );
}
