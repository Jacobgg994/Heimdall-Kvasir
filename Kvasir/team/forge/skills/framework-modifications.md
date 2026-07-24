# Framework Modifications — AOSP Framework Engineering

## Key Source Locations

| Layer | Path | What Lives Here |
|-------|------|-----------------|
| **System Server** | `frameworks/base/services/java/com/android/server/` | AMS, PMS, WMS, PowerMS |
| **Core framework** | `frameworks/base/core/java/android/` | Public API classes |
| **Services core** | `frameworks/base/services/core/java/com/android/server/` | System service implementations |
| **AIDL** | `frameworks/base/core/java/android/os/` | IPC interface definitions |

## Common Modification Patterns

### 1. Custom System Service

```java
// Step 1: Define AIDL interface
// frameworks/base/core/java/android/os/IKvasirService.aidl
interface IKvasirService {
    String getRomVersion();
    boolean isFeatureEnabled(String featureName);
}

// Step 2: Implement service
// frameworks/base/services/core/java/com/android/server/KvasirService.java
public class KvasirService extends IKvasirService.Stub {
    private static final String TAG = "KvasirService";
    private Context mContext;

    public KvasirService(Context context) {
        mContext = context;
    }

    @Override
    public String getRomVersion() {
        return SystemProperties.get("ro.kvasir.version", "unknown");
    }

    @Override
    public boolean isFeatureEnabled(String featureName) {
        return Settings.System.getInt(mContext.getContentResolver(),
            "kvasir_" + featureName, 0) == 1;
    }
}

// Step 3: Register in SystemServer.java
// frameworks/base/services/java/com/android/server/SystemServer.java
private void startKvasirService() {
    Slog.i(TAG, "Starting KvasirService");
    try {
        ServiceManager.addService("kvasir", new KvasirService(mSystemContext));
    } catch (Throwable e) {
        Slog.e(TAG, "Failed to start KvasirService", e);
    }
}
```

### 2. Signature Spoofing (MicroG Support)

```java
// frameworks/base/services/core/java/com/android/server/pm/PackageManagerService.java
// Allow certain packages to pretend to be other packages (for MicroG)

private boolean isSignatureAllowlisted(PackageSetting pkg) {
    // Check if package is in allowlist
    return allowlist.contains(pkg.name);
}

// Modify checkSignatures() to return MATCH when allowlisted
```

### 3. Expanded Volume Panel

```java
// frameworks/base/media/java/android/media/AudioService.java
// Add "advanced volume" mode with per-app volume control
private boolean mAdvancedVolumeEnabled;

public void setAdvancedVolumeEnabled(boolean enabled) {
    mAdvancedVolumeEnabled = enabled;
    // Trigger UI update in SystemUI
}
```

## Building After Framework Changes

```bash
# After modifying SystemServer or core framework
make -j$(nproc) 2>&1 | tee build.log

# Faster rebuild (if only services changed)
make services -j$(nproc)

# Flash
adb reboot bootloader
fastboot flash system system.img
fastboot reboot
```

## Testing Framework Changes

```bash
# Check system server started correctly
adb logcat -b system | grep SystemServer

# Check custom service registered
adb shell service list | grep kvasir

# Call custom service
adb shell service call kvasir 1  # getRomVersion()

# Check for ANRs
adb logcat -b events | grep am_anr
```

## CTS/GTS Safeguards

| Check | Command |
|-------|---------|
| CTS | `run cts --module CtsOsTestCases` |
| GTS | `run gts --module GtsGmsCoreHostTestCases` |
| Verify signature spoofing | `run cts -m CtsSignatureTestCases` |
