import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    minify: "terser",
    assetsInlineLimit: Infinity,
    emptyOutDir: true
  },

  plugins: [tailwindcss(), sveltekit()],
});
