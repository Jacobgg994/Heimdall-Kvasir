# ROM Testing Checklist — Pre-Release

## Smoke Test (30 min)

| # | Test Case | Expected | Command / Method |
|---|-----------|----------|------------------|
| 1 | Device boots to home screen | Boot animation → home screen within 5 min | Power on, observe |
| 2 | Touch works | All touch zones responsive | Swipe, tap all areas |
| 3 | Display works | Colors correct, no artifacts, brightness adjustable | Change brightness, rotate |
| 4 | Buttons work | Power, volume up/down, any extra buttons | Press each button |
| 5 | ADB connects | `adb devices` shows device | `adb devices` |
| 6 | WiFi connects | Can connect to AP and get IP | Settings → WiFi |
| 7 | Basic phone call | Dialer opens, call connects | Call another device |
| 8 | 4G/5G data | Internet access via mobile data | Disable WiFi, browse |

## Functional Test (2 hr)

### Radio & Connectivity
| # | Test Case | Expected | Method |
|---|-----------|----------|--------|
| 1 | WiFi 2.4GHz + 5GHz | Both bands connect, stable | Connect each, check speed |
| 2 | Bluetooth pairing | Pair with known device, audio works | Pair with BT speaker |
| 3 | GPS lock | Lock within 30s, accuracy <10m | GPS Test app |
| 4 | NFC (if H/W) | Read tag, Android Beam | Test with tag |
| 5 | SIM detection | Both SIMs detected, correct carriers | Check settings |
| 6 | VoLTE/VoWiFi | Call over LTE/WiFi | Check status bar icons |
| 7 | Hotspot | Other device connects | Enable hotspot, connect |

### Camera
| # | Test Case | Expected | Method |
|---|-----------|----------|--------|
| 1 | Rear camera | Preview, capture, focus | Open camera app |
| 2 | Front camera | Switch, preview, capture | Switch to selfie |
| 3 | Video recording | Record 30s, playback | Record, play |
| 4 | Flash | Flash syncs with capture | Test with flash on/off |
| 5 | HDR | HDR effect visible | Compare HDR off/on |
| 6 | Portrait mode | Depth effect works | Take portrait photo |

### Sensors
| # | Test Case | Expected | Method |
|---|-----------|----------|--------|
| 1 | Accelerometer | Screen rotates with device | Rotate device |
| 2 | Gyroscope | Works in games/VR | Sensor Test app |
| 3 | Proximity | Screen off during call | Cover sensor during call |
| 4 | Light sensor | Auto brightness adjusts | Cover sensor, observe |
| 5 | Compass | Accurate direction | Maps app, check compass |
| 6 | Fingerprint | Enroll + unlock | Settings → Security |
| 7 | Face unlock | Enroll + unlock | Settings → Security |

### Audio
| # | Test Case | Expected | Method |
|---|-----------|----------|--------|
| 1 | Speaker | Clear audio during call/music | Play music |
| 2 | Headphone jack | Sound through headphones | Plug headphones |
| 3 | Bluetooth audio | Sound through BT device | Connect BT headphones |
| 4 | Microphone | Caller hears you clearly | Record voice memo |
| 5 | Speakerphone | Works during call | Toggle speakerphone |

## Battery Test (24 hr)

| Test | Duration | Method | Target |
|------|----------|--------|--------|
| Idle drain (WiFi) | 8hr | Airplane off, WiFi on, screen off | <0.8%/hr |
| Idle drain (Mobile) | 8hr | Airplane off, data on, screen off | <1.5%/hr |
| Screen-on drain | 2hr | 200 nits, YouTube playback | <12%/hr |
| Gaming drain | 1hr | 60fps game, max brightness | <20%/hr |
| Charging speed | Full charge | 0% to 100% | <90 min |
| Thermal throttling | 30min stress | CPU throttle test | No throttle >20% |

## Stability Test (72 hr)

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| Uptime | No reboot for 72hr | 72+ hours uptime |
| Memory leak | Check RAM usage trend | RAM steady, no climb |
| Random reboot | `adb logcat -b events \| grep -E "boot|crash|panic"` | 0 unexpected reboots |
| SystemUI restart | `adb logcat -b system \| grep SystemUI` | 0 SystemUI crashes |
| ANR | `adb logcat -b events \| grep am_anr` | 0 ANR events |
| SELinux denials | `adb logcat -b events \| grep avc` | 0 denials |

## Performance Test

| Metric | Tool | Target |
|--------|------|--------|
| Boot time (cold) | Stopwatch | <30s to home screen |
| App launch (Settings) | Manual | <1.5s |
| App launch (Camera) | Manual | <2s |
| UI jank (launcher) | GPU profiling | <3ms jank/frame |
| RAM available after boot | `adb shell dumpsys meminfo` | >30% of total RAM |
| Internal storage speed | AndroBench | >300MB/s sequential read |

## Release Gate Sign-off

```
Smoke Test:  _____  (PASS / FAIL)
Functional:  _____  (PASS / FAIL with X minor issues)
Battery:     _____  (PASS / WARN / FAIL)
Stability:   _____  (PASS / WARN with X known leaks)
Performance: _____  (PASS / WARN)
Overall:     _____  (SHIP / SHIP WITH NOTES / BLOCK)

Tester: EMBER
Date: _______________
```
