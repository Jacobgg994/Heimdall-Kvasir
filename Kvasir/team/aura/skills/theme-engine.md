# Theme Engine — RRO / OMS / Monet Guide

## Overlay Types

| Type | System | Scope | Reboot Required |
|------|--------|-------|-----------------|
| **RRO** (Runtime Resource Overlay) | AOSP native | Single package | No (Android 8+) |
| **OMS** (Overlay Manager Service) | Substratum | System-wide | Partial |
| **Monet** (Material You) | Android 12+ | Dynamic color | No |

## RRO Overlays (AOSP Native)

### Structure
```
overlay/
└── <target-package>/
    ├── Android.mk              # Build definition
    └── res/
        └── values/
            ├── colors.xml      # Override colors
            ├── dimens.xml      # Override dimensions
            ├── strings.xml     # Override strings
            └── bools.xml       # Override booleans
```

### Key Flags
```makefile
LOCAL_IS_RUNTIME_RESOURCE_OVERLAY := true
# Priority: higher = takes precedence
LOCAL_OVERLAY_PACKAGES := framework-overlays-<codename>
```

### Example: System Theme Overlay
```xml
<!-- overlay/frameworks_base/res/values/colors.xml -->
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <!-- Accent color -->
    <color name="accent_device_default_light">#FF1A73E8</color>
    <color name="accent_device_default_dark">#FF8AB4F8</color>

    <!-- Background colors -->
    <color name="background_device_default">#FF1A1A2E</color>
    <color name="dark_mode_background_color">#FF16213E</color>
</resources>
```

## OMS / Substratum (Legacy)

### Substratum Builder
```xml
<!-- substratum.xml — define theme attributes -->
<theme>
    <name>Kvasir Dark</name>
    <author>NOVA Team</author>
    <targets>
        <target package="com.android.systemui" />
        <target package="android" />
        <target package="com.android.settings" />
    </targets>
</theme>
```

### OMS Type Layers
```
type1_overlay.xml — Base colors (system accent)
type3_overlay.xml — Navigation bar
type5_overlay.xml — Status bar icons
type6_overlay.xml — QS panel
```

## Monet / Material You (Android 12+)

### Sources for Dynamic Color
| Source | Description |
|--------|-------------|
| Wallpaper | Extract colors from current wallpaper |
| Accent color | User-selected accent |
| Wallpaper (light) | Light variant of wallpaper colors |
| Wallpaper (dark) | Dark variant |

### Override Monet Colors
```xml
<!-- frameworks/base/core/res/res/values/colors.xml -->
<!-- Force specific Monet palette -->
<color name="monet_accent">#FF1A73E8</color>
<color name="monet_accent2">#FF4285F4</color>
<color name="monet_neutral1">#FFF5F5F5</color>
<color name="monet_neutral2">#FFE0E0E0</color>
```

## Font Picker Implementation

```java
// packages/apps/Settings/src/com/android/settings/display/FontPickerActivity.java
private void applyFont(String fontPath) {
    try {
        // Copy font to /data/system/theme/fonts/
        // Update overlay for system font
        String overlayPath = "/data/overlay/themes/fonts/fonts-overlay.apk";
        // Trigger overlay manager
        IOverlayManager om = IOverlayManager.Stub.asInterface(
            ServiceManager.getService("overlay"));
        om.setEnabled("fonts-overlay", true, USER_ID);
    } catch (Exception e) {
        Log.e(TAG, "Failed to apply font", e);
    }
}
```

## Icon Shapes

| Shape | Value | Example ROM |
|-------|-------|-------------|
| System default | (empty) | Stock AOSP |
| Circle | `circle` | Pixel |
| Squircle | `squircle` | OnePlus |
| Rounded square | `rounded_rect` | Samsung |
| Teardrop | `teardrop` | Custom (popular) |

```xml
<!-- overlay for icon shape -->
<string name="config_icon_mask">"M -100,-100 L 100,-100 L 100,100 L -100,100 Z"</string>
```

## Testing Overlays

```bash
# List overlays
cmd overlay list

# Enable/disable specific overlay
cmd overlay enable <package-name>
cmd overlay disable <package-name>

# Check which overlays are active
cmd overlay info <target-package>
```
