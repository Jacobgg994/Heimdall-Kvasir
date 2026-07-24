# Bug Reporting — Debug Methods & Report Format

## Bug Report Template

```
## Bug: [Short descriptive title]

**Device**: <codename>
**Build**: kvasir_<device>-userdebug-<date>
**ROM Version**: KvasirOS 14.0-<build#>
**Severity**: Blocker / Critical / Major / Minor / Trivial

### Reproduction Steps
1. From home screen, open Settings
2. Navigate to Display → Brightness
3. Slide brightness to minimum
4. [Observed behavior]

### Expected Result
Display brightness decreases smoothly to minimum.

### Actual Result
Display brightness jumps to 0% suddenly — no smooth transition.
Screen flickers for 1-2 seconds before stabilizing.

### Logs
[Paste relevant logs below]

### Frequency
Always / Often (4/5) / Sometimes (2/5) / Rare (1/5)

### Screenshots/Videos
[Attach if applicable]

### Notes
Only reproduces after auto-brightness has been enabled once.
```

## Log Collection Methods

### Basic logcat
```bash
# Capture all logs since boot
adb logcat -b all -d > full_logcat_<device>_<date>.txt

# Filter by tag
adb logcat -s CameraHal:V

# Filter by priority
adb logcat *:E  # Errors only
adb logcat *:W  # Warnings and above

# Time-stamped log
adb logcat -v time > logcat_<device>_<date>.txt
# (Ctrl+C to stop)
```

### Kernel logs (dmesg)
```bash
# Full kernel ring buffer
adb shell dmesg > dmesg_<device>_<date>.txt

# Filter for panics/oops
adb shell dmesg | grep -E "panic|Oops|BUG|Unable to handle kernel"

# Filter for our driver
adb shell dmesg | grep -E "kvasir|hal|soc"
```

### Tombstone analysis
```bash
# List recent tombstones
adb shell ls -la /data/tombstones/

# Read latest tombstone
adb shell cat /data/tombstones/tombstone_00

# Key sections to look at:
# - "pid:" → process that crashed
# - "signal:" → signal number (11 = SIGSEGV)
# - "abi:" → architecture
# - backtrace → call stack
# - "stack:" → stack contents
```

### RAM dump
```bash
# Process memory map
adb shell dumpsys meminfo <package-name>

# Native heap
adb shell dumpsys meminfo --native <pid>

# Overall memory
adb shell cat /proc/meminfo
```

### Bugreport full dump
```bash
# Generate complete bug report (takes 30-60s)
adb bugreport bugreport_<device>_<date>.zip
# Contains: logcat, dmesg, dumpstate, dumpsys, ANR traces
```

## Common Debug Scenarios

### Scenario 1: App crash on launch
```bash
# Capture crash log
adb logcat -b crash -d
# Look for: "FATAL EXCEPTION", "Crash", "Force Closed"
# Check tombstone if native crash
```

### Scenario 2: WiFi not connecting
```bash
# WiFi debug log
adb logcat -s wpa_supplicant:V WifiHAL:V WifiService:V
# Also check: dmesg | grep wlan
```

### Scenario 3: Camera crash
```bash
# Camera HAL debug
adb logcat -s CameraHal:V CameraService:V
# Check HAL process
adb shell ps -A | grep camera
# Kill and restart camera HAL
adb shell killall cameraserver
```

### Scenario 4: Battery drain
```bash
# Battery stats
adb shell dumpsys batterystats > batterystats.txt
# Check wakelocks
adb shell dumpsys power
# Check kernel wakelocks
adb shell cat /proc/wakelocks
# Thermal throttling
adb shell dumpsys thermalservice
```

## ANR Trace Analysis

```bash
# Find ANR traces
adb shell ls -la /data/anr/
adb shell cat /data/anr/traces.txt

# Key information:
# - "ANR in <package>" → which app
# - "Reason: <reason>" → input dispatch timeout, broadcast timeout, etc.
# - "CPU usage" → overall system load
# - "main" thread → where the UI thread was stuck
```

## Bug Report Tagging

```
Platform: [AOSP/CAF/LineageOS]
Device:   [<codename>]
Type:     [Crash/Battery/Performance/UI/Feature/Regression]
Severity: [Blocker/Critical/Major/Minor/Trivial]
Status:   [New/Confirmed/In Progress/Fixed/Verified/Closed]
Assignee: [CYPHER/AURA/FORGE/FLUX/VECTOR/EMBER/NOVA]
```
