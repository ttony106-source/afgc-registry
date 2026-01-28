import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  output: 'static',
  site: import.meta.env.SITE_URL || 'https://kamakazigroup.com',
  build: {
    assets: '_assets'
  }
});
