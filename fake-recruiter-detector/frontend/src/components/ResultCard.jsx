// ResultCard.jsx - Displays the risk score, level, and flagged phrases with pink & green theme

const levelColors = {
  Low: { bg: "#dcfce7", text: "#166534", border: "#10b981" },
  Medium: { bg: "#fef3c7", text: "#92400e", border: "#f59e0b" },
  High: { bg: "#fecdd3", text: "#be185d", border: "#ec4899" },
};

const styles = {
  card: {
    marginTop: "24px",
    padding: "24px",
    borderRadius: "12px",
    border: "1.5px solid rgba(236, 72, 153, 0.2)",
    backgroundColor: "#fff",
    boxShadow: "0 4px 12px rgba(16, 185, 129, 0.08)",
  },
  header: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: "20px",
    paddingBottom: "12px",
    borderBottom: "2px solid rgba(236, 72, 153, 0.15)",
  },
  title: {
    fontSize: "1.2rem",
    fontWeight: "800",
    background: "linear-gradient(135deg, #ec4899 0%, #10b981 100%)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    backgroundClip: "text",
  },
  badge: (level) => ({
    padding: "6px 16px",
    borderRadius: "20px",
    fontWeight: "700",
    fontSize: "0.85rem",
    backgroundColor: levelColors[level]?.bg || "#f3e8ff",
    color: levelColors[level]?.text || "#6b7280",
    border: `1.5px solid ${levelColors[level]?.border || "#c4b5fd"}`,
  }),
  scoreRow: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
    marginBottom: "20px",
  },
  scoreLabel: {
    fontSize: "0.9rem",
    color: "#6b7280",
  },
  scoreValue: {
    fontSize: "2.4rem",
    fontWeight: "900",
    background: "linear-gradient(135deg, #ec4899 0%, #10b981 100%)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    backgroundClip: "text",
  },
  progressBar: {
    flex: 1,
    height: "12px",
    borderRadius: "999px",
    backgroundColor: "#f3e8ff",
    overflow: "hidden",
  },
  progressFill: (score, level) => ({
    height: "100%",
    width: `${score}%`,
    borderRadius: "999px",
    background: `linear-gradient(90deg, ${levelColors[level]?.border || "#ec4899"}, ${levelColors[level]?.border || "#10b981"})`,
    transition: "width 0.4s ease",
  }),
  sectionTitle: {
    fontWeight: "700",
    fontSize: "0.95rem",
    background: "linear-gradient(135deg, #ec4899 0%, #10b981 100%)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    backgroundClip: "text",
    marginBottom: "12px",
  },
  flagList: {
    listStyle: "none",
    padding: 0,
    display: "flex",
    flexDirection: "column",
    gap: "8px",
  },
  flagItem: {
    padding: "10px 14px",
    backgroundColor: "#fecdd3",
    border: "1.5px solid #ec4899",
    borderRadius: "8px",
    fontSize: "0.9rem",
    color: "#be185d",
    fontWeight: "500",
  },
  noFlags: {
    fontSize: "0.95rem",
    color: "#10b981",
    fontWeight: "600",
  },
  highlightsSection: {
    marginTop: "20px",
    paddingTop: "20px",
    borderTop: "1px solid rgba(236, 72, 153, 0.15)",
  },
  highlightChips: {
    display: "flex",
    flexWrap: "wrap",
    gap: "10px",
  },
  highlightChip: {
    display: "inline-flex",
    alignItems: "center",
    gap: "6px",
    padding: "8px 14px",
    background: "linear-gradient(135deg, #fce7f3 0%, #d1fae5 100%)",
    border: "1.5px solid #ec4899",
    borderRadius: "20px",
    fontSize: "0.85rem",
    fontWeight: "600",
    color: "#831843",
    boxShadow: "0 2px 6px rgba(236, 72, 153, 0.15)",
  },
  highlightIcon: {
    fontSize: "1rem",
  },
};

/**
 * ResultCard - Shows the analysis results returned by the backend.
 *
 * Props:
 *   result: { score, level, flags, highlights }
 */
export default function ResultCard({ result }) {
  const { score, level, flags, highlights } = result;

  return (
    <div style={styles.card}>
      <div style={styles.header}>
        <span style={styles.title}>✨ Analysis Result</span>
        <span style={styles.badge(level)}>{level} Risk</span>
      </div>

      <div style={styles.scoreRow}>
        <span style={styles.scoreLabel}>Score</span>
        <span style={styles.scoreValue}>{score}</span>
        <div style={styles.progressBar}>
          <div style={styles.progressFill(score, level)} />
        </div>
        <span style={styles.scoreLabel}>/100</span>
      </div>

      <p style={styles.sectionTitle}>🚨 Triggered Flags</p>
      {flags.length === 0 ? (
        <p style={styles.noFlags}>✅ No suspicious patterns detected.</p>
      ) : (
        <ul style={styles.flagList}>
          {flags.map((flag, i) => (
            <li key={i} style={styles.flagItem}>
              🚩 {flag}
            </li>
          ))}
        </ul>
      )}

      {highlights && highlights.length > 0 && (
        <div style={styles.highlightsSection}>
          <p style={styles.sectionTitle}>🔍 Detected Suspicious Phrases</p>
          <div style={styles.highlightChips}>
            {highlights.map((highlight, i) => (
              <span key={i} style={styles.highlightChip}>
                <span style={styles.highlightIcon}>⚡</span>
                {highlight.phrase}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}