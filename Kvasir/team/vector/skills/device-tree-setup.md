# Device Tree Setup — From Scratch

## Directory Initialization

```
device/<oem>/<codename>/
├── AndroidProducts.mk       # Must define PRODUCT_MAKEFILES
├── BoardConfig.mk           # SoC, kernel, partitions, flags
├── device.mk                # PRODUCT_PACKAGES, properties, overlays
├── system.prop              # build.prop additions
├── vendorsetup.sh           # add_lunch_combo
├── fstab.qcom               # Partition mount points
├── init/
│   ├── init.<codename>.rc   # init daemons, services, permissions
│   ├── init.recovery.<codename>.rc  # Recovery mode init
│   └── init.<codename>.usb.rc
├── overlay/                 # Resources overlay
│   └── frameworks/base/core/res/res/
│       └── values/
│           └── config.xml   # Device features
├── sepolicy/                # Device SELinux
├── keylayout/               # Input configuration
├── audio/                   # Audio configs
├── configs/                 # Media profiles, codecs
└── proprietary-files.txt    # Blob list
```

## BoardConfig.mk — Key Options

```makefile
# device/<oem>/<codename>/BoardConfig.mk

# SoC
TARGET_BOARD_PLATFORM := sm8250
TARGET_BOARD_PLATFORM_GPU := qcom-adreno650

# Architecture
TARGET_ARCH := arm64
TARGET_ARCH_VARIANT := armv8-2a
TARGET_CPU_ABI := arm64-v8a
TARGET_CPU_VARIANT := cortex-a76

# Kernel
TARGET_KERNEL_SOURCE := kernel/oneplus/sm8250
TARGET_KERNEL_CONFIG := vendor/<codename>_defconfig
TARGET_KERNEL_CLANG_COMPILE := true
BOARD_KERNEL_IMAGE_NAME := Image.gz
BOARD_KERNEL_PAGESIZE := 4096
BOARD_BOOT_HEADER_VERSION := 2
BOARD_MKBOOTIMG_ARGS += --header_version $(BOARD_BOOT_HEADER_VERSION)

# Partitions
BOARD_BOOTIMAGE_PARTITION_SIZE := 100663296
BOARD_SYSTEMIMAGE_PARTITION_SIZE := 4294967296
BOARD_VENDORIMAGE_PARTITION_SIZE := 1073741824
TARGET_COPY_OUT_VENDOR := vendor
BOARD_USES_PRODUCTIMAGE := true
TARGET_COPY_OUT_PRODUCT := product

# AVB (Verified Boot)
BOARD_AVB_ENABLE := true
BOARD_AVB_MAKE_VBMETA_IMAGE_ARGS += --flags 3
BOARD_AVB_RECOVERY_KEY_PATH := external/avb/test/data/testkey_rsa2048.pem

# Treble
BOARD_VNDK_VERSION := current
PRODUCT_FULL_TREBLE_OVERRIDE := true
```

## device.mk — Product Configuration

```makefile
# device/<oem>/<codename>/device.mk

$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/aosp_base_telephony.mk)
$(call inherit-product, device/<oem>/<codename>/device-vendor.mk)

# Overlays
DEVICE_PACKAGE_OVERLAYS += device/<oem>/<codename>/overlay

# Packages
PRODUCT_PACKAGES += \
    audio.r_submix.default \
    audio.usb.default \
    libaudiohal \
    libbt-vendor \
    sensors.$(TARGET_BOARD_PLATFORM)

# Permissions
PRODUCT_COPY_FILES += \
    frameworks/native/data/etc/android.hardware.camera.flash-autofocus.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.camera.flash-autofocus.xml \
    frameworks/native/data/etc/android.hardware.wifi.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.wifi.xml

# Properties
PRODUCT_PROPERTY_OVERRIDES += \
    ro.product.model=CustomDevice \
    ro.product.brand=<oem>
```

## fstab.qcom — Partition Mount Table

```
# device/<oem>/<codename>/fstab.qcom
#<src>                 <mnt_point>         <type>  <mnt_flags>                          <fs_mgr_flags>
/dev/block/by-name/system      /               ext4    ro,barrier=1                     wait,slotselect,avb
/dev/block/by-name/vendor      /vendor         ext4    ro,barrier=1                     wait,slotselect,avb
/dev/block/by-name/userdata    /data            f2fs    noatime,nosuid,nodev,errors=panic  wait,check,fileencryption=aes-256-xts
/dev/block/by-name/boot        /boot           emmc    defaults                          defaults
/dev/block/by-name/dtbo        /dtbo           emmc    defaults                          defaults
```

## Init Script — init.<codename>.rc

```rc
on init
    # Set permissions for device-specific nodes
    chmod 0660 /dev/kvasir_control
    chown system system /dev/kvasir_control

on boot
    # Start custom HAL
    start hal_kvasir

service hal_kvasir /vendor/bin/hw/kvasir_hal
    class hal
    user system
    group system
    seclabel u:r:hal_kvasir:s0
```

## Key Tests on First Boot

```bash
# Check partitions mounted
adb shell mount | grep -E "system|vendor|data"

# Check device tree applied
adb shell ls -la /dev/block/platform/

# Check init scripts ran
adb shell dmesg | grep init

# Check HAL processes
adb shell ps -A | grep hal
```
