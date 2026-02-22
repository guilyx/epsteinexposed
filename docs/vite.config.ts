// Credits: Erwin Lejeune — 2026-02-22
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: { port: 5175 },
  assetsInclude: ["**/*.md"],
});
