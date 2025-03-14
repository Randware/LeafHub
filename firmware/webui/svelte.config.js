import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const config = {
  preprocess: vitePreprocess(),

  kit: {
    adapter: adapter({
      pages: '../src/public',
      assets: '../src/public',
      precompress: false,
      strict: true
    }),

    output: {
      bundleStrategy: 'inline'
    }
  },
};

export default config;
