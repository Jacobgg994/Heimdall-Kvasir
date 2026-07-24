# ROM Architecture — Reference

## Partition Layout (Typical AOSP)

| Partition | Mount Point | Contents |
|-----------|-------------|----------|
| `system` | `/system` | Core OS — frameworks, apps, libraries |
| `system_ext` | `/system_ext` | OEM/vendor extensions to system |
| `product` | `/product` | Device-specific product customizations |
| `vendor` | `/vendor` | HALs, firmware, proprietary blobs |
| `odm` | `/ odm` | Original Design Manufacturer customizations |
| `vbmeta` | — | Verified boot metadata |
| `boot` | — | Kernel + ramdisk |
| `dtbo` | — | Device Tree Blob Overlay |

## Build Types

### user (production)
```
ro.debuggable=0
ro.secure=1
adb root=disabled
```
- For end-user releases
- No root access
- Production signing keys

### userdebug (development)
```
ro.debuggable=1
ro.secure=1
adb root=restricted (via adb root when ro.debuggable=1)
```
- For internal testing
- ADB root available
- Test-keys signed

### eng (engineering)
```
ro.debuggable=1
ro.secure=0
adb root=enabled
```
- For early bringup
- Full root access
- No performance optimizations

## How to Set

In `device/<oem>/<codename>/device.mk`:
```makefile
# Override build type behavior
ifeq ($(TARGET_BUILD_VARIANT),user)
PRODUCT_SYSTEM_DEFAULT_PROPERTIES += \
    ro.adb.secure=1 \
    persist.sys.usb.config=none
endif
```

## AOSP Build Targets

```bash
# Clean build
make clean && make -j$(nproc)

# Specific targets
make bootimage        # Kernel + ramdisk only
make systemimage      # system partition only
make vendorimage      # vendor partition only

# Combined
make otapackage       # Full OTA zip
```

## SELinux Contexts on Partitions

| Partition | File Contexts |
|-----------|--------------|
| system | `system_file_contexts` |
| vendor | `vendor_file_contexts` |
| odm | ` odm_file_contexts` |
| product | `product_file_contexts` |

## VNDK / LL-NDK

- **VNDK** (Vendor Native Development Kit) — vendor-facing NDK libraries
- **LL-NDK** (Low-Level NDK) — low-level vendor APIs
- Must match between AOSP version and vendor blobs
- Check: `ls $OUT/system/lib64/vndk-*`
