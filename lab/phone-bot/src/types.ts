// Types shared between Main Process and Renderer

export interface DeviceInfo {
  serial: string
  model: string
  state: 'online' | 'offline' | 'busy' | 'unauthorized'
  transport: 'usb' | 'wifi'
  ip?: string
  port?: number
  androidVersion?: string
  resolution?: string
  screenWidth?: number
  screenHeight?: number
  battery?: DeviceBattery
  storage?: DeviceStorage
  tags: string[]
  groupId?: string
  notes: string
  lastSeen: number
  connectedAt: number
}

export interface DeviceBattery {
  level: number        // 0-100
  temperature: number  // Celsius
  charging: boolean
  health: string
  voltage: number
}

export interface DeviceStorage {
  total: number   // bytes
  used: number    // bytes
  free: number    // bytes
  percent: number // 0-100
}

export interface DeviceGroup {
  id: string
  name: string
  color: string
  deviceSerials: string[]
  createdAt: number
}

export interface DeviceProfile {
  serial: string
  tags: string[]
  notes: string
  location?: string
  proxy?: ProxyConfig
}

export interface ProxyConfig {
  host: string
  port: number
  type: 'http' | 'socks5'
  username?: string
  password?: string
}

export interface InputCommand {
  serial: string
  action: 'tap' | 'swipe' | 'text' | 'keyevent' | 'home' | 'back' | 'recents' | 'screenshot' | 'shell'
  x?: number
  xRandom?: number
  y?: number
  yRandom?: number
  x1?: number
  y1?: number
  x2?: number
  y2?: number
  duration?: number
  value?: string
  code?: number
  command?: string
}

export interface ScreenFrame {
  serial: string
  data: string        // base64 encoded image
  width: number
  height: number
  timestamp: number
  format: 'jpeg' | 'png'
}

export interface UINode {
  index: string
  text: string
  resourceId: string
  className: string
  package: string
  contentDesc: string
  checkable: boolean
  checked: boolean
  clickable: boolean
  enabled: boolean
  focusable: boolean
  focused: boolean
  scrollable: boolean
  longClickable: boolean
  password: boolean
  selected: boolean
  bounds: [number, number, number, number] // [left, top, right, bottom]
  children: UINode[]
}

export interface UIElementQuery {
  text?: string
  resourceId?: string
  contentDesc?: string
  className?: string
  package?: string
}

// Flow types v2
export interface FlowStep {
  action: string
  desc?: string
  selector?: UIElementQuery
  fallback?: FlowStep
  probability?: number
  timeout?: number
  // Tap
  x?: number
  xRandom?: number
  y?: number
  yRandom?: number
  // Swipe
  x1?: number
  y1?: number
  x2?: number
  y2?: number
  duration?: number
  durationRandom?: number
  // Text
  value?: string
  // Wait
  ms?: number
  msRandom?: number
  // Keyevent
  code?: number
  // App
  package?: string
  // Loop
  repeat?: { min: number; max: number }
  repeatInterval?: { min: number; max: number }
  // Shell
  command?: string
  // Children (for conditional/loop)
  steps?: FlowStep[]
}

export interface FlowDefinition {
  name: string
  version: number
  platform?: string
  orientation?: string
  resolution?: string
  randomization?: {
    coordinateJitter: number
    delayVariation: number
    startTimeWindow?: [number, number]
  }
  steps: FlowStep[]
  createdAt?: number
  updatedAt?: number
}

export interface FlowProgress {
  flowId: string
  flowName: string
  deviceSerial: string
  status: 'running' | 'paused' | 'completed' | 'failed' | 'stopped'
  currentStep: number
  totalSteps: number
  stepDesc: string
  startedAt: number
  error?: string
}

export interface DeviceHealthAlert {
  serial: string
  type: 'battery_temp' | 'battery_low' | 'storage_full' | 'offline' | 'app_crash' | 'reconnect'
  severity: 'info' | 'warning' | 'critical'
  message: string
  timestamp: number
}

// IPC channel type helpers
export interface IPCFrameEvent {
  serial: string
  data: string
  width: number
  height: number
  timestamp: number
  format: 'jpeg' | 'png'
}
