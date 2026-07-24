# SystemUI Customization — Practical Guide

## Source Locations

| Component | Path |
|-----------|------|
| SystemUI main | `frameworks/base/packages/SystemUI/` |
| Keyguard | `frameworks/base/packages/SystemUI/src/com/android/systemui/keyguard/` |
| Status bar | `frameworks/base/packages/SystemUI/src/com/android/systemui/statusbar/` |
| Quick Settings | `frameworks/base/packages/SystemUI/src/com/android/systemui/qs/` |
| Notification | `frameworks/base/packages/SystemUI/src/com/android/systemui/notification/` |
| Navigation bar | `frameworks/base/packages/SystemUI/src/com/android/systemui/navigationbar/` |

## Common Customizations

### 1. Clock Position

**Modification**: `frameworks/base/packages/SystemUI/src/com/android/systemui/statusbar/phone/ClockPositionController.java`

Options: Left (default AOSP), Center (Pixel style), Right (Samsung style), Hidden

```java
// Add preference for clock position
private int getClockPosition() {
    return Settings.System.getInt(mContext.getContentResolver(),
        "status_bar_clock_position", CLOCK_POSITION_RIGHT);
}
```

### 2. Battery Style

**Modification**: `frameworks/base/packages/SystemUI/src/com/android/systemui/BatteryMeterView.java`

Styles: Circle (with %), Bar, Text-only, Hidden, Plain icon

```java
// Add style enumeration
public enum BatteryStyle {
    DEFAULT, CIRCLE, TEXT, HIDDEN, BAR
}
```

### 3. Quick Settings Panel Layout

**Modification**: `frameworks/base/packages/SystemUI/src/com/android/systemui/qs/QSPanel.java`

| Property | Typical Setting |
|----------|----------------|
| Rows | 3 (default AOSP), 4 (custom) |
| Columns | 3 (default AOSP), 4-5 (custom) |
| Tile width | `qsTileWidth` in dimens.xml |

```xml
<!-- overlay/frameworks/base/core/res/res/values/dimens.xml -->
<dimen name="qs_tile_width">80dp</dimen>
<integer name="quick_settings_num_columns">4</integer>
```

### 4. Notification Panel

**Modification**: `frameworks/base/packages/SystemUI/src/com/android/systemui/statusbar/notification/NotificationShelfController.java`

Customization: Rounded corners, background color, media player layout

```xml
<!-- overlay for notification values -->
<dimen name="notification_corner_radius">16dp</dimen>
<dimen name="notification_header_height">48dp</dimen>
```

## Adding a New Quick Settings Tile

```java
// 1. Create tile class
package com.android.systemui.qs.tiles;

public class CustomTile extends QSTileImpl<BooleanState> {
    public CustomTile(Host host) {
        super(host);
    }

    @Override
    public BooleanState newTileState() {
        return new BooleanState();
    }

    @Override
    protected void handleClick() {
        // Toggle behavior
        mState.value = !mState.value;
        refreshState();
    }

    @Override
    public Intent getLongClickIntent() {
        return new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS);
    }

    @Override
    protected void handleUpdateState(BooleanState state, Object arg) {
        state.label = mContext.getString(R.string.quick_settings_custom);
        state.icon = ResourceIcon.get(R.drawable.ic_custom);
    }

    @Override
    public CharSequence getTileLabel() {
        return mContext.getString(R.string.quick_settings_custom);
    }
}

// 2. Register in SystemUI
// frameworks/base/packages/SystemUI/src/com/android/systemui/dagger/SystemUIModule.java
// Add to QS tile list
```

## RRO Overlay Example

```makefile
# device/<oem>/<codename>/overlay/systemui/Android.mk
LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)
LOCAL_MODULE := SystemUI-overlay-<codename>
LOCAL_PACKAGE_NAME := SystemUI-overlay-<codename>
LOCAL_IS_RUNTIME_RESOURCE_OVERLAY := true
LOCAL_SRC_FILES := $(call all-subdir-Java-files)
LOCAL_SDK_VERSION := current
include $(BUILD_PACKAGE)
```

```xml
<!-- overlay/systemui/res/values/dimens.xml -->
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <dimen name="status_bar_height">36dp</dimen>
    <dimen name="qs_panel_padding_top">8dp</dimen>
</resources>
```

## Testing

```bash
# Build and push
make SystemUI -j$(nproc) && \
adb root && adb remount && \
adb push $OUT/system/priv-app/SystemUI/SystemUI.apk /system/priv-app/SystemUI/ && \
adb reboot
```
