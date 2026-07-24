import { app, BrowserWindow, ipcMain, shell } from 'electron'
import { join } from 'path'
import { DeviceManager } from './device-manager'
import { ScreencapLegacy } from './screencap-legacy'
import { InputController } from './input-controller'
import { ScrcpyServer } from './scrcpy-server'
import { DeviceHealth } from './device-health'

// Prevent multiple instances
const gotLock = app.requestSingleInstanceLock()
if (!gotLock) {
  app.quit()
}

let mainWindow: BrowserWindow | null = null
let deviceManager: DeviceManager | null = null
let screencap: ScreencapLegacy | null = null
let inputController: InputController | null = null
let scrcpyServer: ScrcpyServer | null = null
let deviceHealth: DeviceHealth | null = null

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1440,
    height: 900,
    minWidth: 1024,
    minHeight: 600,
    frame: false,
    titleBarStyle: 'hidden',
    backgroundColor: '#080808',
    title: 'Phone Bot',
    webPreferences: {
      preload: join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: false
    }
  })

  if (process.env.NODE_ENV === 'development' || process.env.VITE_DEV_SERVER_URL) {
    mainWindow.webContents.openDevTools({ mode: 'detach' })
  }

  if (process.env.VITE_DEV_SERVER_URL) {
    mainWindow.loadURL(process.env.VITE_DEV_SERVER_URL)
  } else {
    mainWindow.loadFile(join(__dirname, '../dist/index.html'))
  }

  mainWindow.on('closed', () => {
    mainWindow = null
  })

  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url)
    return { action: 'deny' }
  })
}

// ─── App Lifecycle ───────────────────────────────────────────

app.whenReady().then(async () => {
  createWindow()

  // Initialize core modules
  deviceManager = new DeviceManager()
  scrcpyServer = new ScrcpyServer()
  screencap = new ScreencapLegacy()
  inputController = new InputController(scrcpyServer)
  deviceHealth = new DeviceHealth()

  registerIpcHandlers()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('before-quit', async () => {
  screencap?.stopAll()
  deviceHealth?.stopAll()
  await scrcpyServer?.stopAll()
  deviceManager?.cleanup()
})

// ─── IPC Handlers ────────────────────────────────────────────

function registerIpcHandlers() {
  if (!mainWindow || !deviceManager || !screencap || !inputController || !scrcpyServer) return

  const win = mainWindow

  // ── Devices ────────────────────────────────────────────────

  ipcMain.handle('devices:list', async () => {
    return await deviceManager!.listDevices()
  })

  ipcMain.handle('devices:profile', async (_event, serial: string) => {
    return deviceManager!.getDeviceProfile(serial)
  })

  ipcMain.handle('devices:profile:update', async (_event, serial: string, profile: Record<string, unknown>) => {
    deviceManager!.updateDeviceProfile(serial, profile)
    return { success: true }
  })

  ipcMain.handle('devices:connect', async (_event, address: string) => {
    return await deviceManager!.connectDevice(address)
  })

  ipcMain.handle('devices:disconnect', async (_event, serial: string) => {
    return await deviceManager!.disconnectDevice(serial)
  })

  // ── Screen (Scrcpy Primary, Screencap Fallback) ───────────

  ipcMain.handle('screen:subscribe', async (_event, serial: string) => {
    try {
      // Try scrcpy first (30 FPS H.264)
      await scrcpyServer!.start(serial, (frame) => {
        win.webContents.send('device:frame', {
          serial: frame.serial,
          data: frame.data,
          width: frame.width,
          height: frame.height,
          timestamp: frame.timestamp,
          format: 'jpeg'
        })
      })
      win.webContents.send('device:stream_mode', { serial, mode: 'scrcpy' })
      return { success: true, mode: 'scrcpy' }
    } catch (err) {
      // Fallback to screencap (6 FPS PNG)
      console.warn(`[Screen] scrcpy failed for ${serial}, falling back to screencap:`, err)
      screencap!.startCapturing(serial, (frame) => {
        win.webContents.send('device:frame', frame)
      })
      win.webContents.send('device:stream_mode', { serial, mode: 'screencap' })
      return { success: true, mode: 'screencap' }
    }
  })

  ipcMain.handle('screen:unsubscribe', async (_event, serial: string) => {
    // Stop both scrcpy and screencap
    scrcpyServer!.stop(serial).catch(() => {})
    screencap!.stopCapturing(serial)
    return { success: true }
  })

  ipcMain.handle('screen:screenshot', async (_event, serial: string) => {
    // Always use screencap for single screenshots (faster one-off)
    return await screencap!.captureOnce(serial)
  })

  ipcMain.handle('screen:scrcpy_status', async (_event, serial: string) => {
    const session = scrcpyServer!.getSession(serial)
    return session ? { ...session, process: undefined, streams: undefined } : null
  })

  // ── Input ──────────────────────────────────────────────────

  ipcMain.handle('input:command', async (_event, command) => {
    return await inputController!.execute(command)
  })

  ipcMain.handle('input:broadcast', async (_event, serials: string[], command) => {
    return await inputController!.broadcast(serials, command)
  })

  // ── Window Controls ────────────────────────────────────────

  ipcMain.handle('window:minimize', () => win.minimize())
  ipcMain.handle('window:maximize', () => {
    if (win.isMaximized()) win.unmaximize()
    else win.maximize()
  })
  ipcMain.handle('window:close', () => win.close())
  ipcMain.handle('window:isMaximized', () => win.isMaximized())

  // ── Device Events (push from main) ─────────────────────────

  deviceManager.on('device:added', (device) => {
    win.webContents.send('device:added', device)
  })

  deviceManager.on('device:removed', (serial) => {
    win.webContents.send('device:removed', serial)
    // Cleanup scrcpy/screencap for removed device
    scrcpyServer!.stop(serial).catch(() => {})
    screencap!.stopCapturing(serial)
  })

  deviceManager.on('device:status', (serial, status) => {
    win.webContents.send('device:status', { serial, status })
  })

  // ── Health Monitoring ──────────────────────────────────────

  ipcMain.handle('health:start', async (_event, serial: string) => {
    deviceHealth!.startMonitoring(serial)
    return { success: true }
  })

  ipcMain.handle('health:stop', async (_event, serial: string) => {
    deviceHealth!.stopMonitoring(serial)
    return { success: true }
  })

  ipcMain.handle('health:snapshot', async (_event, serial: string) => {
    return deviceHealth!.getSnapshot(serial) || null
  })

  ipcMain.handle('health:all', async () => {
    const snapshots: Record<string, unknown> = {}
    for (const [serial, snap] of deviceHealth!.getAllSnapshots()) {
      snapshots[serial] = snap
    }
    return snapshots
  })

  // Forward health events to renderer
  deviceHealth!.on('battery:update', (data: { serial: string; battery: Record<string, unknown> }) => {
    win.webContents.send('health:battery', data)
  })

  deviceHealth!.on('storage:update', (data: { serial: string; storage: Record<string, unknown> }) => {
    win.webContents.send('health:storage', data)
  })

  deviceHealth!.on('alert', (alert) => {
    win.webContents.send('health:alert', alert)
  })

  deviceHealth!.on('health:snapshot', (snapshot) => {
    win.webContents.send('health:snapshot', snapshot)
  })

  // ── Device Groups ──────────────────────────────────────────

  ipcMain.handle('groups:list', async () => {
    const groups = deviceManager!.getAllGroups()
    return groups
  })

  ipcMain.handle('groups:create', async (_event, group) => {
    deviceManager!.createGroup(group)
    return { success: true }
  })

  ipcMain.handle('groups:update', async (_event, group) => {
    deviceManager!.updateGroup(group)
    return { success: true }
  })

  ipcMain.handle('groups:delete', async (_event, groupId: string) => {
    deviceManager!.deleteGroup(groupId)
    return { success: true }
  })

  ipcMain.handle('groups:assign', async (_event, serial: string, groupId: string) => {
    deviceManager!.assignToGroup(serial, groupId)
    return { success: true }
  })

  // ── Auto-health on device added ────────────────────────────

  deviceManager.on('device:added', (device) => {
    // Auto-start health monitoring
    deviceHealth!.startMonitoring(device.serial)
  })

  deviceManager.on('device:removed', (serial) => {
    deviceHealth!.stopMonitoring(serial)
  })
}
