# Vendor Blob Extraction — From Stock ROM

## Extraction Methods

### Method 1: extract-files.sh (LineageOS-style)
```bash
# From a running device with stock ROM
cd device/<oem>/<codename>
./extract-files.sh /path/to/lineage/device/oneplus/sm8250

# Or pull from connected device
./extract-files.sh
# This reads proprietary-files.txt and pulls from device via adb
```

### Method 2: From stock firmware image
```bash
# Extract system.img from stock firmware
mkdir stock_system
sudo mount -o loop system.img stock_system

# Copy blobs per proprietary-files.txt
while IFS='|' read -r src dst; do
    cp "stock_system/$src" "vendor/$dst"
done < proprietary-files.txt

sudo umount stock_system
```

### Method 3: From OTA zip
```bash
# Extract OTA payload
python ota_extractor.py ota.zip extracted/
# ota_extractor.py: https://github.com/cyngn/brunch/blob/master/tools/ota_extractor
```

## proprietary-files.txt Format

```
# Lines format:
# Source path (in stock) | Destination path (in vendor tree)
#
# Comments start with #

# Device-specific blobs
/system/vendor/lib64/libvulkan.so|vendor/lib64/libvulkan.so
/system/vendor/lib64/hw/camera.sm8250.so|vendor/lib64/hw/camera.sm8250.so
/system/vendor/firmware/a530_zap.b00|vendor/firmware/a530_zap.b00

# Skip if not found with #
# /system/vendor/lib64/hw/gps.sm8250.so|vendor/lib64/hw/gps.sm8250.so
```

## Blob Versioning

### Why version blobs?
- Different stock ROM versions have different blob compatibility
- Camera blobs from Android 12 might not work on Android 14
- Need to track which stock firmware version blobs came from

### Version tracking
```bash
# Store blob metadata
echo "Extracted from: OnePlus 9 Pro OxygenOS 14.0.1" > vendor/<oem>/<codename>/BLOB_INFO
cat vendor/<oem>/<codename>/BLOB_INFO
# Extracted from: OnePlus 9 Pro OxygenOS 14.0.1
# Date: 2026-07-24
# SHA256: <system.img hash>
```

### Blob directory structure
```
vendor/<oem>/<codename>/
├── proprietary/
│   ├── system/        # Blobs that go to /system
│   └── vendor/        # Blobs that go to /vendor
├── BLOB_INFO          # Extraction metadata
├── Android.mk         # Makefile for proprietary libs
└── Android.bp         # Blueprint for proprietary libs
```

## ABI Compatibility Check

```bash
# Check ELF dependencies
readelf -d vendor/lib64/hw/camera.sm8250.so | grep NEEDED

# Check missing symbols on target
adb push vendor/lib64/hw/camera.sm8250.so /data/local/tmp/
adb shell "cd /data/local/tmp && LD_LIBRARY_PATH=. ldd camera.sm8250.so"

# Check VNDK ABI compatibility
./development/vndk/tools/abi-diff/abi-diff \
  --old-lib old_camera.sm8250.so \
  --new-lib new_camera.sm8250.so
```

## Common Blob Issues

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `dlopen failed: cannot locate symbol` | Missing dependency library | Find and include the missing .so |
| `FATAL: didn't find <class>` | Wrong SDK version | Extract blobs from correct Android version |
| `SIGILL (illegal instruction)` | CPU feature mismatch | Check TARGET_CPU_VARIANT |
| `dlopen failed: has text relocations` | Android 10+ linker restriction | Remove text relocations (or use WRITE_ABI) |
| `HAL init failed: -22 (EINVAL)` | ABI mismatch between HAL and framework | Match VNDK version |

## Blob Cleanup Script

```bash
#!/bin/bash
# cleanup-blobs.sh — Remove unnecessary blobs

while IFS='|' read -r src dst; do
    if [ -f "$dst" ]; then
        # Check if blob is needed (referenced in device tree or other blobs)
        grep -r "$(basename $dst)" device/ vendor/ 2>/dev/null | grep -v "$dst"
        if [ $? -eq 0 ]; then
            echo "KEEP: $dst"
        else
            echo "UNUSED: $dst — removing"
            rm "$dst"
        fi
    fi
done < proprietary-files.txt
```
