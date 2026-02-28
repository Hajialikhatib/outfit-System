import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // Determine if we're in production mode
  const isProduction = mode === 'production'

  return {
    plugins: [react()],
    server: {
      port: 5173,
      // Only use proxy in development mode
      proxy: isProduction ? undefined : {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
        },
        '/media': {
          target: 'http://localhost:8000',
          changeOrigin: true,
        }
      }
    },
    // Build configuration for production
    build: {
      outDir: 'dist',
      sourcemap: false, // Disable sourcemaps in production for security
      minify: 'terser',
    }
  }
})
