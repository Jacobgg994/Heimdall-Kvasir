---
name: android-rom-creation-guide
description: Step-by-step guide — สร้าง Custom Android ROM ใหม่ตั้งแต่ศูนย์ตามสเปคที่กำหนด
metadata: 
  node_type: memory
  type: reference
  created: 2026-07-23
  originSessionId: 97241c28-1ee0-48f0-84d7-9d2531437a7d
  modified: 2026-07-23T05:07:43.378Z
---

# 🏗️ สร้าง Custom Android ROM ใหม่ตั้งแต่ศูนย์

คู่มือสำหรับทีม NOVA — จากแผน/สเปค → โค้ด → flashable ROM

---

## Phase 1: วางแผน & กำหนดสเปค

### 1.1 ตอบคำถามก่อนเริ่ม

| คำถาม | ตัวอย่าง |
|--------|----------|
| **ชื่อ ROM?** | NovaOS, ThunderROM, ฯลฯ |
| **Base?** | AOSP version? (android-15.0.0_r1) หรือ fork จาก LineageOS/crDroid? |
| **Target devices?** | List devices + codename (เช่น Pixel 7 = panther) |
| **Features หลัก?** | Privacy, performance, gaming, battery, Pixel-like, etc. |
| **Google Apps?** | Vanilla (ไม่มี) หรือ GApps built-in? |
| **Root?** | Built-in หรือให้ user flash เอง? |
| **OTA?** | ใช้ OTA server ตัวไหน? |
| **Target user?** | ทั่วไป / power user / privacy-focused? |

### 1.2 Feature Specification Template

```markdown
## NovaOS v1.0 — Feature Spec

### Core
- [ ] Based on AOSP android-15.0.0_r1
- [ ] SELinux: Enforcing
- [ ] AVB: v2 with custom keys

### Performance
- [ ] Custom kernel with schedutil governor
- [ ] ADIOS I/O scheduler
- [ ] GPU driver: latest Adreno
- [ ] ZRAM + swap optimization

### UI/UX
- [ ] Custom boot animation
- [ ] Monet theme engine (Material You)
- [ ] Advanced restart menu
- [ ] Status bar customization
- [ ] Lock screen shortcuts

### Privacy/Security
- [ ] Network permission toggle
- [ ] Sensor permission toggle
- [ ] Sandboxed Google Play (optional)
- [ ] Firewall built-in

### Apps
- [ ] Custom launcher
- [ ] Custom camera app
- [ ] Remove AOSP bloat (Email, Browser, etc.)
- [ ] Add F-Droid (optional)
```

---

## Phase 2: Setup Build Environment

### 2.1 Hardware Requirements

| Spec | Minimum | Recommended |
|------|---------|-------------|
| CPU | 8 cores x86_64 | 16-32 cores |
| RAM | 16 GB | 32-64 GB |
| Disk | 400 GB SSD | 1 TB NVMe |
| OS | Ubuntu 22.04 LTS | Ubuntu 24.04 LTS |
| Network | 100 Mbps | 1 Gbps |

### 2.2 Install Dependencies

```bash
sudo apt update && sudo apt install -y \
  git gnupg flex bison gperf build-essential zip curl zlib1g-dev \
  gcc-multilib g++-multilib libc6-dev-i386 lib32ncurses5-dev \
  x11proto-core-dev libx11-dev lib32z-dev libgl1-mesa-dev \
  libxml2-utils xsltproc unzip python3 python3-pip ccache \
  libssl-dev libncurses5-dev libsqlite3-dev liblz4-tool \
  openjdk-11-jdk android-sdk-platform-tools
```

### 2.3 Install repo Tool

```bash
mkdir -p ~/bin
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
chmod a+x ~/bin/repo
echo 'export PATH=~/bin:$PATH' >> ~/.bashrc
```

### 2.4 Configure ccache (Optional but Recommended)

```bash
export USE_CCACHE=1
export CCACHE_EXEC=/usr/bin/ccache
ccache -M 100G
echo 'export USE_CCACHE=1' >> ~/.bashrc
```

---

## Phase 3: Create ROM Manifest & Download Source

### 3.1 Initialize Source Tree

```bash
mkdir -p ~/novaos
cd ~/novaos

# Option A: AOSP base
repo init -u https://android.googlesource.com/platform/manifest -b android-15.0.0_r1

# Option B: Fork from LineageOS
# repo init -u https://github.com/LineageOS/android.git -b lineage-22.0
```

### 3.2 Create ROM Manifest

สร้างไฟล์ `.repo/local_manifests/novaos.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest>

  <!-- Device Trees -->
  <project path="device/google/panther" name="NovaOS-Devices/android_device_google_panther" remote="github" revision="main" />
  <project path="device/google/gs201" name="NovaOS-Devices/android_device_google_gs201" remote="github" revision="main" />

  <!-- Kernel -->
  <project path="kernel/google/gs201" name="NovaOS-Devices/android_kernel_google_gs201" remote="github" revision="main" />

  <!-- Vendor Blobs -->
  <project path="vendor/google" name="NovaOS-Devices/proprietary_vendor_google" remote="github" revision="main" />

  <!-- Custom ROM Packages -->
  <project path="packages/apps/NovaSettings" name="NovaOS-Devices/android_packages_apps_NovaSettings" remote="github" revision="main" />
  <project path="vendor/nova" name="NovaOS-Devices/android_vendor_nova" remote="github" revision="main" />

  <!-- Remove AOSP packages -->
  <remove-project name="platform/packages/apps/Email" />
  <remove-project name="platform/packages/apps/Browser2" />

</manifest>
```

### 3.3 Sync Source

```bash
repo sync -j8 -c --no-tags --optimized-fetch
```

> ⏱️ ใช้เวลา 2-8 ชั่วโมง ขึ้นกับ internet

---

## Phase 4: สร้าง Device Tree

### 4.1 Directory Structure

```
device/<vendor>/<codename>/
├── Android.mk
├── AndroidProducts.mk
├── BoardConfig.mk
├── device.mk
├── proprietary-files.txt
├── overlay/
│   └── frameworks/base/core/res/res/values/config.xml
├── sepolicy/
│   ├── file_contexts
│   ├── genfs_contexts
│   └── *.te
├── configs/
│   ├── audio_policy_configuration.xml
│   └── media_profiles.xml
└── init/
    └── init.<device>.rc
```

### 4.2 Key Files

#### `AndroidProducts.mk`
```makefile
PRODUCT_MAKEFILES := \
    $(LOCAL_DIR)/nova_panther.mk

COMMON_LUNCH_CHOICES := \
    nova_panther-userdebug
```

#### `BoardConfig.mk`
```makefile
# Architecture
TARGET_ARCH := arm64
TARGET_ARCH_VARIANT := armv8-a
TARGET_CPU_ABI := arm64-v8a
TARGET_CPU_VARIANT := cortex-a55

# Kernel
TARGET_KERNEL_SOURCE := kernel/google/gs201
TARGET_KERNEL_CONFIG := nova_defconfig
BOARD_KERNEL_IMAGE_NAME := Image.lz4

# Partitions
BOARD_SYSTEMIMAGE_PARTITION_SIZE := 8589934592
BOARD_BOOTIMAGE_PARTITION_SIZE := 67108864

# SELinux
BOARD_VENDOR_SEPOLICY_DIRS += device/google/panther/sepolicy

# Features
TARGET_USES_HWC2 := true
TARGET_SUPPORTS_64_BIT_APPS := true
```

#### `device.mk`
```makefile
# Include GSI keys
$(call inherit-product, build/target/product/aosp_arm64.mk)

# Inherit nova common
$(call inherit-product, vendor/nova/config/common.mk)

# Device-specific
PRODUCT_NAME := nova_panther
PRODUCT_DEVICE := panther
PRODUCT_BRAND := Google
PRODUCT_MODEL := Pixel 7
PRODUCT_MANUFACTURER := Google

# HAL packages
PRODUCT_PACKAGES += \
    android.hardware.audio@7.0-impl \
    android.hardware.graphics.composer@2.4-service \
    android.hardware.camera.provider@2.6-service

# Device overlays
DEVICE_PACKAGE_OVERLAYS += device/google/panther/overlay
```

---

## Phase 5: Customize ROM Features

### 5.1 สร้าง ROM Config (`vendor/nova/config/common.mk`)

```makefile
# NovaOS Version
NOVA_VERSION := 1.0-alpha
NOVA_BUILD_DATE := $(shell date +%Y%m%d)
PRODUCT_SYSTEM_DEFAULT_PROPERTIES += \
    ro.nova.version=$(NOVA_VERSION) \
    ro.nova.build_date=$(NOVA_BUILD_DATE) \
    ro.nova.device=$(PRODUCT_DEVICE)

# Feature flags
PRODUCT_SYSTEM_DEFAULT_PROPERTIES += \
    persist.sys.nova.advanced_reboot=true \
    persist.sys.nova.network_traffic=true

# Prebuilt apps
PRODUCT_PACKAGES += \
    NovaSettings \
    NovaLauncher \
    NovaWallpapers

# Remove unwanted
PRODUCT_PACKAGES_REMOVE := \
    Email \
    Browser2 \
    MusicFX \
    Eleven
```

### 5.2 Modify Framework (ตัวอย่าง)

#### แก้ไข SystemUI (`frameworks/base/packages/SystemUI/`)

```java
// frameworks/base/packages/SystemUI/src/com/android/systemui/statusbar/phone/StatusBarFeatures.java
public class StatusBarFeatures {
    // Add custom feature flag
    public static boolean isNovaAdvancedRebootEnabled(Context context) {
        return Settings.System.getInt(context.getContentResolver(),
                "nova_advanced_reboot", 0) == 1;
    }
}
```

#### เพิ่ม Setting (`packages/apps/NovaSettings/`)

```xml
<!-- res/xml/nova_settings.xml -->
<PreferenceScreen>
    <PreferenceCategory android:title="Status Bar">
        <SwitchPreference
            android:key="nova_network_traffic"
            android:title="Network Traffic Monitor"
            android:defaultValue="false" />
        <SwitchPreference
            android:key="nova_advanced_reboot"
            android:title="Advanced Restart Menu"
            android:defaultValue="true" />
    </PreferenceCategory>
    <PreferenceCategory android:title="Lock Screen">
        <SwitchPreference
            android:key="nova_lockscreen_shortcuts"
            android:title="Lock Screen Shortcuts"
            android:defaultValue="true" />
    </PreferenceCategory>
</PreferenceScreen>
```

### 5.3 Custom Boot Animation

```bash
# วาง bootanimation.zip ใน:
vendor/nova/bootanimation/bootanimation.zip
```

### 5.4 Custom Wallpapers & Themes

```
vendor/nova/overlay/
└── frameworks/base/core/res/res/
    ├── drawable-nodpi/default_wallpaper.png
    └── values/colors.xml  → accent color, background
```

---

## Phase 6: Build ROM

### 6.1 Build Steps

```bash
cd ~/novaos

# Load build environment
source build/envsetup.sh

# Select target
lunch nova_panther-userdebug

# Build (clean)
make clobber
make -j$(nproc)

# OR incremental (faster after first build)
m -j$(nproc)
```

### 6.2 Build Output

```
out/target/product/panther/
├── system.img          ← system partition
├── boot.img            ← kernel + ramdisk
├── vendor.img          ← vendor partition
├── vbmeta.img          ← AVB metadata
├── dtbo.img            ← device tree overlay
└── nova_panther-ota-*.zip  ← flashable OTA
```

### 6.3 Build Optimization

```bash
# Multi-job build
m -j$(($(nproc) * 2))

# Build specific module only
mmm frameworks/base
mmm packages/apps/NovaSettings

# Push module directly to device (test)
adb root
adb remount
mmm packages/apps/NovaSettings && adb sync
```

---

## Phase 7: Test & Debug

### 7.1 Flash to Device

```bash
# Reboot to bootloader
adb reboot bootloader

# Flash images
fastboot flash boot boot.img
fastboot flash system system.img
fastboot flash vendor vendor.img
fastboot flash vbmeta vbmeta.img
fastboot reboot
```

### 7.2 Debug If Bootloop

```bash
# Watch boot process
adb wait-for-device && adb logcat | tee boot.log

# Kernel log
adb shell dmesg > dmesg.log

# Check init failures
adb shell cat /dev/kmsg

# Check SELinux denials
adb shell dmesg | grep -i "avc: denied"
```

### 7.3 Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Bootloop at logo | Kernel panic | Check dmesg, verify defconfig |
| Bootloop at animation | System server crash | Check logcat, fix missing HAL |
| No WiFi/BT | Missing firmware | Add to `proprietary-files.txt` |
| SELinux denials | Missing sepolicy rules | Add to `device/<vendor>/<codename>/sepolicy/` |
| Camera crash | Missing camera HAL | Check HAL implementation |
| SafetyNet fail | Props mismatch | Override build fingerprint |

---

## Phase 8: OTA Setup

### 8.1 Generate OTA Package

```bash
# Full OTA
make otapackage

# Incremental OTA (from previous build)
./build/tools/releasetools/ota_from_target_files \
    -i PREVIOUS-target_files.zip \
    NEW-target_files.zip \
    incremental_ota.zip
```

### 8.2 OTA Server Structure

```json
// ota.json
{
  "response": [
    {
      "datetime": 1690000000,
      "filename": "nova_panther-ota-v1.0-20260723.zip",
      "id": "abc123def456",
      "size": 1400000000,
      "url": "https://ota.novaos.dev/panther/nova_panther-ota-v1.0-20260723.zip",
      "version": "1.0"
    }
  ]
}
```

---

## Phase 9: Release Workflow

### 9.1 Checklist ก่อน Release

```
[ ] Build: userdebug → user (production)
[ ] SELinux: Enforcing mode
[ ] AVB: Signed with release keys (NOT test keys)
[ ] OTA: Tested full + incremental
[ ] Clean flash tested
[ ] Dirty flash from previous version tested
[ ] SafetyNet: Passes (ถ้าต้องการ)
[ ] All hardware works: WiFi, BT, Camera, GPS, NFC, Sensors
[ ] Battery: No excessive drain in idle
[ ] Performance: No ANR, no UI jank
```

### 9.2 Generate Signed Release

```bash
# Generate release keys
subject='/C=US/ST=California/L=Mountain View/O=NovaOS/OU=NovaOS/CN=NovaOS'
mkdir ~/.android-certs
for key in releasekey platform shared media networkstack testkey; do
    ./development/tools/make_key ~/.android-certs/$key "$subject"
done

# Build with release keys
export SIGNING_KEY_DIR=~/.android-certs
m -j$(nproc)
```

### 9.3 Versioning

```
MAJOR.MINOR.PATCH-BUILD_DATE-device

Example:
  1.0.0-20260723-panther     ← stable release
  1.1.0-20260725-panther     ← feature update
  1.1.1-20260726-panther     ← bug fix
```

---

## 📊 Project Timeline (ตัวอย่าง 12 Weeks)

| Week | Phase | Deliverable |
|------|-------|-------------|
| 1-2 | Setup + Source | Build environment ready, AOSP synced, manifest created |
| 3-4 | Device Tree | Device boots AOSP on target device |
| 5-6 | Kernel | Custom kernel boots, features added |
| 7-8 | Framework + UI | Custom features working, NovaSettings prototype |
| 9-10 | Polish | Bug fixes, performance optimization, sepolicy |
| 11 | Testing | QA on all target devices, bug bash |
| 12 | Release | v1.0 release, OTA live |

---

## 👥 Team Role Assignment

| Role | Phase รับผิดชอบ |
|------|----------------|
| **NOVA** ⚡ | Phase 1 (spec), Phase 9 (release) — ดูแลทั้งหมด |
| **CYPHER** 🔐 | Phase 5-6 — kernel dev, driver optimization |
| **AURA** ✨ | Phase 5 — System UI, boot animation, themes |
| **FORGE** 🏗️ | Phase 5 — framework modification, new APIs |
| **FLUX** 🔄 | Phase 2,3,6,8 — build system, CI/CD, OTA |
| **VECTOR** 🎯 | Phase 4,5,7 — device tree, HAL, vendor blobs, testing |
| **EMBER** 🔥 | Phase 7,9 — testing, bug reports, QA sign-off |

---

## 🔗 Resources

- [AOSP Build Docs](https://source.android.com/docs/setup/build)
- [LineageOS Build Guide](https://wiki.lineageos.org/devices/)
- [A-Dev Bringup Tool](https://github.com/Katya-Incorporated/A-Dev)
- [android-rom-book](https://github.com/feicong/android-rom-book)
- [[android-rom-learning-repos]] — learning repos for each role

**Why:** Complete build-from-scratch guide for custom Android ROM — from spec to release
**How to apply:** Follow phases in order; assign phases to team members per the role table
