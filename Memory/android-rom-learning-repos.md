---
name: android-rom-learning-repos
description: Learning resources & reference repos for Android ROM team (7 members)
metadata: 
  node_type: memory
  type: reference
  created: 2026-07-23
  originSessionId: 97241c28-1ee0-48f0-84d7-9d2531437a7d
  modified: 2026-07-23T05:15:14.738Z
---

# 📚 Android ROM Team — Learning Resources

Curated GitHub repos, docs, and tools for each team member to study.

---

## 🧭 NOVA ⚡ — Android ROM Lead (Overall Architecture)

**ต้องรู้ทุกส่วน:** ภาพรวม AOSP, ROM architecture, device bringup workflow, release strategy

### เริ่มต้นที่นี่
| Repo | Description | Stars |
|------|-------------|-------|
| [Akipe/awesome-android-aosp](https://github.com/Akipe/awesome-android-aosp) | curated list ของทุก resource ด้าน AOSP/ROM | ⭐314 |
| [ErrorxCode/AOSP-wikipedia](https://github.com/ErrorxCode/AOSP-wikipedia) | ultimate hub สำหรับ AOSP custom ROM guide | — |
| [karthik558/AOSP-Build-Resource](https://github.com/karthik558/AOSP-Build-Resource) | ขั้นตอน build AOSP พื้นฐาน, prerequisites, troubleshooting | ⭐30 |

### Porting & Bringup
| Repo | Description |
|------|-------------|
| [rajdeep-3305/android-porting-guide](https://github.com/rajdeep-3305/android-porting-guide) | all-in-one guide: porting ROM, GSI, recovery, debug, bootloop fixes |
| [Katya-Incorporated/A-Dev](https://github.com/Katya-Incorporated/A-Dev) | device bringup tool by kdrag0n — เร็วกว่า extract-utils 2000% |
| [LineageOS Wiki — Adding a Device](https://wiki.lineageos.org/addingdevice-howto) | official guide การเพิ่ม device ใหม่ |

### ROM ตัวอย่างให้ศึกษา
| ROM | Description |
|-----|-------------|
| [LineageOS](https://github.com/LineageOS) | ROM ต้นแบบ — ศึกษา structure, device tree, build system |
| [TrebleDroid/device_phh_treble](https://github.com/TrebleDroid/device_phh_treble) | GSI device tree สำหรับ Treble-compatible devices |
| [AxionAOSP](https://github.com/AxionAOSP) | AOSP derivative — ดูว่า custom ROM จัดโครงสร้างยังไง |

---

## 🔐 CYPHER 🔐 — Kernel Engineer

**เน้น:** Custom kernel, drivers, toolchain, GKI, optimization

### Tutorials
| Repo | Description | Stars |
|------|-------------|-------|
| [ravindu644/Android-Kernel-Tutorials](https://github.com/ravindu644/Android-Kernel-Tutorials) | สอน build kernel แบบ step-by-step สำหรับมือใหม่ — GKI/non-GKI, Docker, signed boot images | ⭐high |
| [itewqq/android-kernel-play](https://github.com/itewqq/android-kernel-play) | kernel development notes — syscalls, LKM, Kconfig, anti-debug, VSCode+clangd setup | — |

### Build Tools & CI
| Repo | Description |
|------|-------------|
| [shoey63/Kernel-Builder-GKI-Susfs](https://github.com/shoey63/Kernel-Builder-GKI-Susfs) | GitHub Actions สร้าง GKI kernel อัตโนมัติ + KernelSU, SUSFS, WireGuard |
| [migit439/android-kernel-builder](https://github.com/migit439/android-kernel-builder) | GitHub Action builder อ่าน config จาก JSON — รองรับ KernelSU, AnyKernel3 |

### Official Docs
| Doc | Link |
|-----|------|
| AOSP — Build Kernels | https://source.android.com/docs/setup/build/building-kernels |
| AOSP — Build Pixel Kernels | https://source.android.com/docs/setup/build/building-pixel-kernels |
| GKI Overview | https://source.android.com/docs/core/architecture/kernel/generic-kernel-image |

### Kernel Sources ตัวอย่าง
| Source | Description |
|--------|-------------|
| [AOSP Kernel Manifests](https://android.googlesource.com/kernel/manifests) | official kernel manifests |
| [LineageOS Kernel Trees](https://github.com/LineageOS?q=android_kernel) | ดู kernel trees จาก LineageOS หลาย devices |

---

## ✨ AURA ✨ — System UI Engineer

**เน้น:** Notification panel, QS, lock screen, themes, animations

### Theme & Customization Engines
| Repo | Description | Stars |
|------|-------------|-------|
| [luisbocanegra/substratum-tweaks](https://github.com/luisbocanegra/substratum-tweaks) | Substratum theme สำหรับ tweak resource values — status bar, QS, rounded corners, blur | — |
| [Red-A-Hawk/Iconify](https://github.com/Red-A-Hawk/Iconify) | ปรับแต่ง UI แบบละเอียด — QS tiles, notification, media player, volume panel | ⭐high |
| [jareddantis/eviltheme](https://github.com/jareddantis/eviltheme) | Enhanced VRTheme Engine — mod resources โดยไม่ต้องแทนที่ APK, รองรับ Magisk systemless | — |
| [pranavpandey/dynamic-theme](https://github.com/pranavpandey/dynamic-theme) | JSON-based theme engine — ใช้เป็น reference สร้าง theme engine เอง | ⭐1.6k |

### AOSP Modding
| Repo | Description |
|------|-------------|
| [dttzyjw0012/AospXpert](https://github.com/dttzyjw0012/AospXpert) | Xposed+Magisk module — status bar, QS, lock screen, gestures บน AOSP 12-16 |
| [pranavpandey/dynamic-support](https://github.com/pranavpandey/dynamic-support) | Java library — runtime theme switching engine |

### Official Reference
| Repo | Link |
|------|------|
| AOSP SystemUI | https://android.googlesource.com/platform/frameworks/base/+/master/packages/SystemUI/ |
| Monet (Material You) | https://github.com/monet-engine |

### Case Study: ROM Theme Systems
- **DotOS Dynamic Theming** — MonetCompat-based ใช้ wallpaper เป็น source
- **crDroid** — customization-rich ROM
- **Pixel Experience** — ดูว่าจัดการ Pixel-exclusive UI features ยังไง
- **Evolution X** — feature-rich system UI modifications

---

## 🏗️ FORGE 🏗️ — Framework Engineer

**เน้น:** AOSP framework, System Server, services, API compatibility, security patches

### AOSP Framework Source
| Repo | Link |
|------|------|
| AOSP frameworks/base | https://android.googlesource.com/platform/frameworks/base/ |
| AOSP System Server | https://android.googlesource.com/platform/frameworks/base/+/master/services/ |
| AOSP Settings | https://android.googlesource.com/platform/packages/apps/Settings/ |

### Learning
| Resource | Description |
|----------|-------------|
| [AOSP Code Search](https://cs.android.com) | search AOSP source code |
| [Android Framework Internals](https://source.android.com/docs/core) | official docs — architecture, services, HAL |
| [Romain Guy's Blog](https://www.curious-creature.com/) | Android graphics/framework internals |
| [dttzyjw0012/AospXpert](https://github.com/dttzyjw0012/AospXpert) | ตัวอย่างจริงของ framework modding ผ่าน Xposed |

### HAL & Framework Bridge
| Repo | Description |
|------|-------------|
| [Halium Project](https://github.com/Halium) | HAL abstraction layer — เรียนการ bridge framework ↔ HAL |
| [TrebleDroid/device_phh_treble](https://github.com/TrebleDroid/device_phh_treble) | GSI framework patches |

### Security
| Resource | Link |
|----------|------|
| AOSP Security Bulletins | https://source.android.com/docs/security/bulletin |
| Monthly Patch Backports | https://android.googlesource.com/platform/frameworks/base/ — follow monthly security tags |

---

## 🔄 FLUX 🔄 — Build/CI Engineer

**เน้น:** Soong, Ninja, Make, CI/CD, OTA update, build optimization

### Build System Official
| Repo | Description |
|------|-------------|
| [aosp-mirror/platform_build](https://github.com/aosp-mirror/platform_build) | AOSP build system (Soong, Kati, Ninja) |
| [AxionAOSP/android_build](https://github.com/AxionAOSP/android_build) | build system mirror |
| [google/ninja-to-soong](https://github.com/google/ninja-to-soong) | แปลง Ninja → Soong (ใช้ integrate external projects) |

### Build Tools
| Tool | Description |
|------|-------------|
| [iusmac/ContainerizedAndroidBuilder](https://github.com/iusmac/ContainerizedAndroidBuilder) | containerized TUI builder — build ROM ใน Docker |
| [antony-jr/ham](https://github.com/antony-jr/ham) | Hetzner Android Make — ใช้ Hetzner Cloud build ROM <€1/build |
| [NachtsternBuild/fastboot-assistant](https://github.com/NachtsternBuild/fastboot-assistant) | GTK tool — flash ROM/GSI |

### CI/CD
| Resource | Description |
|----------|-------------|
| GitHub Actions — AOSP builds | ดู workflow ตัวอย่างจาก [AxionAOSP](https://github.com/AxionAOSP) |
| [Jenkins + AOSP](https://source.android.com/docs/setup/build/jack) | (legacy) build farm reference |

### Official Docs
| Doc | Link |
|-----|------|
| AOSP Build System | https://source.android.com/docs/setup/build |
| Soong (Blueprint) | https://android.googlesource.com/platform/build/soong/ |
| OTA Updates | https://source.android.com/docs/core/ota |
| Ninja Build | https://ninja-build.org/manual.html |

---

## 🎯 VECTOR 🎯 — HAL/Device Tree Engineer

**เน้น:** Device tree, HAL implementation, vendor blobs, bringup devices ใหม่

### Device Tree ตัวอย่าง (Gold Standard)
| Repo | Description |
|------|-------------|
| [LineageOS/android_device_motorola_pnangn](https://github.com/LineageOS/android_device_motorola_pnangn) | official LineageOS device tree (Moto G 5G 2024) — ตัวอย่างสมบูรณ์ |
| [josexda/device_motorola_devon](https://github.com/JoseXda/device_motorola_devon) | community device tree — สะอาด, จัด structure ดี |

### Device Bringup Tools
| Repo | Description |
|------|-------------|
| [YZBruh/LineageOS-Tree-Generator](https://github.com/YZBruh/LineageOS-Tree-Generator) | สร้าง device tree อัตโนมัติจาก ROM dump |
| [Katya-Incorporated/A-Dev](https://github.com/Katya-Incorporated/A-Dev) | bringup tool — extract blobs, resolve build rules, fix VINTF manifests |
| [JLST-LG845/local_manifests](https://github.com/JLST-LG845/local_manifests) | local manifests + bringup scripts + build error fixes |

### HAL Reference
| Repo | Description |
|------|-------------|
| [TrebleDroid/device_phh_treble](https://github.com/TrebleDroid/device_phh_treble) | GSI HAL implementations — audio, NFC, sensors, charger, sepolicy |
| [Halium Docs](https://github.com/Halium/docs) | HAL porting guide — init, get sources, integrate |
| [Halium/android_device_halium_halium_arm64](https://github.com/Halium/android_device_halium_halium_arm64) | generic Halium device tree (buildable) |

### Vendor Blobs
| Resource | Description |
|----------|-------------|
| [TheMuppets (GitHub)](https://github.com/TheMuppets) | vendor blobs collection — ดูว่า extract และ structure ยังไง |
| [LineageOS extract-utils](https://github.com/LineageOS/android_tools_extract-utils) | script ดึง blobs จาก device |

### Device Trees ตาม SoC
| Platform | Resource |
|----------|----------|
| Snapdragon 8xx | [sm8450-mainline/fdt](https://github.com/sm8450-mainline/fdt) — device trees from MIUI, HyperOS, LineageOS |
| MediaTek | [mt8163 GitHub Org](https://github.com/mt8163) — device/kernel/vendor/hardware trees |

---

## 🔥 EMBER 🔥 — QA & Device Testing

**เน้น:** ROM testing, bug reports, test automation, stability/performance

### UI Testing Frameworks
| Repo | Description | Stars |
|------|-------------|-------|
| [KasperskyLab/Kaspresso](https://github.com/KasperskyLab/Kaspresso) | Android UI test framework — Espresso+UI Automator, screenshot tests, Allure reports, ADB | ⭐1.8k |
| [security-pride/LLMDroid](https://github.com/security-pride/LLMDroid) | LLM-powered GUI testing — ต่อยอด Droidbot/Humanoid/Fastbot2 + code coverage | — |

### Android System Testing
| Tool | Description |
|------|-------------|
| [Autotest (AOSP)](https://android.git.googlesource.com/platform/external/autotest/) | ChromeOS/Android integration testing — on-device tests, lab infra |
| [Robolectric](http://robolectric.org) | JVM unit tests — เร็ว ไม่ต้อง emulator |

### QA Automation
| Repo | Description |
|------|-------------|
| [Harzva/android-release-emulator-qa-skill](https://github.com/Harzva/android-release-emulator-qa-skill) | automated QA checks: install, screenshots, UI XML dump, logcat, SHA256 |
| [BoykaFramework/boyka-framework](https://github.com/BoykaFramework/boyka-framework) | cross-platform test automation — Android, iOS, desktop, API |

### Performance Testing
| Tool | Description |
|------|-------------|
| Android Profiler | built-in — CPU, memory, network, battery |
| [Perfetto](https://perfetto.dev) | system-wide profiling |
| [Systrace](https://developer.android.com/topic/performance/tracing) | kernel + userspace tracing |

### Bug Tracking Template
```
## Bug Report — [Device] [ROM Version]

**Severity:** Critical / High / Medium / Low
**Device:** [model, SoC, RAM]
**Build:** [build date / version]

### Steps to Reproduce
1. ...
2. ...

### Expected Behavior
...

### Actual Behavior
...

### Logs
- logcat: [attach]
- dmesg: [attach]
- tombstone: [attach]

### Screenshots / Video
[attach]
```

---

## 📖 ทุกตำแหน่ง — Resources กลางที่ทุกคนควรอ่าน

| Resource | Why |
|----------|-----|
| [AOSP Source](https://source.android.com) | official docs — ตั้งแต่ build จนถึง security |
| [LineageOS Wiki](https://wiki.lineageos.org) | คู่มือ ROM development ที่ดีที่สุด |
| [XDA University](https://xdaforums.com/t/xda-university) | community knowledge base |
| [Android Code Search](https://cs.android.com) | search ได้ทุก repos ของ AOSP |
| [AOSP Gerrit](https://android-review.googlesource.com) | ดู code review, commits, patches |

---

## 📺 YouTube Channels & Video Courses

### ช่อง YouTube
| Channel | Description |
|---------|-------------|
| [@aosp-devs](https://www.youtube.com/@aosp-devs) | FOSDEM 2025 talks — Android 15 HALs, AIDL, APEX, VNDK |
| [Build Custom Android ROM Playlist](https://www.youtube.com/watch?v=d8JhwX-cdDQ&list=PLQcIdsw6jRy2Et-TES3VitOQKx733WkG) | สอน build ROM แบบ step-by-step |
| AlaskaLinuxUser (via XDA) | Zero to Hero — จากไม่มี device tree จน build ROM ได้ |
| [AOSP — Android OS Internals Series](https://www.youtube.com/playlist?list=PLWz5rJ2EKKc_El_x5LFgTjB0DqFmPax2W) | ลงลึก AOSP structure |

### คอร์ส Udemy (มีค่าใช้จ่าย)
| Course | Focus | Updated |
|--------|-------|---------|
| [Android OS Internals / AOSP Automotive ROM Development](https://www.udemy.com/course/android-os-internals-aosp-automotive-development/) | AOSP environment, Car Settings, System UI, SELinux, boot | May 2025 |
| Android OS Internals / AOSP Mobile ROM Development | Mobile AOSP ROM | — |
| Android OS Internals / AOSP in Depth | AMS, WMS, System UI, boot process | — |

---

## 📚 หนังสือแนะนำ

| หนังสือ | โฟกัส | ปี |
|---------|-------|-----|
| **[Inside the Android OS](https://www.pearson.com/en-au/subject-catalog/p/inside-the-android-os-building-customizing-managing-and-operating-android-system-services/P200000009535/9780134096414)** — Meike & Schiefer | ทันสมัยที่สุด — AOSP build, boot, HAL, Treble, ART, security | 2021 |
| **[Embedded Android](https://www.oreilly.com/library/view/embedded-android/9781449327958/)** — Karim Yaghmour (O'Reilly) | Classic — Linux↔Android bridge, internals primer, build system, HAL | 2013 |
| **[Learning Embedded Android N Programming](https://www.packtpub.com/product/learning-embedded-android-n-programming/9781785282881)** | Hands-on — ROM customization, kitchen tools, boot animation | 2016 |
| [android-rom-book (feicong)](https://github.com/feicong/android-rom-book) | หนังสือ Open-source ภาษาจีน — AOSP customization จากศูนย์ | ⭐660+ |

---

## 🔐 SELinux & Security Hardening

### Official & Reference
| Resource | Description |
|----------|-------------|
| [AOSP SELinux](https://source.android.com/docs/security/features/selinux) | official docs |
| [GrapheneOS/platform_system_sepolicy](https://github.com/GrapheneOS/platform_system_sepolicy) | ตัวอย่าง sepolicy ที่เข้มงวด — ใช้เป็น gold standard |
| [AxionAOSP/android_system_sepolicy](https://github.com/AxionAOSP/android_system_sepolicy) | custom ROM sepolicy reference |
| [aosPB-Project/system_sepolicy](https://github.com/aosPB-Project/system_sepolicy) | PixelBuilds sepolicy — ดูว่า Pixel-specific จัดการยังไง |

### การ Config Device SEPolicy
```makefile
# ใน BoardConfig.mk
BOARD_VENDOR_SEPOLICY_DIRS += device/<vendor>/<board>/sepolicy
SYSTEM_EXT_PUBLIC_SEPOLICY_DIRS += device/<vendor>/<board>/sepolicy/systemext/public
SYSTEM_EXT_PRIVATE_SEPOLICY_DIRS += device/<vendor>/<board>/sepolicy/systemext/private
PRODUCT_PUBLIC_SEPOLICY_DIRS += device/<vendor>/<board>/sepolicy/product/public
PRODUCT_PRIVATE_SEPOLICY_DIRS += device/<vendor>/<board>/sepolicy/product/private
BOARD_SEPOLICY_M4DEFS += btmodule=foomatic btdevice=/dev/gps
```

### Kernel Hardening
| Resource | Description |
|----------|-------------|
| CFI (Control Flow Integrity) | aarch64 BTI/PAC — kernel protection |
| XN (Execute Never) | ป้องกัน code execution ใน data pages |
| BPF LSM (Linux Security Module) | ใช้ eBPF ป้องกัน privilege escalation |
| LEMON | eBPF-based memory acquisition บน hardened Android |

---

## 🔓 Root Solutions — Internals & Development

ทีม ROM ควรเข้าใจ root solutions ทุกตัวเพื่อ integration และ debugging:

| Solution | Mechanism | Source |
|----------|-----------|--------|
| **[Magisk](https://github.com/topjohnwu/Magisk)** | Ramdisk patch (userspace) | ต้นตำรับ — systemless root |
| **[KernelSU](https://github.com/tiann/KernelSU)** | Kernel module (GKI), `prctl()` syscall | kernel-based — ใช้บน GKI devices |
| **[APatch](https://github.com/bmax121/APatch)** | Kernel kprobe/kpatch, SuperKey | hybrid — ไม่ต้องใช้ kernel source ⭐4,500+ |
| **[ReZygisk](https://github.com/PerformanC/ReZygisk)** | open-source Zygisk replacement | C-based — รองรับ Magisk+KernelSU+APatch |
| **[Kam](https://github.com/MemDeco-WG/Kam)** | build toolchain — สร้าง module ครั้งเดียวใช้ได้ทุก root | CLI + templates |

### Understanding Zygisk
Zygisk คือ API ของ Magisk ที่ inject code เข้า Zygote process → ทุก app process ได้รับ injection
- ใช้ทำ module ที่ hook ระบบ เช่น safety net bypass, adblock
- ReZygisk เป็น open-source alternative (Zygisk Next กลายเป็น closed-source)

---

## 🪲 Dynamic Analysis & Debugging Tools

### Frida Ecosystem
| Tool | Description |
|------|-------------|
| [Frida](https://frida.re) | Dynamic instrumentation — hook Java/Native, trace syscalls |
| [Objection](https://github.com/sensepost/objection) | Runtime exploration toolkit บน Frida — bypass SSL pinning, root detection |
| [frida-tools](https://github.com/frida/frida-tools) | CLI: `frida-trace`, `frida-ps`, `frida-ls-devices` |
| [m0bilesecurity/Frida-Mobile-Scripts](https://github.com/m0bilesecurity/Frida-Mobile-Scripts) | collection of Frida scripts for mobile |

### Reverse Engineering
| Tool | Description |
|------|-------------|
| [APKTool](https://github.com/iBotPeaches/Apktool) | decompile/recompile APK — Smali, resources, manifest |
| [JADX](https://github.com/skylot/jadx) | decompile APK → Java/Kotlin source |
| [android-reverse-starter](https://github.com/vladkalyuzhny/android-reverse-starter) | bash scripts — automate decompile↔modify↔recompile↔sign |
| [APKLab (VS Code)](https://marketplace.visualstudio.com/items?itemName=Surendrajat.apklab) | VS Code extension — full Smali editing workflow |

### ADB & System Debugging
| Tool | Description |
|------|-------------|
| `adb logcat` | system-wide logs |
| `adb bugreport` | full system dump (logs, dumpsys, meminfo, etc.) |
| `dumpsys` | dump any system service state |
| `strace` | trace syscalls (attach to process) |
| [Perfetto](https://perfetto.dev) | system-wide trace — CPU, GPU, memory, I/O, binder |
| [Simpleperf](https://developer.android.com/ndk/guides/simpleperf) | CPU performance profiler |

---

## ⚡ Performance Optimization Deep Dive

### CPU Governor Tuning
| Governor | Use Case | Tuning |
|----------|----------|--------|
| **schedutil** | default EAS governor | `iowait_boost_enable=1`, `rate_limit_us=0` |
| **interactive** | legacy governor | `timer_slack=-1` |
| **performance** | max throughput | locks CPU at max freq |
| **Reflex CPUFreq** | custom ROM | advanced freq scaling |
| **blu_active** (blu_spark) | balanced perf/battery | — |

### I/O Scheduler
| Scheduler | Description |
|-----------|-------------|
| **ADIOS** (Adaptive Deadline I/O Scheduler) v3.2 | ปรับปรุง random read IOPS ได้ถึง 10% |
| **CFQ** | ตั้งค่า `rq_affinity=2`, `iostats=0`, `read_ahead=128KB` |
| **bfq** | multi-queue fairness |

### GPU Driver Tuning
| Parameter | Path | Effect |
|-----------|------|--------|
| Throttling disable | `/sys/class/kgsl/kgsl-3d0/throttling = 0` | ปิด thermal throttle → FPS boost |
| Power level | `/sys/class/kgsl/kgsl-3d0/default_pwrlevel` | 0 = max, N = lower |
| Bus split | `/sys/class/kgsl/kgsl-3d0/bus_split = 0` | keep GPU+memory coupled |
| Idle timeout | `/sys/class/kgsl/kgsl-3d0/idle_timer` | 58ms — เร็วขึ้น |
| Adreno driver upgrade | V@762.36 OGL, Vulkan 1.3.128 | ใหม่กว่า stock |

### Tuning Tools
| Tool | Description |
|------|-------------|
| [IDroidTweaks](https://github.com/rakarmp/IDroidTweaks) | Magisk module — GPU, governor, I/O, HWUI, memory |
| [Origami Kernel Manager](https://explore.market.dev/ecosystems/shell/projects/origami_kernel_manager) | Termux CLI — CPU/GPU freq, DRAM, charging |
| ZeetaaTweak | shell script — governor params, GPU, I/O, stune boost |

### Custom Kernels ตัวอย่าง (เรียนจากของจริง)
| Kernel | จุดเด่น |
|--------|---------|
| **Franco Kernel** | max performance |
| **Sultan Kernel** | battery life |
| **kirisakura** | gaming — aggressive GPU scaling |
| **blu_spark** | balanced — battery+perf |

---

## 🏗️ Project Treble, GSI, APEX, Mainline

### APEX (Android Pony EXpress)
- Container format ตั้งแต่ Android 10 — update system components ผ่าน Play Store
- ไฟล์ `.apex` = ZIP (uncompressed, 4KB aligned) → `apex_payload.img` (ext4 + dm-verity)
- `apexd` daemon — verify, install, activate (ต้อง reboot)
- **Pre-installed**: `/system/apex`, **Updated**: `/data/apex`
- ต้องการ Kernel 4.4+, loop driver, dm-verity

### Mainline Modules (APEX format)
| Module | อัปเดตอะไร |
|--------|-----------|
| `com.android.runtime` | ART, bionic libc, linker |
| `com.android.tzdata` | timezone, ICU |
| `com.android.media` | media frameworks |
| `com.android.conscrypt` | TLS/SSL |
| `com.android.resolv` | DNS resolver |

### GSI (Generic System Image)
- [TrebleDroid/device_phh_treble](https://github.com/TrebleDroid/device_phh_treble) — GSI device tree
- [TrebleDroid/platform_system_apex](https://github.com/TrebleDroid/platform_system_apex) — APEX for GSI
- Flattened APEX → Image APEX (Android 13+)

---

## 🔄 Android Boot Process — Complete Chain (Internals Deep Dive)

```
Power ON → Boot ROM → Bootloader → Linux Kernel → Init (PID 1)
  → Zygote (app_process64) → System Server → Launcher
```

### Init (PID 1) — `system/core/init/init.cpp`
1. Mount virtual filesystems (`tmpfs`, `proc`, `sysfs`, `selinuxfs`)
2. Start property service (key-value store)
3. Parse `init.rc` → start Zygote via socket definition

### Zygote — `frameworks/base/cmds/app_process/app_main.cpp`
1. `main()` → `AppRuntime.start("ZygoteInit", ...)`
2. `AndroidRuntime::start()` → create Java VM (ART), register JNI
3. `ZygoteInit.main()` → preload classes/resources, fork SystemServer, run select loop
4. **ใช้ Unix socket (ไม่ใช่ Binder)** — single-threaded กัน deadlock ตอน `fork()`
5. ทุก app process fork จาก Zygote → inherits preloaded classes

### System Server — `frameworks/base/services/java/com/android/server/SystemServer.java`
```
startBootstrapServices() → Watchdog, AMS, ATMS, PMS, PowerManager...
startCoreServices() → Battery, GPU, UsageStats, WebView...
startOtherServices() → WMS, Input, Camera, Alarm, Notification, Location, BT, Audio...
```
แล้วเรียก `AMS.systemReady()` → start Launcher

### Key Sources
| Source | File |
|--------|------|
| Init source | `system/core/init/init.cpp` |
| Init language | `system/core/init/README.md` |
| Zygote | `frameworks/base/core/java/com/android/internal/os/ZygoteInit.java` |
| System Server | `frameworks/base/services/java/com/android/server/SystemServer.java` |
| Watchdog | `frameworks/base/services/core/java/com/android/server/Watchdog.java` |

---

## 🎓 PhD-Level: Academic Research & Papers

### Key Conferences to Follow

| Conference | Focus | Frequency |
|-----------|-------|-----------|
| **USENIX Security** | Top-tier systems security — Android papers every year | Annual (Aug) |
| **ACM CCS** | Computer & communications security | Annual (Nov) |
| **NDSS** | Network & distributed system security | Annual (Feb) |
| **IEEE S&P (Oakland)** | Security & privacy | Annual (May) |
| **OSDI** | Operating systems design | Annual (Jul) |
| **MobiSys** | Mobile systems & applications | Annual (Jun) |
| **EuroSys** | European systems conference | Annual (Apr) |

### Must-Read Android Papers (2023-2025)

| Paper | Conference | Topic |
|-------|-----------|-------|
| **Ariadne** | USENIX 2025 | Data-driven customization inconsistencies in Android ROMs — พบ 30 access control bugs ใน 11 custom ROMs |
| **ChoiceJacking** | USENIX 2025 | bypasses JuiceJacking mitigations across 8 vendors |
| **Peep With A Mirror** | USENIX 2024 | breaks Android app sandbox via cache side-channel (ANDROSCOPE) |
| **Defects-in-Depth** | USENIX 2024 | analyzes kernel 1-day exploit defenses on Android devices |
| **NASS** | USENIX 2025 | fuzzing native Android system services — 12 bugs, 5 CVEs |
| **BaseMirror** | ACM CCS 2024 | reverse engineers 873 baseband commands from RIL binaries — 8 zero-days |
| **PathFuzzer** | IET 2025 | intent vulnerability fuzzing — 131 confirmed bugs |
| **Auditing Framework APIs** | USENIX 2023 | inferring security specs from app-side behavior |

### Classic Papers (ต้องอ่าน)

| Paper | Year | Why |
|-------|------|-----|
| **TaintDroid** | 2010 | Realtime privacy monitoring on Android |
| **DroidScope** | 2012 | Virtualization-based Android malware analysis |
| **Android Permissions Demystified** | 2012 | Permission system flaws |
| **Execute This!** | 2018 | Analyzing unsafe dynamic code loading |
| **FlowDroid** | 2014 | Static taint analysis for Android |
| **FUSE** | 2019 | Finding file-less permission bugs via fuzzing |

### Cellular/Baseband Security Papers
| Paper | Topic |
|-------|-------|
| [BaseMirror](https://github.com/OSUSecLab/BaseMirror) | reverse engineer RIL → baseband commands |
| [5GSEC Cellular Security Papers](https://github.com/5GSEC/Cellular-Security-Papers) | curated list of all cellular security research |
| ShannonBaseband | Samsung baseband reverse engineering |
| BaseSAFE | Emulation-based baseband fuzzing |
| FIRMWIRE | Transparent dynamic analysis for baseband firmware |

---

## ⚙️ ART Runtime Internals — Compiler & GC PhD-Level

> 📖 **หนังสือแนะนำ**: 《Android Runtime源码解析》(史宁宁, Tsinghua Press 2022) — อ่านเพื่อ deep dive

### Compilation Pipeline

```
DEX bytecode
  → dex2oat (on-device compiler)
    → Optimizing Backend (default since Android 6)
      → HGraph (SSA-based IR, control flow graph)
        → Optimization Passes
          → Native Code (.oat ELF file)
```

### HGraph IR (Intermediate Representation)

| Element | Description |
|---------|-------------|
| **HInstruction** | 1:1 with DEX bytecode + SSA indices, types, inputs, uses |
| **HBasicBlock** | Straight-line code sequence |
| **HGraph** | Full method CFG in SSA form |
| **Suspension Points** | GC entry points inserted by compiler |

### Optimization Pass Categories

**Platform-independent:**
- Constant folding, instruction simplification
- Dead code elimination (DCE)
- Loop invariant code motion (LICM)
- Bounds check elimination (BCE)
- Global value numbering (GVN)
- Instruction sinking

**Platform-dependent:**
- Register allocation (linear scan)
- Architecture-specific code gen (ARM64, x86_64)
- SIMD/NEON vectorization

### Method Execution States

```
Interpreted (DEX) → JIT-compiled → AOT-compiled
                          ↕ (profile-guided recompilation)
```

### Garbage Collection Types

| Collector | Use |
|-----------|-----|
| **Concurrent Copying (CC)** | Default — young generation |
| **Concurrent Mark-Sweep (CMS)** | Full heap |
| **Sticky CMS** | Partial — only dirty cards |
| **Semi-Space** | Young only |
| **Mark-Sweep-Compact** | Defragmentation |

### Key GC Concepts
- **Read Barriers** (Baker-style) — for concurrent copying
- **Card Table** — tracking dirty regions
- **Region-based heap** — non-moving (TLAB) + moving (bump-pointer) spaces
- **Homogeneous Space Compression** — defrag without full GC

### Allocator Types
| Allocator | Space |
|-----------|-------|
| **Bump Pointer** | Region space (fast allocation) |
| **Free-list (RosAlloc)** | Non-moving space (slots) |
| **TLAB** | Thread-Local Allocation Buffer |

### JIT Internals

1. **Profile-guided**: collects method hotness, type info, branch frequencies
2. **On-Stack Replacement (OSR)**: switch from interpreted to compiled mid-method
3. **Code cache**: subject to GC under memory pressure (~4MB for large apps)
4. **JIT daemon**: dumps profile → AOT daemon (`dex2oat`) recompiles
5. JIT = same compiler as AOT, but exploits runtime type info for better inlining

### Key Source Paths
| Component | Path |
|-----------|------|
| dex2oat | `art/dex2oat/` |
| Optimizing Compiler | `art/compiler/optimizing/` |
| HGraph | `art/compiler/optimizing/nodes.h` |
| GC | `art/runtime/gc/` |
| JIT | `art/runtime/jit/` |
| OAT format | `art/runtime/oat_file.h` |

---

## 🐛 Vulnerability Research & Fuzzing — PhD Level

### Fuzzing Frameworks

| Tool | Target | Result |
|------|--------|--------|
| **NASS** | Native Android system services (Binder RPC) | 12 bugs, 5 CVEs (USENIX 2025) |
| **BTFuzzer** | Bluetooth protocols | CVE-2020-27024 + new info leak |
| **PathFuzzer** | Intent vulnerabilities | 131 confirmed bugs in 500 apps |
| **syzkaller** | Linux kernel syscalls | 1000+ kernel bugs |
| **AFL++** | Userspace binaries | General purpose |
| **libFuzzer** | Library/large-codebase | Coverage-guided |
| **JANUS** | Android APK signing | Found master key vuln |

### CVE Research Methodology

```
1. ATTACK SURFACE MAPPING
   ├── Exported components (AndroidManifest)
   ├── Binder interfaces (AIDL/HIDL)
   ├── UNIX sockets (/dev/socket/*)
   ├── Syscalls (seccomp filters)
   ├── Kernel drivers (ioctls)
   └── Baseband interfaces (RIL)

2. STATIC ANALYSIS
   ├── Control flow + call graph
   ├── Taint analysis (sources → sinks)
   ├── Permission flow analysis
   └── Pattern matching (dangerous APIs)

3. DYNAMIC FUZZING
   ├── Coverage-guided (libFuzzer/AFL++)
   ├── Interface-aware (valid structs first)
   ├── Stateful (model protocol state machine)
   └── Differential (compare implementations)

4. EXPLOIT DEVELOPMENT
   ├── Primitive: arbitrary read/write
   ├── KASLR bypass: info leak
   ├── Control flow: ROP/JOP chains
   └── Post-exploit: disable SELinux, extract keys
```

### Android Mitigation Analysis

| Mitigation | Since | Bypass Difficulty |
|-----------|-------|-------------------|
| **ASLR** (PIE) | Android 5.0 | Requires info leak |
| **DEP** (NX) | Always | ROP/JOP needed |
| **Stack Canaries** | Android 6.0 | Info leak + overwrite |
| **CFI** | Android 9.0 (kernel 4.9+) | Counterfeit code paths |
| **Shadow Call Stack** | Android 10 | Hard to bypass |
| **PAC/BTI** (ARMv8.3+) | Android 11 | Pointer auth bypass required |
| **MTE** (ARMv8.5+) | Android 13+ | Very hard — hardware tagged memory |
| **KCFI** | Android 14 | Kernel control-flow integrity |
| **SCS** | Android 12+ | Shadow call stack |

---

## 📡 Baseband/Modem/RIL — PhD-Level

> 🎓 This is the **most obscure** Android subsystem — เรียนนี่ = เหนือกว่า 99% ของ ROM devs

### Architecture

```
Android Framework (TelephonyManager)
  ↕ Binder
RIL Daemon (rild)
  ↕ Socket (/dev/socket/rild)
Vendor RIL (.so library)
  ↕ IPC (SIPC/IPC/HSIC/SHARE_MEM)
Baseband Processor (CP) runs RTOS (Nucleus/RTXC/ThreadX)
  ↕ AT Commands / SIPC Protocol
Modem Hardware (RF Transceiver)
```

### Samsung RIL Internals (Shannon Baseband)

| Layer | Protocol |
|-------|----------|
| Android ↔ Vendor RIL | `invokeOemRilRequestRaw` |
| RIL ↔ Baseband | SIPC (Samsung Inter-Processor Communication) |
| Baseband firmware | Proprietary RTOS (Nucleus) |
| Command format | Ipc41 / Ipc41X protocol |

### BaseMirror Key Findings (ACM CCS 2024)

- **873 undocumented baseband commands** extracted from 28 vendor RILs
- **8 zero-day vulnerabilities** on Samsung Galaxy A53
- Command group identified by **5th byte** in Ipc41X protocol
- Adversary classes: rooted → unprotected APIs → unprotected sockets

### Baseband Attack Surface

```
AP → CP (Android attacks baseband):
  ├── RILD socket (accessible to radio group)
  ├── OEM RIL hooks (invokeOemRilRequestRaw)
  ├── Secret codes (*#*#CODE#*#*)
  └── AT command injection

CP → AP (compromised baseband attacks Android):
  ├── RIL responses (malformed)
  ├── DMA access to AP memory
  └── USB/PCIe backdoors
```

### Key Resources
| Resource | Link |
|----------|------|
| BaseMirror (tool) | https://github.com/OSUSecLab/BaseMirror |
| Cellular Security Papers | https://github.com/5GSEC/Cellular-Security-Papers |
| ShannonBaseband | https://github.com/grant-h/ShannonBaseband |

---

## 🔒 TEE Programming — Write Your Own Trusted Application

> 🎓 PhD-level skill — เขียนโปรแกรมใน Secure World

### OP-TEE Architecture

```
Normal World (REE)              │  Secure World (TEE)
  ┌─────────────────┐           │  ┌──────────────────┐
  │ Client App (CA) │────SMC───▶│  │ Trusted App (TA) │
  │ libteec.so      │           │  │ (S-EL0 user mode) │
  └─────────────────┘           │  └──────────────────┘
                                │  ┌──────────────────┐
                                │  │ OP-TEE OS        │
                                │  │ (S-EL1 kernel)   │
                                │  └──────────────────┘
```

### Client App (CA) — Normal World

```c
// host/main.c
#include <tee_client_api.h>

TEEC_Context ctx;
TEEC_Session sess;
TEEC_UUID uuid = TA_MY_APP_UUID;  // Must match TA

TEEC_InitializeContext(NULL, &ctx);
TEEC_OpenSession(&ctx, &sess, &uuid, TEEC_LOGIN_PUBLIC, NULL, NULL, NULL);

TEEC_Operation op;
memset(&op, 0, sizeof(op));
op.paramTypes = TEEC_PARAM_TYPES(TEEC_VALUE_INPUT, TEEC_NONE, TEEC_NONE, TEEC_NONE);
op.params[0].value.a = 42;

TEEC_InvokeCommand(&sess, CMD_DO_SOMETHING, &op, NULL);
TEEC_CloseSession(&sess);
TEEC_FinalizeContext(&ctx);
```

### Trusted Application (TA) — Secure World

```c
// ta/my_app_ta.c
#include <tee_internal_api.h>

TEE_Result TA_CreateEntryPoint(void) { return TEE_SUCCESS; }
void TA_DestroyEntryPoint(void) {}

TEE_Result TA_OpenSessionEntryPoint(uint32_t param_types,
    TEE_Param params[4], void **sess_ctx)
{ return TEE_SUCCESS; }

TEE_Result TA_InvokeCommandEntryPoint(void *sess_ctx, uint32_t cmd_id,
    uint32_t param_types, TEE_Param params[4])
{
    switch (cmd_id) {
        case CMD_DO_SOMETHING:
            IMSG("Received value: %d", params[0].value.a);
            // Perform secure operation here
            return TEE_SUCCESS;
    }
    return TEE_ERROR_NOT_SUPPORTED;
}

void TA_CloseSessionEntryPoint(void *sess_ctx) {}
```

### TA Project Structure

```
my_ta/
├── host/
│   ├── main.c              # CA (Normal World)
│   └── Makefile
└── ta/
    ├── include/
    │   └── ta_my_app.h      # UUID + command IDs
    ├── my_app_ta.c           # TA entry points
    ├── user_ta_header_defines.h  # UUID, stack size, flags
    ├── Makefile
    └── sub.mk
```

### Building & Deploying

```bash
# Build TA
make CROSS_COMPILE=aarch64-linux-gnu- \
     TA_DEV_KIT_DIR=/path/to/optee-os/export-ta_arm64

# Build CA
make CROSS_COMPILE=aarch64-linux-gnu- \
     TEEC_EXPORT=/path/to/optee-client/export

# Deploy
scp <uuid>.ta root@device:/lib/optee_armtz/
scp my_ca root@device:/usr/bin/
```

### Security Rules

| Rule | Detail |
|------|--------|
| **Signing** | Production TA MUST use private key (NOT OP-TEE dev key) |
| **Subkeys** | Different actors sign different TAs without sharing root key |
| **Memory Isolation** | TA can't access other TA's memory (TZASC enforced) |
| **No Debug in Prod** | TA debug flag OFF in production (`TA_FLAG_EXEC_DDR`) |

### Rust TEE Development (Teaclave TrustZone SDK)

```bash
git clone https://github.com/apache/incubator-teaclave-trustzone-sdk
cd incubator-teaclave-trustzone-sdk
./setup.sh && source environment
make optee && make examples
```

### Key Concepts Glossary

| Term | Meaning |
|------|---------|
| **SMC** | Secure Monitor Call — switch between worlds |
| **TZASC** | TrustZone Address Space Controller — memory partitioning |
| **TZPC** | TrustZone Protection Controller — peripheral partitioning |
| **RPMB** | Replay Protected Memory Block — secure storage on eMMC |
| **PUF** | Physically Unclonable Function — device-unique key |
| **HUK** | Hardware Unique Key — root key in eFuses |
| **SSK** | Secure Storage Key — derived from HUK |
| **FEK** | File Encryption Key — per-TA encryption key |

---

## 📖 PhD-Level Books

| Book | Author | Year | Why |
|------|--------|------|-----|
| **《Android Runtime源码解析》** | 史宁宁 | 2022 | ART internals — based on Android 10.0.0_r39, covers compiler, GC, startup |
| **《深入理解Android》(卷I-V)** | 邓凡平 | 2016-2019 | Deep Android internals — class loader, JNI, ART, process |
| **Android Security Internals** | Nikolay Elenkov | 2014 | Foundation of Android security (dated but fundamentals) |
| **Embedded Android** | Karim Yaghmour | 2013 | Linux↔Android bridge, still gold-standard |
| **Inside the Android OS** | Meike & Schiefer | 2021 | Most current — Treble, ART, HAL, boot |
| **The Mobile Hacker's Handbook** | Wiley | 2024 | Latest mobile exploitation techniques |
| **Linux Kernel Development** | Robert Love | 2010 | Understanding kernel (3rd ed) |
| **Understanding the Linux Kernel** | Bovet & Cesati | 2005 | Deep kernel internals (O'Reilly) |

---

## 🔬 Linux Scheduler — EAS/CFS Deep Dive

> 🎓 เข้าใจ scheduler = รู้ว่า kernel ตัดสินใจ run อะไรเมื่อไหร่บน core ไหน

### Scheduler Evolution

```
O(n) → O(1) → CFS (2.6.23) → EAS (4.x, Android default)
                ↓                      ↓
              BFS (desktop)    Energy-aware scheduling
                   ↓
              MuQSS (scalable BFS)
```

### CFS (Completely Fair Scheduler)

| Concept | Explanation |
|---------|-------------|
| **Virtual Runtime (vruntime)** | Per-task accumulator — lower = runs first |
| **Red-Black Tree** | Self-balancing BST ordered by vruntime |
| **sched_latency** | Target latency (6ms default) |
| **sched_min_granularity** | Min time slice (0.75ms) |
| **Nice priority** | -20 (highest) to +19 (lowest) → weight |
| **PELT** | Per-Entity Load Tracking — utilization tracking |

### EAS (Energy Aware Scheduling)

```
find_energy_efficient_cpu():
  1. Compute CPU capacity (arch_scale_cpu_capacity)
  2. Estimate utilization (PELT = running + waiting)
  3. For each candidate CPU: predict total system energy
  4. Choose CPU that minimizes Δenergy with acceptable performance
  5. If over-utilized (>80%): fall back to CFS load balance
```

| Component | Detail |
|-----------|--------|
| **Energy Model (EM)** | Per-frequency OPP power table in DT |
| **schedutil governor** | Required — uses util signal for DVFS |
| **Over-utilization flag** | >80% cap → disable EAS → enable LB |
| **Asymmetric topology** | big.LITTLE required for EAS |
| **SD_SHARE_CAP_STATES** | sched domain flag for EAS |

### EAS Tuning Parameters (Android)

```properties
# Kernel cmdline or sysfs
/sys/devices/system/cpu/cpu<N>/cpu_capacity
/sys/devices/system/cpu/sched_migration_cost_ns=500000
/sys/devices/system/cpu/sched_latency_ns=6000000

# Vendor hooks (Android out-of-tree)
sys.use_tunings=true
```

### BFS / MuQSS (Alternative Scheduler for Desktop)

| Feature | BFS/MuQSS |
|---------|-----------|
| **Algorithm** | Earliest Eligible Virtual Deadline First (EEVDF) |
| **Queue** | Single skiplist (MuQSS) vs per-CPU (CFS) |
| **Strength** | Desktop responsiveness |
| **Weakness** | Scalability (≤16 CPUs) |
| **Status** | Out-of-tree patchset |

### Research: ML for Scheduler Tuning

- **LearningEAS** — RL (policy gradient) tunes `TARGET_LOAD`, `sched_migration_cost` → 5.7% power reduction, 25.5% perf improvement on LG G8
- **STUN** — Q-learning optimization of kernel scheduler params
- OSPM 2025: Current EM too simple for modern complex SoCs; vendor hooks proposed

---

**Why:** Comprehensive reference for Android ROM team — PhD-level knowledge across security, runtime, compiler, scheduler, baseband, TEE, and vulnerability research
**How to apply:** Assign advanced topics to team members based on specialization; one deep topic per team member, present to the rest

> **เรียนโดย:** AURA ✨, FORGE 🏗️ — สำคัญมากสำหรับ UI modding

### Complete Pipeline: App → Screen

```
App (Canvas/View.draw)
  → HWUI (DisplayList → RenderThread)
    → GPU (OpenGL ES / Vulkan via Skia)
      → Surface (GraphicBuffer in BufferQueue)
        → SurfaceFlinger (compositor)
          → HWC (Hardware Composer overlay or GPU composition)
            → Display HAL → DRM/KMS → Screen Panel
```

### Key Components

| Component | Role | Details |
|-----------|------|---------|
| **Skia** | 2D Graphics Engine | Google's open-source engine — all Canvas API → Skia draw calls |
| **HWUI** | Hardware-Accelerated UI | แปลง `View.draw()` → DisplayList → RenderThread GPU execution |
| **Vulkan** | Modern GPU API | Low-overhead, SPIR-V, ใช้แทน OpenGL ES |
| **SurfaceFlinger** | Compositor | รับ buffers จากทุกแอพ → composite → screen |
| **HWC** | Hardware Composer | ใช้ Display Controller Overlay planes — faster + lower power |
| **BufferQueue** | Data Channel | Producer(แอพ) ↔ Consumer(SurfaceFlinger) — triple buffering |
| **Gralloc** | Memory Allocator | จอง GraphicBuffer ผ่าน ION — zero-copy ระหว่าง process |
| **Choreographer** | VSYNC Scheduler | จังหวะ 16.7ms @60Hz — ป้องกัน jank |

### Composition Strategies

| Mode | When | Power | Performance |
|------|------|-------|-------------|
| **Hardware Overlay** | N windows ≤ N overlay planes | ✅ Lowest | ✅ Best |
| **GPU Composition (GLES)** | Complex blending, many layers | ❌ Higher | ❌ Overhead |
| **Mixed Mode** | Some layers overlay, rest GPU | ⚡ Balanced | ⚡ Balanced |

### Modern Features (2024+)
- **VRR (Variable Refresh Rate)**: 1Hz–120Hz via LTPO + HWC2.5+
- **Foldable Optimization**: display mode switching (Android 12+)
- **Vulkan Dominance**: replacing OpenGL ES for lower CPU overhead

### Debugging Tools
```bash
dumpsys SurfaceFlinger                          # composition state, layers
adb shell dumpsys gfxinfo <package>             # frame stats, jank
Perfetto (System Tracing)                       # full pipeline trace
RenderDoc                                        # GPU frame capture
```

### Source Code Paths
| Component | Path |
|-----------|------|
| SurfaceFlinger | `frameworks/native/services/surfaceflinger/` |
| HWUI | `frameworks/base/libs/hwui/` |
| Skia | `external/skia/` |
| BufferQueue | `frameworks/native/libs/gui/BufferQueue*.cpp` |
| Gralloc HAL | `hardware/libhardware/include/hardware/gralloc.h` |

---

## 🔐 Android Security Architecture — Deep Dive

> **เรียนโดย:** CYPHER 🔐, FORGE 🏗️ — foundation ของ ROM security

### Three Pillars

```
TrustZone/TEE ──────► Keystore/Keymaster ──────► Verified Boot (AVB)
 (Hardware root)       (Key protection)             (Boot chain integrity)
```

### ARM TrustZone & TEE

```
Normal World (REE)              │  Secure World (TEE)
  Android OS + Apps             │  Trusted Apps + Keys
  ↓ SMC (Secure Monitor Call)   │  ↓
  Kernel TrustZone Driver       │  OP-TEE / QTEE / Trusty OS
  CA (Client App)               │  TA (Trusted App)
                      ↕ TEEC_InvokeCommand ↕
```

| TEE OS | ใช้โดย |
|--------|--------|
| **OP-TEE** | Open-source, Linaro |
| **QTEE** | Qualcomm Snapdragon |
| **Trusty** | Google (Pixel) |
| **Titan M** | Google dedicated security chip (StrongBox) |

### Verified Boot (AVB) — Chain of Trust

```
Hardware Root of Trust (eFuses)
  → Bootloader (verified by OEM public key)
    → boot.img (RSA-2048 signature)
      → system/vendor (dm-verity hash tree)
```

| Boot State | Color | Meaning |
|-----------|-------|---------|
| All verified | 🟢 GREEN | Full trust |
| Non-OEM key | 🟡 YELLOW | Warning shown |
| Unlocked | 🟠 ORANGE | No verification |
| Failed | 🔴 RED | Halt — security violation |

### Android Keystore / Keymaster

| Security Level | Location | Protection |
|---------------|----------|------------|
| **Software** | Android OS (OpenSSL) | App sandbox only |
| **TEE-backed** | TrustZone (OP-TEE/QTEE/Trusty) | Key never leaves secure world |
| **StrongBox** | Dedicated chip (Titan M) | Tamper-resistant, highest security |

### Key Attestation
- App requests certificate chain → signed by Google hardware attestation root
- Certificate contains: verified boot state, bootloader lock status, OS version
- Remote server verifies: device is genuine, not rooted, bootloader locked

### Source Code
| Component | Path |
|-----------|------|
| Keymaster HAL | `hardware/interfaces/keymaster/` |
| Keystore Service | `system/security/keystore/` |
| Verified Boot | `system/extras/verity/` |
| dm-verity | kernel: `drivers/md/dm-verity*` |

---

## 🔗 Binder IPC — Kernel Driver Deep Dive

> **เรียนโดย:** FORGE 🏗️, CYPHER 🔐 — backbone ของ Android IPC

### Architecture Overview

```
Client Process              │    Server Process
  libbinder.so              │      libbinder.so
    ioctl(BINDER_WRITE_READ)│        ioctl(BINDER_WRITE_READ)
         ↕                  │             ↕
┌─────────┴─────────────────┴──────────────┐
│  KERNEL: drivers/android/binder.c        │
│  /dev/binder, /dev/hwbinder, /dev/vndbinder│
└───────────────────────────────────────────┘
```

### Binder Device Nodes
| Device | Use |
|--------|-----|
| `/dev/binder` | Framework ↔ App (AIDL) |
| `/dev/hwbinder` | Framework ↔ Vendor (HIDL) |
| `/dev/vndbinder` | Vendor ↔ Vendor (AIDL) |

### Why Binder (Not Socket/Pipe)?

| Feature | Binder | Socket/Pipe |
|---------|--------|-------------|
| **Data Copy** | **1 copy** (mmap) | 2 copies |
| **Security** | UID/PID per transaction | None built-in |
| **Object Reference** | Reference counting + death notification | Manual |
| **Thread Management** | Auto thread pool | Manual |

### The "One Copy" Magic (mmap)

```
Traditional IPC:  AppA → kernel buffer → AppB  (2 copies)

Binder IPC:
  1. Server mmaps /dev/binder → kernel buffer mapped into server's address space
  2. Client writes → kernel copies data into server's mapped buffer (1 copy only)
  3. Server reads directly from mapped buffer (no second copy)
```

### Locking Hierarchy (3-level spinlock)

```
proc->outer_lock  →  node->lock  →  proc->inner_lock
  (binder_ref)       (binder_node)  (threads, todo lists, nodes)
```

### Key Data Structures
| Struct | Purpose |
|--------|---------|
| `binder_proc` | Per-process bookkeeping (threads, nodes, refs, todo) |
| `binder_node` | Binder service object (can receive transactions) |
| `binder_ref` | Reference from one process to another's node |
| `binder_thread` | Per-thread state (transaction_stack, looper state) |
| `binder_work` | Work item (TRANSACTION, DEAD_BINDER, etc.) |

### Priority Inheritance
- Real-time thread making binder call → target thread inherits RT priority
- Node level: `min_priority` field ensures minimum priority for callers
- Critical for audio/video — prevents jank from priority inversion

### Limits
- **1MB transaction** (`TransactionTooLargeException` if exceeded)
- **15 threads** per process (default thread pool cap)
- Synchronous calls block calling thread

### Source
| File | Content |
|------|---------|
| `drivers/android/binder.c` | Kernel driver (~6000+ lines) |
| `frameworks/native/libs/binder/` | Userspace library (libbinder) |

---

## 🔊 Android Audio System — Deep Dive

> **เรียนโดย:** VECTOR 🎯, FORGE 🏗️ — HAL interaction, DSP pipeline

### Complete Audio Pipeline

```
App [PCM] → AudioTrack → Shared Memory (Ashmem)
  → AudioFlinger (MixerThread: resample + mix + format convert)
    → Audio HAL (out_write)
      → Kernel ALSA (DMA Buffer)
        → I2S/SLIMbus → Codec/DAC → Speaker/Headphone
```

### Core Components

| Component | Role | Location |
|-----------|------|----------|
| **AudioFlinger** | Audio factory — mix, resample, format convert | `frameworks/av/services/audioflinger/` |
| **AudioPolicyService** | Traffic cop — routing, volume, focus arbitration | `frameworks/av/services/audiopolicy/` |
| **AudioTrack** | App-side data pipe | `frameworks/base/media/java/android/media/AudioTrack.java` |
| **Audio HAL** | Hardware abstraction | `hardware/interfaces/audio/` (AIDL) |
| **TinyALSA** | Userspace ALSA library | `external/tinyalsa/` |
| **ALSA Driver** | Kernel DMA buffer + I2S | `sound/soc/` |

### AudioFlinger Thread Types

| Thread | Use Case |
|--------|----------|
| **MixerThread** | Default — music, video, most apps |
| **DirectOutputThread** | Low-latency — bypass mixer |
| **OffloadThread** | Hardware decode — MP3/AAC decoded by DSP |
| **DuplicatingThread** | Dual output — speaker + BT simultaneously |
| **MmapThread** | AAudio — mmap to DMA buffer, lowest latency |
| **RecordThread** | Audio recording |

### Mixer Core Formula

```
Output = Σ(Input_i × Volume_i)   // saturated to 16/24-bit
```

With resampling (SRC) when app rate ≠ hardware rate (e.g., 44.1kHz → 48kHz)

### Audio HAL Evolution

| Generation | IPC | Isolation |
|-----------|-----|-----------|
| **Legacy** | Direct .so load | None (same process) |
| **HIDL (Treble)** | HwBinder | system ↔ vendor |
| **AIDL (Latest)** | Standard Binder | Better performance, less copies |

### Low-Latency Path: AAudio / MMAP

```
Normal Path:  App → Shared Mem → AudioFlinger → HAL → Kernel (20ms+)
Fast Path:    App → mmap(DMA Buffer) → Kernel via poll/AAudio (5ms or less)
```

Fast Mixer: `SCHED_FIFO` real-time thread, CPU affinity → no preemption

### ALSA / ASoC Architecture

| Layer | Component |
|-------|-----------|
| **Platform** | SoC audio (CPU DAI + PCM DMA) — e.g., qdsp6v2 |
| **Codec** | Audio chip driver — e.g., WCD9335 (DAC/ADC/Mixer) |
| **Machine** | Links Platform + Codec via `dai_link` |

### Qualcomm DSP Path
```
App → AudioFlinger → HAL → Hexagon aDSP (decode/encode/effects) → Codec
```

### Debugging
```bash
dumpsys media.audio_flinger     # active streams, underrun count
tinymix                          # ALSA mixer controls
tinyplay /data/test.pcm         # test audio directly to HAL
```

---

## 🧠 Memory Management — Deep Dive

> **เรียนโดย:** CYPHER 🔐 — kernel optimization

### Evolution of LMK (Low Memory Killer)

```
Kernel LMK (pre-4.12)  →  Userspace lmkd (Android 9+)
                            ├── vmpressure (legacy)
                            └── PSI (Pressure Stall Information) — Android 10+
```

### lmkd Configuration Properties

```properties
# PSI thresholds
ro.lmk.use_psi=true
ro.lmk.psi_partial_stall_ms=70          # low memory trigger (200 for low-RAM)
ro.lmk.psi_complete_stall_ms=700        # critical memory trigger

# Thrashing control
ro.lmk.thrashing_limit=30               # thrashing threshold
ro.lmk.thrashing_limit_decay=10         # decay per window

# Kill strategy
ro.lmk.kill_heaviest_task=true          # kill heaviest, not oldest
ro.lmk.kill_timeout_ms=100              # wait before kill
ro.lmk.low=1001                         # adj threshold
ro.lmk.medium=800
ro.lmk.critical=0

# Legacy (fallback)
ro.lmk.use_minfree_levels=false         # use PSI, not free memory

# Swap
ro.lmk.swap_free_low_percentage=10      # trigger swap cleanup
ro.lmk.swap_util_max=50                 # max swap utilization
```

### ZRAM Optimization

```bash
# fstab entry
/dev/block/zram0 none swap defaults zramsize=50%,zram_compression=zstd

# Check
cat /proc/swaps
zramctl
```

| Algorithm | Speed | Ratio |
|-----------|-------|-------|
| **lz4** | Fastest | Moderate |
| **zstd** | Fast | Good |
| **lzo** | Fast | Lower |
| **deflate** | Slow | Best |

### Memory cgroups
- Required for lmkd: `CONFIG_MEMCG=y`, `CONFIG_MEMCG_SWAP=y`
- Each app process → cgroup (based on `oom_score_adj`)
- Enables per-process memory limits + accounting

### Key Kernel Configs
```
CONFIG_PSI=y                    # Pressure Stall Information
CONFIG_MEMCG=y                  # Memory cgroups
CONFIG_MEMCG_SWAP=y             # Swap accounting
CONFIG_ZRAM=y                   # Compressed RAM block device
CONFIG_ZRAM_DEF_COMP_ZSTD=y     # zstd as default
```

---

## 📸 Android Camera Pipeline — HAL3 Deep Dive

> **เรียนโดย:** VECTOR 🎯 — camera HAL, ISP bringup

### Architecture Stack

```
Camera2 API (App)
  → CameraService (system service, permissions)
    → Camera HAL3 (AIDL/HIDL: ICameraProvider → ICameraDevice → ICameraDeviceSession)
      → Camera Driver (V4L2 + ISP + Sensor)
```

### HAL3 Pipeline Model

```
1 request → 1 frame result
  Request = [sensor config + lens config + 3A mode + output surfaces]
  Result  = [metadata + N image buffers (1 per output surface)]
```

### ISP (Image Signal Processor) Pipeline

| Stage | Function | Modes |
|-------|----------|-------|
| **Demosaic** | Bayer → RGB | Cannot disable |
| **Color Correction** | 3×3 matrix | MANUAL_SENSOR control |
| **Tone Curve** | Gamma + contrast | FAST / HIGH_QUALITY |
| **Noise Reduction** | Spatial + temporal | OFF / FAST / HIGH_QUALITY |
| **Sharpening** | Edge enhancement | OFF / FAST / HIGH_QUALITY |
| **Scaler** | Multiple resolutions | Hardware scaler units |

### Camera2 Hardware Levels

| Level | Features |
|-------|----------|
| **LEGACY** | Backward compat — no manual controls |
| **LIMITED** | Basic manual parameters |
| **FULL** | Manual control + 3A feedback + multi-stream |
| **LEVEL_3** | Logical cameras + depth + RAW burst |

### Key HAL Files
| File | Role |
|------|------|
| `ICameraProvider.hal` | Camera enumeration |
| `ICameraDevice.hal` | Open/close device |
| `ICameraDeviceSession.hal` | Configure streams, submit requests |
| `types.hal` | All data structures |

### Vendor Customization Points
- ISP tuning parameters (per-sensor calibration)
- 3A algorithms (AE, AWB, AF)
- Custom post-processing effects
- Multi-camera logical device behavior

### Debugging
```bash
dumpsys media.camera              # camera service state
adb shell dumpsys media.camera    # active sessions, HAL info
```

---

## 📡 Other Critical Subsystems

### Power Management
| Component | Role |
|-----------|------|
| **Wakelocks** | Prevent suspend (kernel + userspace) |
| **Doze** | Aggressive idle → suspend |
| **Suspend-to-Idle (S2I)** | Modern replacement for deep sleep |
| **CPU Idle** | C-states — C0(active) → C3(deep) |
| **Thermal Engine** | Throttle CPU/GPU/Battery when hot |

### Networking Stack
| Layer | Implementation |
|-------|---------------|
| **WiFi HAL** | AIDL: `android.hardware.wifi` |
| **wpa_supplicant** | WiFi authentication |
| **Bluetooth Stack** | Fluoride (AOSP) + vendor BT HAL |
| **Radio (RIL)** | Telephony — vendor RIL daemon |
| **Netd** | Network daemon — firewall, DNS, tethering |

### Storage
| Layer | Implementation |
|-------|---------------|
| **vold** | Volume daemon — mount, format, encryption |
| **FBE (File-Based Encryption)** | Per-file encryption key (Android 7+) |
| **FDE (Full-Disk Encryption)** | Legacy — entire partition encrypted |
| **sdcardfs** | Emulated storage (replaced by FUSE in newer kernels) |
| **f2fs** | Flash-friendly filesystem — better for UFS |

---

## 🎮 Android Internals — Additional Learning Resources

### AOSP Source Navigation Tips

```bash
# Find which process owns a service
adb shell dumpsys | grep "DUMP OF SERVICE"

# Find Binder interface
cd frameworks/base && grep -r "interface.*extends IInterface"

# Find native service
cd frameworks/native/services && ls

# Find HAL definition
cd hardware/interfaces && find . -name "*.hal" -o -name "*.aidl"
```

### Key AOSP Repos to Study

| Repo | What You Learn |
|------|---------------|
| `frameworks/base` | Core framework — AMS, WMS, PMS, SystemUI, resources |
| `frameworks/native` | SurfaceFlinger, BufferQueue, Binder, Sensors |
| `frameworks/av` | AudioFlinger, CameraService, MediaPlayer, Stagefright |
| `system/core` | Init, ADB, Logcat, Toolbox, liblog |
| `system/security` | Keystore, Keymaster |
| `hardware/interfaces` | All HAL definitions (AIDL/HIDL) |
| `packages/apps` | AOSP apps — Launcher3, Settings, Camera2, etc. |
| `external/` | Third-party — Skia, SQLite, libpng, freetype, etc. |
| `bionic/` | Android's libc (not glibc!) + dynamic linker |
| `art/` | ART runtime — dex2oat, GC, JIT |

### Advanced Debugging Tools

| Tool | Use |
|------|-----|
| `atrace` | Kernel + userspace trace (sched, gfx, audio, binder) |
| `systrace` | Visualize atrace output |
| `Perfetto` | Modern trace (replaces systrace) |
| `simpleperf` | CPU profiler (like Linux perf) |
| `heapprofd` | Heap profiler |
| `debuggerd` | Crash dump (tombstones) |
| `lsof` / `ls -l /proc/<pid>/fd` | Open file descriptors |
| `showmap` | Process memory map |
| `procrank` | Process memory ranking |

---

**Why:** Comprehensive reference for Android ROM team learning — covers repos, tools, books, videos, communities, and internals at every subsystem level
**How to apply:** Assign sections to each team member based on role; have them study and present findings to the team

### Forums
| Community | Link |
|-----------|------|
| XDA Developers | https://xdaforums.com |
| aosp-devs.org | https://aosp-devs.org — newsletter, events |
| /r/AndroidROM | Reddit community |
| Stack Overflow (android-rom tag) | https://stackoverflow.com |

### Telegram Groups
- XDA ROM Building Help groups (search per device)
- Android ROM Development global groups

### Events
- **FOSDEM AOSP Devroom** (annual, Brussels) — talks on YouTube [@aosp-devs](https://www.youtube.com/@aosp-devs)
- **Linux Plumbers Conference** — Android + kernel tracks

### ROMs ตัวอย่างให้ติดตาม
| ROM | จุดเด่น |
|-----|---------|
| [LineageOS](https://github.com/LineageOS) | ต้นแบบ — ใหญ่สุด, devices มากสุด |
| [GrapheneOS](https://github.com/GrapheneOS) | security-hardened |
| [crDroid](https://github.com/crdroidandroid) | customization-rich |
| [Evolution X](https://github.com/Evolution-X) | feature-rich |
| [Pixel Experience](https://github.com/PixelExperience) | Pixel-exclusive features |
| [AfterlifeOS](https://github.com/AfterlifeOS) | kernel-level optimizations |

---

## 🛠️ Workflow & Development Environment

### เครื่องสำหรับ Build AOSP
| Spec | Minimum | Recommended |
|------|---------|-------------|
| CPU | 8 cores (64-bit) | 16+ cores |
| RAM | 16 GB | 32-64 GB |
| Disk | 400 GB SSD | 1 TB NVMe |
| OS | Ubuntu 18.04+ | Ubuntu 22.04 LTS |
| Swap | 16 GB | 32 GB |

### Essential Tools
```bash
# Build dependencies
sudo apt install git gnupg flex bison gperf build-essential \
  zip curl zlib1g-dev gcc-multilib g++-multilib libc6-dev-i386 \
  lib32ncurses5-dev x11proto-core-dev libx11-dev lib32z-dev \
  libgl1-mesa-dev libxml2-utils xsltproc unzip python3

# repo tool
mkdir ~/bin
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
chmod a+x ~/bin/repo
```

### AOSP Source Download
```bash
# Initialize
repo init -u https://android.googlesource.com/platform/manifest -b android-15.0.0_r1

# Sync (ใช้เวลา 2-8 ชม ขึ้นกับ internet)
repo sync -j8 -c --no-tags
```

### Build
```bash
source build/envsetup.sh
lunch aosp_arm64-userdebug
m -j$(nproc)
```

### CI/CD for ROM
| Tool | Description |
|------|-------------|
| GitHub Actions | free for public repos — build ROM อัตโนมัติ |
| [ContainerizedAndroidBuilder](https://github.com/iusmac/ContainerizedAndroidBuilder) | Docker build |
| [ham (Hetzner Android Make)](https://github.com/antony-jr/ham) | cloud build <€1/build |

---

**Why:** Comprehensive reference for Android ROM team learning — covers repos, tools, books, videos, communities, and internals
**How to apply:** Assign sections to each team member based on role; have them study and present findings to the team
