// AnalyzerForm.jsx - Textarea input and submit button for the analyzer

import { useState } from "react";

const styles = {
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "12px",
  },
  label: {
    fontWeight: "700",
    fontSize: "0.95rem",
    background: "linear-gradient(135deg, #ec4899 0%, #10b981 100%)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    backgroundClip: "text",
  },
  textarea: {
    width: "100%",
    minHeight: "140px",
    padding: "12px",
    borderRadius: "10px",
    border: "2px solid #f3e8ff",
    fontSize: "0.95rem",
    resize: "vertical",
    outline: "none",
    fontFamily: "inherit",
    transition: "border-color 0.3s ease, box-shadow 0.3s ease",
  },
  button: {
    alignSelf: "flex-end",
    padding: "11px 32px",
    background: "linear-gradient(135deg, #ec4899 0%, #db2777 100%)",
    color: "#fff",
    border: "none",
    borderRadius: "10px",
    fontSize: "1rem",
    fontWeight: "700",
    cursor: "pointer",
    boxShadow: "0 4px 15px rgba(236, 72, 153, 0.3)",
    transition: "transform 0.2s ease, box-shadow 0.2s ease",
  },
  buttonDisabled: {
    background: "linear-gradient(135deg, #fbcfe8 0%, #dcfce7 100%)",
    cursor: "not-allowed",
    boxShadow: "0 2px 8px rgba(236, 72, 153, 0.1)",
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
  const [focused, setFocused] = useState(false);

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
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        placeholder="e.g. Hi! We found your profile on LinkedIn and have an exciting opportunity…"
        style={{
          ...styles.textarea,
          borderColor: focused ? "#ec4899" : "#f3e8ff",
          boxShadow: focused ? "0 0 0 3px rgba(236, 72, 153, 0.1)" : "none",
        }}
        disabled={loading}
      />
      <button
        type="submit"
        disabled={loading || !text.trim()}
        onMouseEnter={(e) => {
          if (!loading && text.trim()) {
            e.target.style.transform = "translateY(-2px)";
            e.target.style.boxShadow = "0 6px 20px rgba(236, 72, 153, 0.4)";
          }
        }}
        onMouseLeave={(e) => {
          if (!loading && text.trim()) {
            e.target.style.transform = "none";
            e.target.style.boxShadow = "0 4px 15px rgba(236, 72, 153, 0.3)";
          }
        }}
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