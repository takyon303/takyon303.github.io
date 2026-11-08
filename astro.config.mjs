import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";

import react from "@astrojs/react";

export default defineConfig({
  // custom domain on GitHub Pages
  site: "https://takyon.online",

  vite: {
    plugins: [tailwindcss()],
  },

  integrations: [react()],
});