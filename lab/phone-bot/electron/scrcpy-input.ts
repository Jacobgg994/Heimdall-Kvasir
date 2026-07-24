/**
 * Scrcpy Control Protocol — Binary message encoding
 *
 * Phase 1: Replaces adb shell input (700ms) with scrcpy control socket (5ms).
 *
 * Protocol reference: scrcpy v3.x ControlMessage types
 * Uses InputManager.injectInputEvent() via reflection on the device server.
 */

// Control Message Types
export const CONTROL_TYPE = {
  INJECT_KEYCODE: 0,
  INJECT_TEXT: 1,
  INJECT_TOUCH_EVENT: 2,
  INJECT_SCROLL_EVENT: 3,
  BACK_OR_SCREEN_ON: 4,
  EXPAND_NOTIFICATION_PANEL: 5,
  EXPAND_SETTINGS_PANEL: 6,
  COLLAPSE_PANELS: 7,
  GET_CLIPBOARD: 8,
  SET_CLIPBOARD: 9,
  SET_SCREEN_POWER_MODE: 10,
  ROTATE_DEVICE: 11
} as const

// Touch Action
export const TOUCH_ACTION = {
  DOWN: 0,
  UP: 1,
  MOVE: 2
} as const

// Keycode Action (Android KeyEvent actions)
export const KEYCODE_ACTION = {
  UP: 0,
  DOWN: 1
} as const

// Screen Power Mode
export const POWER_MODE = {
  OFF: 0,
  NORMAL: 1
} as const

/**
 * Encode a touch event (tap/click)
 */
export function encodeTouchEvent(
  action: number,
  pointerId: bigint,
  x: number,
  y: number,
  screenWidth: number,
  screenHeight: number,
  pressure: number = 65535
): Buffer {
  const buf = Buffer.alloc(27)

  let offset = 0
  buf.writeUInt8(CONTROL_TYPE.INJECT_TOUCH_EVENT, offset); offset += 1
  buf.writeUInt8(action, offset); offset += 1

  // Pointer ID (8 bytes, big-endian int64)
  buf.writeBigInt64BE(pointerId, offset); offset += 8

  // Position: point.x (int32) + point.y (int32)
  buf.writeInt32BE(Math.round(x), offset); offset += 4
  buf.writeInt32BE(Math.round(y), offset); offset += 4

  // Screen dimensions
  buf.writeUInt16BE(screenWidth, offset); offset += 2
  buf.writeUInt16BE(screenHeight, offset); offset += 2

  // Pressure (uint16)
  buf.writeUInt16BE(pressure, offset); offset += 2

  // Action button (int32, 0=PRIMARY)
  buf.writeInt32BE(0, offset)

  return buf
}

/**
 * Encode a swipe/scroll event (multi-touch drag)
 */
export function encodeScrollEvent(
  x: number,
  y: number,
  screenWidth: number,
  screenHeight: number,
  hScroll: number,
  vScroll: number,
  buttons: number = 0
): Buffer {
  const buf = Buffer.alloc(21)

  let offset = 0
  buf.writeUInt8(CONTROL_TYPE.INJECT_SCROLL_EVENT, offset); offset += 1
  buf.writeInt32BE(Math.round(x), offset); offset += 4
  buf.writeInt32BE(Math.round(y), offset); offset += 4
  buf.writeUInt16BE(screenWidth, offset); offset += 2
  buf.writeUInt16BE(screenHeight, offset); offset += 2
  buf.writeInt32BE(hScroll, offset); offset += 4
  buf.writeInt32BE(vScroll, offset); offset += 4
  buf.writeInt32BE(buttons, offset)

  return buf
}

/**
 * Encode a key event (Home, Back, Power, etc.)
 */
export function encodeKeyEvent(
  keycode: number,
  action: number = KEYCODE_ACTION.DOWN,
  repeat: number = 0,
  metaState: number = 0
): Buffer {
  const buf = Buffer.alloc(14)

  let offset = 0
  buf.writeUInt8(CONTROL_TYPE.INJECT_KEYCODE, offset); offset += 1
  buf.writeUInt8(action, offset); offset += 1
  buf.writeInt32BE(keycode, offset); offset += 4
  buf.writeInt32BE(repeat, offset); offset += 4
  buf.writeInt32BE(metaState, offset)

  return buf
}

/**
 * Encode a text input event
 */
export function encodeTextEvent(text: string): Buffer {
  const textBytes = Buffer.from(text, 'utf-8')
  const buf = Buffer.alloc(5 + textBytes.length)

  let offset = 0
  buf.writeUInt8(CONTROL_TYPE.INJECT_TEXT, offset); offset += 1
  buf.writeInt32BE(textBytes.length, offset); offset += 4
  textBytes.copy(buf, offset)

  return buf
}

/**
 * Encode Back button or Screen On
 */
export function encodeBackOrScreenOn(action: number): Buffer {
  const buf = Buffer.alloc(2)
  buf.writeUInt8(CONTROL_TYPE.BACK_OR_SCREEN_ON, 0)
  buf.writeUInt8(action, 1)  // 0=BACK, 1=SCREEN_ON
  return buf
}

/**
 * Encode screen power mode toggle
 */
export function encodePowerMode(mode: number): Buffer {
  const buf = Buffer.alloc(2)
  buf.writeUInt8(CONTROL_TYPE.SET_SCREEN_POWER_MODE, 0)
  buf.writeUInt8(mode, 1)  // 0=OFF, 1=NORMAL
  return buf
}

/**
 * Encode expand/collapse notification panel
 */
export function encodeExpandNotificationPanel(): Buffer {
  return Buffer.from([CONTROL_TYPE.EXPAND_NOTIFICATION_PANEL])
}

export function encodeExpandSettingsPanel(): Buffer {
  return Buffer.from([CONTROL_TYPE.EXPAND_SETTINGS_PANEL])
}

export function encodeCollapsePanels(): Buffer {
  return Buffer.from([CONTROL_TYPE.COLLAPSE_PANELS])
}

/**
 * Encode a complete tap (DOWN + UP) from coordinates
 */
export function encodeTap(x: number, y: number, screenWidth: number, screenHeight: number): Buffer {
  const pointerId = BigInt(0)
  const down = encodeTouchEvent(TOUCH_ACTION.DOWN, pointerId, x, y, screenWidth, screenHeight)
  const up = encodeTouchEvent(TOUCH_ACTION.UP, pointerId, x, y, screenWidth, screenHeight)
  return Buffer.concat([down, up])
}

/**
 * Encode a complete swipe with interpolated MOVE events
 */
export function encodeSwipe(
  x1: number, y1: number,
  x2: number, y2: number,
  screenWidth: number, screenHeight: number,
  durationMs: number = 300
): Buffer {
  const pointerId = BigInt(0)
  const steps = Math.max(5, Math.floor(durationMs / 16)) // ~60fps
  const chunks: Buffer[] = []

  // DOWN at start
  chunks.push(encodeTouchEvent(TOUCH_ACTION.DOWN, pointerId, x1, y1, screenWidth, screenHeight))

  // MOVE through interpolated positions
  for (let i = 1; i < steps; i++) {
    const t = i / steps
    const x = x1 + (x2 - x1) * t
    const y = y1 + (y2 - y1) * t
    chunks.push(encodeTouchEvent(TOUCH_ACTION.MOVE, pointerId, x, y, screenWidth, screenHeight))
  }

  // UP at end
  chunks.push(encodeTouchEvent(TOUCH_ACTION.UP, pointerId, x2, y2, screenWidth, screenHeight))

  return Buffer.concat(chunks)
}

/**
 * Known Android keycodes
 */
export const KEYCODE = {
  HOME: 3,
  BACK: 4,
  CALL: 5,
  ENDCALL: 6,
  VOLUME_UP: 24,
  VOLUME_DOWN: 25,
  POWER: 26,
  CAMERA: 27,
  CLEAR: 28,
  ENTER: 66,
  DEL: 67,
  MENU: 82,
  SEARCH: 84,
  RECENTS: 187,   // KEYCODE_APP_SWITCH
  NOTIFICATION: 83
} as const
