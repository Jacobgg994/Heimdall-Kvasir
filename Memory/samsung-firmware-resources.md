---
name: samsung-firmware-resources
description: "Samsung stock ROM download & flashing — samfw.com, Odin, TWRP, device bringup"
metadata: 
  node_type: memory
  type: reference
  created: 2026-07-23
  originSessionId: 97241c28-1ee0-48f0-84d7-9d2531437a7d
  modified: 2026-07-23T06:39:01.107Z
---

# 📱 Samsung Firmware — Stock ROM Download & Flashing

> **สำหรับทีม NOVA:** Samsung devices ใช้ Odin/Download Mode ไม่ใช่ fastboot — ต่างจาก Pixel/Xiaomi/OnePlus อย่างสิ้นเชิง

---

## 📥 samfw.com — Samsung Firmware Download

**URL:** https://samfw.com/

### วิธีโหลด
1. เข้า samfw.com
2. ใส่ **Model Number** (เช่น `SM-S928B`, `SM-G990B2`, `SM-X205`)
3. เลือก **CSC/Region** (Country Specific Code — เช่น `THL` = Thailand, `XSA` = Australia)
4. ดาวน์โหลดไฟล์ ZIP

### ไฟล์ที่ได้ (Samsung Firmware Format)

```
ZIP content → extract → .tar.md5 files:
  AP_XXXXX.tar.md5   ← System + Recovery + Kernel (ใหญ่สุด)
  BL_XXXXX.tar.md5   ← Bootloader
  CP_XXXXX.tar.md5   ← Modem/Baseband (ไม่มีถ้าเป็น WiFi-only)
  CSC_XXXXX.tar.md5  ← Consumer Software Customization (wipe data)
  HOME_CSC_XXXXX.tar.md5 ← CSC ที่ preserve data
```

### Samsung vs Google/Pixel Format

| Feature | Samsung | Google/Pixel |
|---------|---------|-------------|
| **Format** | `.tar.md5` (Odin) | `.img` (fastboot) |
| **Flash tool** | Odin (Windows) | fastboot (cross-platform) |
| **Download mode** | Vol Down + Vol Up → USB | Vol Down + Power → fastboot |
| **Partition scheme** | AP/BL/CP/CSC | boot/system/vendor/product |
| **Bootloader unlock** | OEM Unlock toggle | `fastboot flashing unlock` |
| **Warranty** | Knox eFuse 🔥 (irreversible) | Just bootloader state |
| **Firmware source** | samfw.com, SamMobile, Frija | Google Factory Images |

### Sites เปรียบเทียบ

| Site | Speed | Free | Notes |
|------|-------|------|-------|
| **samfw.com** | ⚡ Fast | ✅ Free | Recommended — direct download |
| **SamMobile** | 🐌 Slow | ✅ Free (throttled) | Premium for fast download |
| **Frija** | ⚡ Fast | ✅ Free | Windows tool — pulls from Samsung servers |
| **Bifrost** | ⚡ Fast | ✅ Free | Linux alternative to Frija |
| **Samsung Firmware Downloader** | ⚡ Fast | ✅ Free | Open-source Python tool |

---

## 🔧 Odin — Samsung Flash Tool

### Versions

| Version | Use For |
|---------|---------|
| **Odin 3.14.4** | Latest — S24, S23, newer devices |
| **Odin 3.13.1** | Legacy — older devices |
| **Patched Odin** | Cross-region flash, skip checks |

### Download Mode

```
Newer devices (no Bixby):
  1. Power off → hold Vol Down + Vol Up
  2. Connect USB cable → Warning screen → press Vol Up

Older devices (Bixby button):
  1. Power off → hold Vol Down + Bixby + Power
  2. Warning screen → press Vol Up
```

### Odin Slots

| Slot | File | Purpose |
|------|------|---------|
| **BL** | BL_*.tar.md5 | Bootloader |
| **AP** | AP_*.tar.md5 | System/Kernel/Recovery (largest, slowest to load) |
| **CP** | CP_*.tar.md5 | Modem/Baseband |
| **CSC** | CSC_*.tar.md5 | Full reset + region config |
| **USERDATA** | (rare) | User data image |

### Flashing Steps
```bash
# 1. Install Samsung USB Drivers
# 2. Boot to Download Mode
# 3. Open Odin as Administrator
# 4. Load firmware into slots:
#    BL  ← BL_*.tar.md5
#    AP  ← AP_*.tar.md5
#    CP  ← CP_*.tar.md5
#    CSC ← CSC_*.tar.md5 (factory reset) OR HOME_CSC_*.tar.md5 (keep data)
# 5. Options: ☑ Auto Reboot  ☑ F. Reset Time
# 6. Click Start → wait for PASS! (green)
```

### ⚠️ Critical Warnings

| Warning | Detail |
|---------|--------|
| **Bootloader Downgrade** | ดูตัวอักษรที่ 5 ใน firmware string → ห้าม flash firmware ที่มี binary version ต่ำกว่า |
| **Knox eFuse** | ถ้า Knox แตก → Samsung Pay, Secure Folder, Samsung Pass พังถาวร เปลี่ยนเมนบอร์ดอย่างเดียว |
| **CSC vs HOME_CSC** | `CSC_` = wipe data เสมอ / `HOME_CSC_` = เก็บ data (แต่อาจเกิด bug) |
| **Wrong Model** | ถ้า flash firmware ผิดรุ่น → brick (กู้ด้วย Odin + firmware ที่ถูกต้อง) |

---

## 🛠️ SamFw FRP Tool

Windows tool สำหรับ:
- **FRP Bypass** (Factory Reset Protection) — Android 5-14
- **Screen Lock Removal** — PIN/password/pattern โดยไม่ wipe
- **CSC Change** — เปลี่ยน region
- **Odin Integration** — launch Odin directly

> ⚠️ ฟรีสำหรับ security patches ก่อน พ.ย. 2022 / เสียเงินสำหรับ device ใหม่กว่า
> ⚠️ Windows เท่านั้น

---

## 🔓 TWRP on Samsung — Device Tree Bringup

### Samsung ≠ AOSP

Samsung devices ไม่ใช้ `fastboot flash` เหมือน Pixel:
- ใช้ **Odin** + `.tar.md5` files
- Recovery อยู่ใน `vendor_boot` (Android 12+) แทน `recovery` partition
- **Knox** ต้อง disable สำหรับ custom binaries

### TWRP Build Process for Samsung

```bash
# 1. Init TWRP manifest
repo init -u https://github.com/minimal-manifest-twrp/platform_manifest_twrp_aosp.git -b twrp-12.1

# 2. Clone Samsung device tree
git clone https://github.com/<dev>/android_device_samsung_<codename> device/samsung/<codename>

# 3. Build vendor_boot (NOT recovery!)
source build/envsetup.sh
export ALLOW_MISSING_DEPENDENCIES=true
lunch twrp_<codename>-eng
mka vendorbootimage

# 4. Package for Odin
tar -cvf twrp-vendor_boot.tar vendor_boot.img

# 5. Flash via Odin
# Load twrp-vendor_boot.tar into AP slot → Start
```

### Key Samsung Differences for ROM Devs

| Aspect | Samsung | Other Android |
|--------|---------|---------------|
| **Flash protocol** | Odin (proprietary) | fastboot (standard) |
| **Image format** | tar.md5 | .img (raw/sparse) |
| **Partition table** | PIT file | GPT |
| **Recovery location** | vendor_boot (new) | recovery / boot |
| **Bootloader unlock** | KG state + OEM toggle | `fastboot flashing unlock` |
| **Anti-rollback** | SW REV (bit in bootloader) | AVB rollback index |
| **Vendor blobs** | proprietary .img + CSC | vendor.img |
| **eSIM/Fused components** | Knox + TEEGRIS (Samsung TEE) | Trusty/OP-TEE |
| **Kernel** | Samsung's own branch | AOSP common kernel |

---

## 📦 Vendor Blob Extraction from Samsung Firmware

```bash
# 1. Extract AP tar
tar -xvf AP_*.tar.md5

# 2. Convert sparse system.img to raw
simg2img system.img system_raw.img

# 3. Mount
sudo mount -o loop system_raw.img /mnt/samsung_system

# 4. Extract proprietary files
# vendor/ → HAL libraries, firmware, configs
# product/ → Samsung apps, overlays
# system/ → framework jars, permissions

# 5. Extract vendor.img (if separate)
simg2img vendor.img vendor_raw.img
sudo mount -o loop vendor_raw.img /mnt/samsung_vendor
```

### Samsung-Specific Blobs

```
Key Samsung proprietary components:
  vendor/lib64/hw/
    ├── audio.primary.exynos*.so    ← Samsung audio HAL
    ├── camera.exynos*.so           ← Samsung camera HAL
    ├── gralloc.exynos*.so          ← Samsung GPU allocator
    ├── hwcomposer.exynos*.so       ← Samsung display composer
    └── memtrack.exynos*.so         ← Samsung memory tracker

  vendor/firmware/
    ├── modem.bin                   ← Shannon baseband firmware
    ├── dsp/                        ← Samsung DSP firmware
    └── sec_s3fw*.bin               ← Samsung security firmware

  vendor/etc/
    ├── init/                       ← Samsung init scripts (.rc)
    ├── selinux/                    ← Samsung SEPolicy extensions
    └── vintf/                      ← Samsung HAL manifests
```

---

## 🔗 Key Resources

| Resource | URL |
|----------|-----|
| **samfw.com** | https://samfw.com — stock firmware download |
| **Frija** | https://github.com/SlackingVeteran/frija — firmware download tool |
| **Bifrost** | https://github.com/zacharee/SamloaderKotlin — Linux firmware downloader |
| **Odin 3.14.4** | Search XDA for latest |
| **TWRP Builder** | https://github.com/twrp-recovery-builder-2024 |
| **Samsung Device Trees** | GitHub search: `android_device_samsung_` |
| **XDA Samsung Forums** | https://xdaforums.com/c/samsung/ |

---

**Why:** Samsung firmware download + flashing is completely different from Pixel/standard AOSP devices. Team NOVA needs this knowledge for Samsung device support.
**How to apply:** VECTOR uses this to extract Samsung vendor blobs; CYPHER uses this for Samsung kernel development; AURA uses CSC overlays for regional customization.
