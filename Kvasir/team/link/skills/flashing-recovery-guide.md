---
name: flashing-recovery-guide
description: Samsung Odin flashing, Fastboot, TWRP, bootloader unlock/lock — ขั้นตอน + backup
metadata:
  type: skill
  category: device-control
  owner: link
---

# Flashing & Recovery Guide

> "Backup first. Flash second. Test always."

## Golden Rule: Backup Before Flash

**Never flash any device without a complete backup.** This is the #1 rule inherited from JIMMY's "Nothing is Deleted" principle.

### For Samsung Devices — TWRP Nandroid Backup

```bash
# 1. Boot into TWRP recovery
powershell.exe -Command "adb reboot recovery"
# OR (if already in download mode / using key combo)
# Power + Volume Up + Bixby for Samsung

# 2. In TWRP, perform nandroid backup via adb
powershell.exe -Command "adb shell twrp backup /sdcard/TWRP/BACKUPS/ --twrp-backup"

# Or use TWRP GUI:
# Backup → Select: System, Data, Boot, EFS, Modem → Swipe to Backup
# Store backup on external SD card AND copy to host machine
```

### For Samsung Devices — Odin Backup (Stock ROM)

Before flashing custom ROM, extract stock firmware:

```bash
# Use Heimdall (Linux/Odin alternative) to dump partitions
heimdall close-pc-screen
heimdall download-pit --output stock.pit

# Dump critical partitions
heimdall dump --BOOT boot.img --RECOVERY recovery.img \
  --SYSTEM system.img.ext4 --HIDDEN hidden.img.ext4 \
  --CSC csc.img.ext4 --CP modem.bin --EFS efs.img

# Archive
tar -czf stock-backup-$(date +%Y%m%d).tar.gz stock.pit *.img *.bin
```

## Samsung Odin Flashing (via Heimdall on Linux/WSL2)

### Overview
Samsung devices use **Odin protocol** for flashing. On Linux, use **Heimdall**. Our Note 8 fleet (SM-N950F) uses Exynos SoC — fully unlockable.

### Enter Download Mode
```bash
# Via ADB (if booted)
powershell.exe -Command "adb reboot download"

# Manual: Power Off → Volume Down + Bixby + Power → Volume Up to confirm
```

### Flash Stock ROM via Heimdall
```bash
# Install Heimdall
sudo apt install heimdall-flash

# Detect device
heimdall detect

# Flash full stock ROM (extract from Samsung firmware .tar.md5)
heimdall flash --BOOT boot.img --RECOVERY recovery.img \
  --SYSTEM system.img --USERDATA userdata.img \
  --HIDDEN hidden.img --CSC csc.img --CP modem.bin

# Or flash individual partitions
heimdall flash --RECOVERY twrp-3.7.0-greatlte.img
```

### Flash via Odin on Windows (native)
Since our USB hub connects through Windows, **using Odin on Windows directly** is sometimes more reliable:

```powershell
# On Windows (powershell.exe from WSL2)
& "C:\Odin3\Odin3.exe"

# Then in GUI:
# 1. Click BL → select BL_*.tar.md5
# 2. Click AP → select AP_*.tar.md5  
# 3. Click CP → select CP_*.tar.md5
# 4. Click CSC → select HOME_CSC_*.tar.md5 (preserves data)
# 5. Ensure "F.Reset Time" and "Auto Reboot" checked
# 6. Start
```

### Stock ROM Sources
| Model | Code | Source |
|-------|------|--------|
| SM-N950F | greatlte | [SamMobile](https://www.sammobile.com/samsung/galaxy-note-8/firmware/SM-N950F/) |
| SM-G990U | r9q | [SamFw](https://samfw.com/) |

## Fastboot Commands (Non-Samsung / AOSP)

Samsung uses Odin, not Fastboot. For the S21 FE (SM-G990U) and any future AOSP devices:

```bash
# Enter Fastboot mode
powershell.exe -Command "adb reboot bootloader"

# List devices
powershell.exe -Command "fastboot devices"

# Flash partitions
powershell.exe -Command "fastboot flash boot boot.img"
powershell.exe -Command "fastboot flash system system.img"
powershell.exe -Command "fastboot flash vendor vendor.img"

# Erase
powershell.exe -Command "fastboot erase userdata"
powershell.exe -Command "fastboot erase cache"

# Unlock bootloader
powershell.exe -Command "fastboot oem unlock"
# OR for newer devices
powershell.exe -Command "fastboot flashing unlock"

# Reboot
powershell.exe -Command "fastboot reboot"
```

## TWRP Installation

### Samsung (Note 8 — SM-N950F)

```bash
# Download TWRP for greatlte
# https://twrp.me/samsung/samsunggalaxynote8.html

# 1. Enable OEM Unlock in Developer Options
# Settings → Developer Options → OEM Unlock: ON

# 2. Reboot to Download Mode
powershell.exe -Command "adb reboot download"

# 3. Flash TWRP via Odin/Heimdall
heimdall flash --RECOVERY twrp-3.7.0_9-0-greatlte.img

# 4. IMMEDIATELY after flash, boot to recovery (key combo)
# Volume Up + Bixby + Power (hold until TWRP logo)
# Otherwise stock ROM will overwrite recovery!

# 5. In TWRP:
# - Allow modifications (swipe)
# - Wipe → Format Data (type "yes") — removes encryption
# - Reboot → Recovery (to verify TWRP persists)
```

### Verify TWRP Installation
```bash
# Inside TWRP, run via adb
powershell.exe -Command "adb shell twrp version"
# → TWRP 3.7.0

# Or check recovery partition hash
powershell.exe -Command "adb shell md5sum /dev/block/platform/.../by-name/RECOVERY"
```

## Bootloader Unlock / Lock

### Samsung (Exynos) — Unlock

```bash
# Method 1: Developer Options (Android 9+)
# Settings → Developer Options → OEM Unlock: ON

# Method 2: Download Mode toggle
# Reboot to Download Mode → Volume Up (long press) → Unlock bootloader

# Verify unlock status
powershell.exe -Command "adb shell getprop ro.boot.warranty_bit"
# 0 = unlocked, 1 = locked

powershell.exe -Command "adb shell getprop ro.boot.secure_hardware"
# Should return nothing or "0" for fully unlocked
```

### Samsung (Exynos) — Lock

```bash
# WARNING: Locking bootloader will wipe device!
# Only do this when returning to stock

# 1. Flash stock firmware via Odin (full, not HOME_CSC)
# 2. Reboot to Download Mode
# 3. Volume Down (long press) → Lock bootloader
# 4. Device will factory reset automatically
```

### Samsung (Snapdragon / S21 FE SM-G990U)

```bash
# US Snapdragon Samsung devices typically have LOCKED bootloaders
# SM-G990U is carrier-branded (US) — cannot unlock easily
# Check status:
powershell.exe -Command "adb shell getprop ro.boot.cpuid"
# If it returns a value, bootloader is locked

# For S21 FE SM-G990U:
# - Use ADB/root within existing ROM
# - Do NOT attempt bootloader unlock — risk of hard brick
# - Stock flash via Odin only (no custom recovery)
```

## Stock ROM Backup (Before Custom ROM)

Create a full backup set before flashing any custom ROM:

```bash
#!/bin/bash
# link-backup-device.sh — Full backup of one device

DEVICE=$1
BACKUP_DIR="/var/link/backups/$DEVICE-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "=== Backing up $DEVICE ==="

# 1. Partition table
powershell.exe -Command "adb -s $DEVICE shell cat /proc/partitions" > "$BACKUP_DIR/partitions.txt"

# 2. Build.prop (ROM info)
powershell.exe -Command "adb -s $DEVICE shell cat /system/build.prop" > "$BACKUP_DIR/build.prop"

# 3. Installed packages
powershell.exe -Command "adb -s $DEVICE shell pm list packages -f" > "$BACKUP_DIR/packages.txt"

# 4. Screen shot of current home
powershell.exe -Command "adb -s $DEVICE shell screencap -p /sdcard/screen.png"
powershell.exe -Command "adb -s $DEVICE pull /sdcard/screen.png $BACKUP_DIR/screen.png"

# 5. EFS partition (IMEI backup — CRITICAL!)
powershell.exe -Command "adb -s $DEVICE shell su -c 'dd if=/dev/block/platform/.../by-name/EFS of=/sdcard/efs-backup.img'"
powershell.exe -Command "adb -s $DEVICE pull /sdcard/efs-backup.img $BACKUP_DIR/efs-backup.img"

# 6. Radio/Modem firmware
powershell.exe -Command "adb -s $DEVICE shell su -c 'dd if=/dev/block/platform/.../by-name/RADIO of=/sdcard/modem-backup.img'"
powershell.exe -Command "adb -s $DEVICE pull /sdcard/modem-backup.img $BACKUP_DIR/modem-backup.img"

echo "=== Backup complete: $BACKUP_DIR ==="
```

## Post-Flash Workflow

After flashing a new ROM:

```bash
# 1. Initial setup (skip WiFi, skip Google sign-in)
# 2. Enable Developer Options (tap Build Number 7x)
# 3. Enable USB Debugging
settings put global development_settings_enabled 1
settings put global adb_enabled 1

# 4. Enable ADB over WiFi (for fleet management)
setprop service.adb.tcp.port 5555
stop adbd; start adbd

# 5. Install Magisk (if rooted ROM)
powershell.exe -Command "adb install Magisk-v28.1.apk"

# 6. Push Magisk boot script for WiFi ADB persistence
powershell.exe -Command "adb push wifi-adb.sh /data/adb/service.d/"
powershell.exe -Command "adb shell chmod 755 /data/adb/service.d/wifi-adb.sh"

# 7. Restore user data (if applicable)
# Via TWRP: Restore → select data backup → swipe
# Or: adb restore backup.ab

# 8. Verify
powershell.exe -Command "adb devices"
powershell.exe -Command "adb shell getprop ro.build.version.release"
powershell.exe -Command "adb shell su -c 'which magisk'"
```

## Emergency Recovery

### Device stuck in bootloop
```bash
# 1. Try booting to safe mode
# Volume Down during boot (Samsung logo)

# 2. Wipe cache from recovery
# Volume Up + Bixby + Power → Recovery → Wipe cache

# 3. If TWRP installed — restore nandroid
# TWRP → Restore → Select latest backup → Swipe to Restore

# 4. Last resort — reflash stock ROM via Odin
# Download Mode → Odin → Flash stock firmware
```

### Device won't enter Download Mode
```bash
# Try with USB jig (for older Samsung)
# OR use EDL cable (for Qualcomm devices like S21 FE)
# OR: Device may be hard bricked — need JTAG repair
```

### EFS corrupted (IMEI lost)
```bash
# If EFS partition gets corrupted:
# 1. Restore EFS from backup
powershell.exe -Command "adb shell su -c 'dd if=/sdcard/efs-backup.img of=/dev/block/platform/.../by-name/EFS'"

# 2. If no backup — restore modem firmware via Odin
# BL flash with combination firmware may restore EFS
```

## Samsung Device Reference

| Property | Note 8 (SM-N950F) | S21 FE (SM-G990U) |
|----------|-------------------|--------------------|
| SoC | Exynos 8895 | Snapdragon 888 |
| Rootable | Yes (Magisk) | Limited (locked BL) |
| Bootloader | Unlockable | Locked (US variant) |
| Recovery | TWRP available | Stock only |
| Flash Tool | Heimdall / Odin | Odin only |
| Protocol | Odin | Odin |
| Download Mode | Vol Down + Bixby + Power | Vol Down + Power |
| Current OS | Android 10 custom | Android 14 stock |

## Fleet Note 8 Partition Table (Reference)

```
Partition layout for SM-N950F (greatlte):

BLK          SIZE    NAME
mmcblk0p1    16M     PIT (partition info table)
mmcblk0p2    32M     BOOT (kernel + ramdisk)
mmcblk0p3    64M     RECOVERY (TWRP goes here)
mmcblk0p4    16M     EFS (IMEI — BACKUP THIS!)
mmcblk0p5    8M      MODEMST1
mmcblk0p6    8M      MODEMST2
mmcblk0p7    3GB     SYSTEM
mmcblk0p8    512M    VENDOR
mmcblk0p9    8GB     USERDATA (app data, internal storage)
mmcblk0p10   8M      RADIO (modem firmware)
mmcblk0p11   4M      PERSDATA
mmcblk0p12   8M      PARAM
```

## Common Mistakes

| Mistake | Consequence | Prevention |
|---------|-------------|-----------|
| Flashing without backup | Data loss, IMEI loss | Always full nandroid first |
| Not disabling FRP | Device locked to Google account | Remove Google accounts before flash |
| Wrong TWRP variant | Bootloop, recovery loop | Verify device code (greatlte for Note 8) |
| Flashing Snapdragon firmware on Exynos | Hard brick | Check model number before download |
| Disconnect during flash | Partition corruption | Use UPS, don't touch cables |
| Skip "OEM Unlock" | Only Download Mode works | Check Developer Options before flash |
| Boot to system after TWRP flash | Stock ROM overwrites recovery | IMMEDIATELY boot to recovery |
