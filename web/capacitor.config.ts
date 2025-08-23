import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.pqtorus.app',
  appName: 'PQTorus',
  webDir: 'dist',
  server: {
    androidScheme: 'https'
  },
  android: {
    webContentsDebuggingEnabled: true
  }
};

export default config;
