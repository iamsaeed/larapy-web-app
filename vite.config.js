import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';

export default defineConfig({
  plugins: [vue()],

  resolve: {
    alias: {
      'vue': 'vue/dist/vue.esm-bundler.js'
    }
  },

  build: {
    outDir: 'public/build',
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      input: {
        app: resolve(__dirname, 'resources/js/app.js'),
        css: resolve(__dirname, 'resources/css/app.css'),
      },
    },
  },

  server: {
    host: '0.0.0.0',
    port: 5173,
    hmr: {
      host: 'localhost',
    },
  },

  // For development, write hot file to public directory
  experimental: {
    renderBuiltUrl(filename, { hostType }) {
      if (hostType === 'js') {
        return { js: `/build/${filename}` };
      } else {
        return { css: `/build/${filename}` };
      }
    },
  },
});