import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => ({
  plugins: [react()],
  // Preserve CRA's public environment-variable contract without exposing server secrets.
  define: {
    'process.env.PUBLIC_URL': JSON.stringify(''),
    ...Object.fromEntries(Object.entries(loadEnv(mode, process.cwd(), 'REACT_APP_'))
      .map(([key, value]) => ['process.env.' + key, JSON.stringify(value)])),
  },
  build: { outDir: 'build' },
  test: { environment: 'jsdom', globals: true, setupFiles: ['./src/setupTests.ts'] },
}));
