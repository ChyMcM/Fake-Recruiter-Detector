// api.js - Functions for communicating with the FastAPI backend

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

/**
 * Send a recruiter message to the backend for analysis.
 *
 * @param {string} text - The recruiter message to analyze.
 * @returns {Promise<{score: number, level: string, flags: string[], highlights: {phrase: string}[]}>}
 */
export async function analyzeMessage(text) {
  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`API error ${response.status}: ${error}`);
  }

  return response.json();
}
