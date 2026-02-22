// vite.config.js - Vite configuration for the React frontend
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // Proxy API calls to the FastAPI backend during development
    proxy: {
      "/analyze": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
