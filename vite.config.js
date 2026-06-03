import { defineConfig } from 'vite';

export default defineConfig({
  appType: 'mpa',
  plugins: [
    {
      name: 'rewrite-all',
      configureServer(server) {
        server.middlewares.use((req, res, next) => {
          if (!req.url.includes('.') && req.url !== '/' && !req.url.startsWith('/@')) {
            req.url += '.html';
          }
          next();
        });
      }
    }
  ]
});
