import { app } from 'electron'
import { join } from 'path'

export const CONFIG = {
  // Paths
  dataDir: join(app.getPath('userData'), 'data'),
  flowsDir: join(app.getPath('userData'), 'flows'),
  logsDir: join(app.getPath('userData'), 'logs'),
  scrcpyJar: join(__dirname, '../server/scrcpy-server.jar'),

  // ADB
  adbPath: 'adb', // Use system PATH
  adbPort: 5037,
  reconnectInterval: 5000,
  reconnectMaxRetries: 10,

  // Screen Capture
  screencapInterval: 300, // ms (legacy fallback mode)
  screencapQuality: 80,   // JPEG quality 1-100
  screencapMaxWidth: 480, // thumbnail max width for grid

  // Scrcpy (Phase 1)
  scrcpyEnabled: true,
  scrcpyFallbackOnFail: true,
  scrcpyTimeout: 15000,
  scrcpyMaxWidth: 720,     // downscale to save bandwidth
  scrcpyBitrate: 8,        // Mbps
  scrcpyMaxFps: 30,

  // Health Monitoring
  healthCheckInterval: 10000, // 10 seconds

  // Device Defaults
  defaultTimeout: 15000,
  tapRetryCount: 2,

  // Network
  tcpConnectTimeout: 10000,
  keepaliveInterval: 15000
} as const
