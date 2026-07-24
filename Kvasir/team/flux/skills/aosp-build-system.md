# AOSP Build System — Soong, Make, and Ninja

## Build Layers

```
Make (Android.mk) ──► Soong (Android.bp) ──► Ninja (.ninja) ──► Build Artifacts
     Legacy mods         Blueprint files          Build graph       .img / .zip
```

## Soong (Android.bp) — Blueprint System

### Basic Module Definition
```bp
// Android.bp
cc_binary {
    name: "kvasir_tool",
    srcs: ["src/main.cpp", "src/utils.cpp"],
    shared_libs: ["libbase", "liblog"],
    cflags: ["-Wall", "-Werror"],
    vendor: true,
}
```

### Module Types
| Type | Purpose |
|------|---------|
| `cc_binary` | C/C++ executable |
| `cc_library` | C/C++ shared/static library |
| `java_library` | Java library (.jar) |
| `android_app` | Android application (.apk) |
| `prebuilt_etc` | Prebuilt file (config, script) |
| `prebuilt_firmware` | Firmware image |

### Common Properties
```bp
android_app {
    name: "KvasirSettings",
    srcs: ["src/**/*.java"],
    platform_apis: true,       // Use system APIs
    certificate: "platform",   // Platform signature
    privileged: true,          // Install as privileged app
    required: ["libkvasir"],   // Dependency
    overrides: ["Settings"],   // Replace stock Settings
}
```

## Make (Android.mk) — Legacy but Still Used

```makefile
LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)

LOCAL_MODULE := KvasirSettings
LOCAL_SRC_FILES := $(call all-java-files-under, src)
LOCAL_PACKAGE_NAME := KvasirSettings
LOCAL_CERTIFICATE := platform
LOCAL_PRIVILEGED_MODULE := true
LOCAL_REQUIRED_MODULES := libkvasir

include $(BUILD_PACKAGE)
```

## PRODUCT_PACKAGES — Including Modules in ROM

```makefile
# device/<oem>/<codename>/device.mk

# Include apps in build
PRODUCT_PACKAGES += \
    KvasirSettings \
    KvasirWallpaper \
    CustomLauncher

# Include libraries
PRODUCT_PACKAGES += \
    libkvasir \
    libkvasir_jni
```

## inherit-product — Composition

```makefile
# device/<oem>/<codename>/device.mk

# Base AOSP product
$(call inherit-product, build/target/product/aosp_product.mk)
$(call inherit-product, build/target/product/treble_common.mk)

# SoC family
$(call inherit-product, device/qcom/sm8250/common.mk)

# Device specific
$(call inherit-product, device/<oem>/<codename>/device_kernel.mk)
$(call inherit-product, device/<oem>/<codename>/device_vendor.mk)
```

## Build Targets (Common)

```bash
# Full build
make bacon                    # Full OTA zip

# Individual images
make systemimage              # system.img
make vendorimage              # vendor.img
make bootimage                # boot.img (kernel + ramdisk)
make recoveryimage            # recovery.img
make dtboimage                # dtbo.img

# Modules
make KvasirSettings           # Single APK
make libkvasir                # Single library

# Partial rebuild
make snod                     # system.img - no deps check (fast!)
```

## Build Timing

```bash
# Profile build time
make -j$(nproc) 2>&1 | tee build.log

# Find slow targets
grep "seconds" build.log | sort -rn -k3 | head -20

# Check ninja build graph
ninja -f out/build-<target>.ninja -t stats
```

## CCache Configuration

```bash
# Setup ccache
export USE_CCACHE=1
export CCACHE_DIR=/mnt/ccache
prebuilts/misc/linux-x86/ccache/ccache -M 50G

# Check stats
prebuilts/misc/linux-x86/ccache/ccache -s

# Expected hit rate: 80-95% for incremental builds
```
