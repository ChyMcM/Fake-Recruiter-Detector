// ResultCard.jsx - Displays the risk score, level, and flagged phrases

const levelColors = {
  Low: { bg: "#c6f6d5", text: "#276749", border: "#9ae6b4" },
  Medium: { bg: "#fefcbf", text: "#744210", border: "#f6e05e" },
  High: { bg: "#fed7d7", text: "#822727", border: "#fc8181" },
};

const styles = {
  card: {
    marginTop: "24px",
    padding: "20px",
    borderRadius: "10px",
    border: "1.5px solid #e2e8f0",
    backgroundColor: "#fff",
  },
  header: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: "16px",
  },
  title: {
    fontSize: "1.1rem",
    fontWeight: "700",
    color: "#2d3748",
  },
  badge: (level) => ({
    padding: "4px 14px",
    borderRadius: "999px",
    fontWeight: "700",
    fontSize: "0.85rem",
    backgroundColor: levelColors[level]?.bg || "#e2e8f0",
    color: levelColors[level]?.text || "#2d3748",
    border: `1.5px solid ${levelColors[level]?.border || "#cbd5e0"}`,
  }),
  scoreRow: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
    marginBottom: "16px",
  },
  scoreLabel: {
    fontSize: "0.9rem",
    color: "#718096",
  },
  scoreValue: {
    fontSize: "2rem",
    fontWeight: "800",
    color: "#2d3748",
  },
  progressBar: {
    flex: 1,
    height: "10px",
    borderRadius: "999px",
    backgroundColor: "#e2e8f0",
    overflow: "hidden",
  },
  progressFill: (score, level) => ({
    height: "100%",
    width: `${score}%`,
    borderRadius: "999px",
    backgroundColor: levelColors[level]?.border || "#cbd5e0",
    transition: "width 0.4s ease",
  }),
  sectionTitle: {
    fontWeight: "600",
    fontSize: "0.9rem",
    color: "#4a5568",
    marginBottom: "8px",
  },
  flagList: {
    listStyle: "none",
    padding: 0,
    display: "flex",
    flexDirection: "column",
    gap: "6px",
  },
  flagItem: {
    padding: "6px 12px",
    backgroundColor: "#fff5f5",
    border: "1px solid #fed7d7",
    borderRadius: "6px",
    fontSize: "0.88rem",
    color: "#c53030",
  },
  noFlags: {
    fontSize: "0.9rem",
    color: "#68d391",
  },
};

/**
 * ResultCard - Shows the analysis results returned by the backend.
 *
 * Props:
 *   result: { score, level, flags, highlights }
 */
export default function ResultCard({ result }) {
  const { score, level, flags } = result;

  return (
    <div style={styles.card}>
      <div style={styles.header}>
        <span style={styles.title}>Analysis Result</span>
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

      <p style={styles.sectionTitle}>Triggered Flags</p>
      {flags.length === 0 ? (
        <p style={styles.noFlags}>✓ No suspicious patterns detected.</p>
      ) : (
        <ul style={styles.flagList}>
          {flags.map((flag, i) => (
            <li key={i} style={styles.flagItem}>
              ⚠ {flag}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
