---
name: top-os-engineer-curriculum
description: Systematic curriculum — ระดับ TOP OS Engineer สำหรับทีม NOVA ทั้ง 7 คน
metadata: 
  node_type: memory
  type: reference
  created: 2026-07-23
  originSessionId: 97241c28-1ee0-48f0-84d7-9d2531437a7d
  modified: 2026-07-23T05:26:26.970Z
---

# 🏔️ TOP OS Engineer — Systematic Curriculum

เส้นทางจาก ROM Developer → OS Engineer ระดับโลก — จัดเป็นระบบ 10 Levels

---

## 📊 Skill Map Overview

```
LEVEL 1  ██ Foundation: C, Assembly, Computer Architecture
LEVEL 2  ██ Build Your Own OS: xv6 labs, OSDev from scratch
LEVEL 3  ██ Linux Kernel Internals: scheduler, memory, sync, RCU
LEVEL 4  ██ AOSP/Android Deep Internals: every subsystem
LEVEL 5  ██ Firmware & Boot: coreboot, UEFI, Trusted Firmware
LEVEL 6  ██ Next-Gen OS: Fuchsia/Zircon, seL4, microkernel design
LEVEL 7  ██ Formal Methods: Isabelle/HOL, TLA+, verified systems
LEVEL 8  ██ Security Research: CVE, exploit, fuzzing, Baseband
LEVEL 9  ██ TEE & TrustZone: OP-TEE, Trusty, Trusted Apps
LEVEL 10 ██ Real Engineering: upstream, profiling, code review
```

---

## LEVEL 1: Foundation — ภาษา + Architecture

### C Programming — Expert Level

```
ต้องเขียนได้โดยไม่ต้องคิด:
  ├── Pointer arithmetic (single, double, triple indirection)
  ├── Function pointers + callbacks
  ├── Bit manipulation + bitfields
  ├── Volatile + const correctness
  ├── Memory alignment + padding
  ├── Inline assembly (GCC extended asm)
  ├── Linker scripts (.ld files)
  └── Freestanding C (no libc — bare metal)
```

### Assembly — Read + Write (ARM64 focus)

```
ARM64 (AArch64):
  ├── Registers: x0-x30, sp, pc, pstate
  ├── Calling convention (AAPCS64)
  ├── Exception levels: EL0(userspace) → EL1(kernel) → EL2(hypervisor) → EL3(secure monitor)
  ├── System registers: SCTLR_EL1, TCR_EL1, TTBR0/1_EL1, VBAR_EL1
  ├── Instructions: ldr/str, stp/ldp, adr/adrp, bl/blr/ret, msr/mrs, svc/hvc/smc
  └── Barriers: dmb, dsb, isb
```

### Computer Architecture

| Topic | Must Understand |
|-------|----------------|
| **CPU Pipeline** | Fetch → Decode → Execute → Memory → Writeback |
| **Cache Hierarchy** | L1i, L1d (VIPT/PIPT), L2, L3, cache coherency (MESI/MOESI) |
| **MMU** | Page tables (4-level on ARM64), TLB, ASID |
| **Memory Model** | ARM: weak ordering, acquire/release, barriers |
| **Out-of-Order Execution** | Spectre/Meltdown class attacks |
| **NUMA** | Node topology, memory affinity |

### Resources
| Resource | Link |
|----------|------|
| **The C Programming Language (K&R)** | classic — must own |
| **Computer Systems: A Programmer's Perspective (CSAPP)** | the bible |
| **ARM Cortex-A Series Programmer's Guide** | ARM official |
| **ARM Architecture Reference Manual (ARM ARM)** | armv8-a manual |
| **godbolt.org** | Compiler Explorer — see assembly output |

---

## LEVEL 2: Build Your Own OS

### Path A: MIT 6.S081/6.1810 — xv6 Labs (RECOMMENDED)

xv6 is MIT's teaching OS — re-implementation of Unix V6 for RISC-V multiprocessors.

```
Course Site: https://pdos.csail.mit.edu/6.S081/
Source: https://github.com/mit-pdos/xv6-riscv
Book: https://pdos.csail.mit.edu/6.S081/2024/xv6/book-riscv-rev4.pdf
```

### 11 Labs — Must Complete All

| # | Lab | Skill |
|---|-----|-------|
| 1 | **Utilities** | System call usage, fork/exec/pipe |
| 2 | **System Calls** | Write kernel syscalls (trace, sysinfo) |
| 3 | **Page Tables** | Walk xv6 page tables, add kernel pagetable per process |
| 4 | **Traps** | Exception vectors, trapframe, backtrace |
| 5 | **Lazy Allocation** | Defer physical page allocation until page fault |
| 6 | **Copy-on-Write (COW)** | Fork optimization — share pages, copy on write fault |
| 7 | **Multithreading** | User-level threads, context switching |
| 8 | **Lock Optimization** | Per-CPU freelist, hash-bucket buffer cache lock |
| 9 | **File System** | Large files (double-indirect), symbolic links |
| 10 | **mmap** | Memory-mapped file I/O |
| 11 | **Network Driver** | VirtIO network device driver |

### Path B: OSDev — From Absolute Zero

```
1. Bootloader (GRUB/Multiboot or UEFI)
2. Print to screen (VGA text / UEFI GOP framebuffer)
3. Interrupt handling (IDT / exception vector table)
4. Physical memory manager (bitmap / free-list)
5. Virtual memory + paging (page tables)
6. Heap allocator (kmalloc/kfree)
7. Multitasking (context switch, scheduler)
8. System calls (syscall handler)
9. User mode (ring 3 / EL0 transition)
10. Simple filesystem (FAT or custom)
```

### Resources
| Resource | Link |
|----------|------|
| [OSDev Wiki](https://wiki.osdev.org) | primary resource |
| [xv6 Book (RISC-V)](https://pdos.csail.mit.edu/6.S081/2024/xv6/book-riscv-rev4.pdf) | reading alongside labs |
| [xv6 Source](https://github.com/mit-pdos/xv6-riscv) | code to study |
| [Little OS Book](https://littleosbook.github.io/) | beginner alternative |

---

## LEVEL 3: Linux Kernel Internals — PhD Deep

### Scheduler

```
Process States: RUNNING → RUNNABLE → SLEEPING → STOPPED → ZOMBIE

CFS Algorithm:
  vruntime = actual_runtime × (nice_0_weight / task_weight)
  Pick task with MINIMUM vruntime from red-black tree

EAS Algorithm:
  find_energy_efficient_cpu():
    for each candidate CPU:
      predicted_energy = EM(cpu, utilization_after_placement)
    return CPU with MIN(Δenergy), subject to performance constraint
```

### Memory Management

```
Virtual Memory Architecture (ARM64, 48-bit VA, 4-level):
  [63:48] sign extend
  [47:39] PGD (Level 0) → 512 entries
  [38:30] PUD (Level 1) → 512 entries
  [29:21] PMD (Level 2) → 512 entries
  [20:12] PTE (Level 3) → 512 entries
  [11:0]  Page offset (4KB)

Page Reclaim:
  kswapd (per-NUMA-node) wakes at low watermark → reclaim pages
  3 watermarks: HIGH > LOW > MIN
  Page types: unreclaimable, swappable, syncable, discardable
```

### Synchronization Primitives

| Primitive | Use Case | Implementation |
|-----------|----------|----------------|
| **spin_lock** | Short critical sections (<1μs) | Atomic test-and-set + cpu_relax |
| **mutex** | Sleeping lock | Atomic + wait-queue |
| **rwlock** | Read-heavy | Reader count + writer exclusion |
| **RCU** | Read-mostly data structures | Wait for all readers in quiescent state |
| **seqlock** | Read-mostly with seq num | Sequence number + retry |
| **completion** | One-shot signaling | Completion variable |
| **futex** | Userspace sleeping lock | Fast path: atomic CAS in userspace; Slow path: syscall |
| **MCS lock** | NUMA spinlock | Per-CPU spinning on local flag |

### RCU Deep Dive

```
RCU Lifecycle:
  1. READ: rcu_read_lock() → access data → rcu_read_unlock()
  2. UPDATE: copy data → modify copy → rcu_assign_pointer(ptr, new_copy)
  3. RECLAIM: synchronize_rcu() — wait for all readers → kfree(old_copy)

Memory Ordering:
  Writer: rcu_assign_pointer() = smp_store_release() (WRITE → RELEASE barrier)
  Reader: rcu_dereference() = smp_read_barrier_depends() (CONSUME ordering)
  After pointer load, dependency ordering ensures all accesses through pointer see new data
  (Except Alpha — which needs explicit read barrier)

Quiescent State:
  - Any point where CPU is not in an RCU read-side critical section
  - Context switch = quiescent state (no preempt RCU)
  - synchronize_rcu() waits for ALL CPUs to pass through quiescent state
```

### Key Kernel Concepts

| Topic | Must Know |
|-------|-----------|
| **Page Cache** | radix-tree/xarray, writeback, dirty throttling |
| **Slab Allocator** | kmem_cache, SLUB design, per-CPU caches |
| **Block Layer** | bio, request_queue, I/O scheduler (mq-deadline, kyber, bfq) |
| **Device Tree** | .dts/.dtsi → .dtb, overlays, phandle |
| **Kernel Modules** | insmod/rmmod, modprobe, vermagic, modversions |

### Resources
| Resource | Why |
|----------|-----|
| [Linux Kernel Programming 2E](https://www.packtpub.com/product/linux-kernel-programming/9781803232225) (2024) | Book — covers up to 6.1 LTS, RCU, per-CPU |
| [Linux Kernel Development (Love)](https://www.amazon.com/Linux-Kernel-Development-Robert-Love/dp/0672329468) | Classic — scheduler, memory, syscalls |
| [LWN.net](https://lwn.net) | Weekly kernel news — READ RELIGIOUSLY |
| [Linux Weekly News Kernel Index](https://lwn.net/Kernel/Index/) | Topic-organized articles |
| [kernelnewbies.org](https://kernelnewbies.org) | Beginners portal |
| Bootlin Linux Kernel Docs | https://bootlin.com/doc/ |

---

## LEVEL 4: AOSP/Android Deep Internals

> 📖 See full reference: [[android-rom-learning-repos]]

### Every Subsystem — Must Know Source Path

| Subsystem | Source Path | Key Files |
|-----------|-------------|-----------|
| **Init** | `system/core/init/` | `init.cpp`, `builtins.cpp`, `property_service.cpp` |
| **Zygote** | `frameworks/base/core/java/com/android/internal/os/` | `ZygoteInit.java`, `ZygoteServer.java` |
| **System Server** | `frameworks/base/services/java/com/android/server/` | `SystemServer.java`, `am/`, `wm/`, `pm/` |
| **SurfaceFlinger** | `frameworks/native/services/surfaceflinger/` | `SurfaceFlinger.cpp`, `Layer.cpp` |
| **AudioFlinger** | `frameworks/av/services/audioflinger/` | `AudioFlinger.cpp`, `Threads.cpp` |
| **Binder Driver** | `drivers/android/binder.c` | Kernel side |
| **ART Runtime** | `art/runtime/` | `thread.cc`, `gc/`, `jit/` |
| **ART Compiler** | `art/compiler/optimizing/` | `nodes.h`, `optimizing_compiler.cc` |
| **Keystore** | `system/security/keystore/` | `keystore_main.cpp` |
| **Camera** | `frameworks/av/services/camera/libcameraservice/` | `CameraService.cpp` |

### Key Files Every TOP Engineer Reads
```
frameworks/base/services/core/java/com/android/server/am/ActivityManagerService.java
frameworks/base/services/core/java/com/android/server/wm/WindowManagerService.java
frameworks/native/services/surfaceflinger/SurfaceFlinger.cpp
system/core/init/init.cpp
drivers/android/binder.c
art/runtime/gc/heap.cc
```

### Build & Debug
```bash
# Build single module
mmm frameworks/native/services/surfaceflinger

# Push + restart
adb root && adb remount
adb sync

# Live debug
adb logcat -b all | grep -E "SF|AM|WM" > system_debug.log
```

---

## LEVEL 5: Firmware & Boot Chain

### Firmware Stack (ARM64 Android/ChromeOS)

```
┌─────────────────────────────────────────┐
│ Application Processor (AP)              │
│  Boot ROM (mask ROM, immutable)         │ ← HW root of trust
│    ↓                                    │
│  Bootloader Stage 1 (on-chip SRAM)      │
│    ↓                                    │
│  Bootloader Stage 2 (DRAM):             │
│    ├── U-Boot / Little Kernel (LK)      │ ← Android typical
│    └── coreboot + depthcharge           │ ← ChromeOS
│       ↓                                 │
│  Trusted Firmware-A (TF-A):             │
│    ├── BL1 → BL2 → BL31 (EL3)          │ ← Secure world setup
│    └── BL32 = OP-TEE (S-EL1)           │ ← TEE OS
│       ↓                                 │
│  Linux Kernel / Zircon (EL1)           │ ← OS boot
└─────────────────────────────────────────┘
```

### Key Firmware Components

| Component | Role | Source |
|-----------|------|--------|
| **TF-A (ARM Trusted Firmware)** | EL3 runtime, PSCI, secure boot | https://github.com/ARM-software/arm-trusted-firmware |
| **U-Boot** | Universal bootloader | https://github.com/u-boot/u-boot |
| **Little Kernel (LK)** | Android bootloader (Qualcomm/MTK) | https://github.com/littlekernel/lk |
| **coreboot** | Open-source firmware | https://www.coreboot.org |
| **depthcharge** | ChromeOS verified boot payload | chromium.googlesource.com |
| **TianoCore/EDK2** | Open-source UEFI | https://github.com/tianocore/edk2 |
| **UEFI MinPlatform** | Intel open-source firmware | `edk2-platforms` |

### Verified Boot (AVB)

```
Chain of Trust:
  HW Root Key (eFuses)
    → Boot ROM verifies Bootloader (RSA-2048 signature)
      → Bootloader verifies boot.img (vbmeta)
        → boot.img verifies system/vendor (dm-verity hash tree)
          → Each 4KB block verified on access

vbmeta struct:
  - Hash descriptors (per partition)
  - Hash tree descriptors
  - Chain partition descriptors (chained vbmeta)
  - Public key metadata

AVB Tooling:
  avbtool make_vbmeta_image
  avbtool add_hash_footer --partition_size <N> --partition_name <name>
```

### Must Know
- **Device Tree (DTS/DTB)**: hardware description → kernel
- **ACPI** (x86) vs **Device Tree** (ARM) vs **FDT** (Flattened Device Tree)
- **Fastboot protocol**: flash, erase, boot, getvar
- **Android Boot Image format**: header + kernel + ramdisk + second + dtb
- **GKI (Generic Kernel Image)**: unified kernel across devices

---

## LEVEL 6: Next-Generation OS Architecture

### Fuchsia / Zircon — Google's Next OS

```
Philosophy: microkernel-like + capability-based security

Architecture:
  ┌────────────────────────────────────┐
  │ Components (user-space)            │
  │  ├── Starnix (Linux compat)       │
  │  ├── Filesystems                  │
  │  ├── Network Stack                │
  │  └── Device Drivers               │
  ├────────────────────────────────────┤
  │ Zircon Kernel (privileged)        │
  │  - ~100 syscalls                  │
  │  - Handle-based object system     │
  │  - VDSO (virtual dynamic shared)  │
  │  - Capability-based access        │
  └────────────────────────────────────┘

Concepts:
  - Job: group of processes (resource limits)
  - Process: address space
  - Thread: execution context
  - VMO (Virtual Memory Object): pageable memory
  - Channel: bidirectional IPC (message-based)
  - Port: notification delivery
  - Handle: capability to an object (with rights)
  - VDSO: syscall entry in user space (no SVC instruction direct)
```

### seL4 — Formally Verified Microkernel

```
Verification Status:
  ✓ Functional correctness (C implementation)
  ✓ Binary correctness (compiled binary = C semantics)
  ✓ IPC fastpath correctness
  ✓ Access control enforcement
  ✓ Information-flow noninterference
  ✓ Worst-Case Execution Time (WCET)

Architecture:
  - ~10,000 lines of C (kernel)
  - ~480,000 lines of Isabelle/HOL proofs
  - Capability-based security model
  - Spatial + temporal isolation
  - No dynamic memory allocation in kernel

Concepts:
  - Capability: unforgeable token granting specific rights to an object
  - CNode: capability storage (like a page table for caps)
  - CSpace: capability space per thread
  - VSpace: virtual memory space
  - Endpoint: synchronous IPC channel
  - Notification: asynchronous signal
  - Untyped memory: raw physical memory controlled by capabilities
```

### Key Differences to Understand

| Concept | Linux/Android | Fuchsia/Zircon | seL4 |
|---------|--------------|----------------|------|
| **Kernel type** | Monolithic | Microkernel-like | True microkernel |
| **Drivers** | Kernel space | User space | User space |
| **IPC** | Binder (1-copy mmap) | Channels (message passing) | Endpoints (sync IPC) |
| **Security model** | DAC + MAC (SELinux) | Capability-based | Capability-based |
| **Verification** | None | Partial | Full (machine-checked) |
| **File system** | VFS in kernel | User-space component | None (minimal) |
| **Networking** | Kernel TCP/IP | User-space network stack | None (minimal) |

### Resources
| Resource | Link |
|----------|------|
| Fuchsia Source | https://fuchsia.googlesource.com/fuchsia |
| Zircon Docs | https://fuchsia.dev/fuchsia-src/concepts/kernel |
| seL4 Manual | https://sel4.systems/Info/Docs/seL4-manual-latest.pdf |
| seL4 Proofs | https://github.com/seL4/l4v |
| SIGOPS OSDI papers | https://sigops.org |

---

## LEVEL 7: Formal Methods

### Proof Assistants & Model Checking

| Tool | Use | Ecosystem |
|------|-----|-----------|
| **Isabelle/HOL** | Theorem proving — seL4 verification | Higher-order logic, Sledgehammer |
| **TLA+** | System specification + model checking — distributed systems | PlusCal, TLC model checker |
| **Coq** | Theorem proving — CompCert verified C compiler | Gallina, Ltac |
| **F* (FStar)** | Program verification — verified crypto (HACL*) | Dependent types |
| **CBMC** | Bounded model checking for C programs | SAT/SMT backend |
| **KLEE** | Symbolic execution for C programs | LLVM bitcode |

### What to Actually Learn

```
1. TLA+ First (easiest entry):
   - Write system specifications in TLA+
   - Model check with TLC
   - Learn: https://learntla.com

2. Isabelle/HOL:
   - Understand seL4 proofs (even if you can't write them)
   - Read: seL4: Formal Verification of an OS Kernel (SOSP 2009 paper)

3. CBMC/KLEE (practical for kernel code):
   - Verify your kernel patches with bounded model checking
   - Find bugs before they reach production
```

### Key Papers
| Paper | Conference | Year |
|-------|-----------|------|
| seL4: Formal Verification of an OS Kernel | SOSP | 2009 |
| Comprehensive Formal Verification of an OS Microkernel | TOPLAS | 2014 |
| Verified LISP Implementations on ARM, x86, and RISC-V | PLDI | 2023 |
| Cogent: Verifying High-Level Language Implementation | ASPLOS | 2024 |

### Resources
| Resource | Link |
|----------|------|
| Learn TLA+ | https://learntla.com |
| TLA+ Video Course | https://lamport.azurewebsites.net/video/videos.html |
| seL4 Proofs | https://github.com/seL4/l4v |
| VST (Verified Software Toolchain) | https://vst.cs.princeton.edu |

---

## LEVEL 8: Security Research — CVE/Exploit/Fuzzing

### Vulnerability Discovery Pipeline

```
1. ATTACK SURFACE MAPPING (per subsystem):
   Binder: ioctl(BINDER_WRITE_READ), transactions, mmap, ref counting
   Kernel: syscalls, ioctls, netlink, filesystem operations
   RIL: sockets, AT commands, SIPC packets
   HAL: HwBinder/AIDL interfaces, shared memory

2. STATIC ANALYSIS:
   CodeQL (GitHub) — query Android source
   Semgrep — pattern matching
   Manual code review — focus on:
     - Copy_from_user / copy_to_user
     - Integer overflows in size calculations
     - Race conditions (TOCTOU)
     - Use-after-free in ref-counted objects
     - Missing bounds checks

3. FUZZING:
   syzkaller → Linux kernel syscalls (Google's tool, 4000+ bugs)
   libFuzzer → userspace libraries
   AFL++ → generic binary fuzzing
   NASS → Android native services via Binder (USENIX 2025)
   BTFuzzer → Bluetooth protocol stack

4. EXPLOIT DEVELOPMENT:
   Primitive: arbitrary read/write
   KASLR bypass: info leak
   Heap spray: groom for predictable layout
   ROP/JOP: control flow after DEP
   Post-exploit: disable SELinux, extract keys
```

### Android Kernel Exploit Mitigations

| Mitigation | Kernel Config | Bypass Difficulty (2025) |
|-----------|---------------|--------------------------|
| **KASLR** | `CONFIG_RANDOMIZE_BASE` | Requires info leak |
| **KPTI** | `CONFIG_PAGE_TABLE_ISOLATION` | Side-channel |
| **SMAP/SMEP** | `CONFIG_ARM64_SW_TTBR0_PAN` | ROP to kernel data only |
| **KCFI** | `CONFIG_CFI_CLANG` | Counterfeit code paths |
| **Shadow Call Stack** | `CONFIG_SHADOW_CALL_STACK` | Corrupt shadow stack too |
| **PXN/PAN** | ARMv8.1 hardware | Cannot execute user pages |
| **MTE** | `CONFIG_ARM64_MTE` | Very hard — tagged memory |
| **PAC** | ARMv8.3-A pointer auth | Forge valid PAC signature |
| **BTI** | ARMv8.5-A branch target | Cannot JOP to arbitrary instr |
| **SELinux** | `CONFIG_SECURITY_SELINUX` | Disable via kernel write |

### Fuzzing Setup (Practical)

```bash
# syzkaller for Android kernel
git clone https://github.com/google/syzkaller
cd syzkaller && make

# Create config
{
  "target": "linux/arm64",
  "http": "localhost:56741",
  "workdir": "/workdir",
  "kernel_obj": "/android-kernel/out",
  "kernel_src": "/android-kernel",
  "syzkaller": "/syzkaller",
  "image": "/boot.img",
  "type": "adb"
}
```

### CVE Research — Key Git Repos
| Repo | Description |
|------|-------------|
| [syzkaller](https://github.com/google/syzkaller) | Kernel fuzzer |
| [Android Security Bulletins](https://source.android.com/docs/security/bulletin) | Monthly CVEs |
| [AOSP Security](https://source.android.com/docs/security) | Official docs |
| [oss-security mailing list](https://www.openwall.com/lists/oss-security/) | CVE disclosures |
| [google/security-research](https://github.com/google/security-research) | Google Project Zero style |

---

## LEVEL 9: TEE & TrustZone Programming

### Build Your Own TEE App

> See full TA/CA code in [[android-rom-learning-repos]] TEE Programming section

### Architecture

```
SMC Calling Convention (ARM SMCCC):
  Function ID format:
    [31]    = 1 (SMC) or 0 (HVC)
    [30]    = 1 (64-bit) or 0 (32-bit)
    [29:24] = Service Call Range
    [23:16] = Reserved
    [15:0]  = Function Number

  Standard SMC functions:
    SMC32/64: 0x8200xxxx (PSCI, SiP, OEM, etc.)
    FAST call: bit[31]=1, bit[30]=1, bit[15:0]!=0xFFFF

World Switch (Cost):
  ~2-5 μs for SMC on modern ARM SoCs
  Includes: context save/restore, cache/TLB flush if needed
```

### OP-TEE Internals

```
OP-TEE memory layout:
  [S-EL1] OP-TEE OS: ~512KB-2MB
  [S-EL0] Trusted Applications: per-TA memory pool
  TZASC: hardware firewall between secure/non-secure memory regions
  TZPC: peripheral protection (GPIO, I2C, etc.)

OP-TEE build:
  make PLATFORM=vexpress-qemu_armv8a \
       CFG_TEE_CORE_LOG_LEVEL=4 \
       CFG_TEE_TA_LOG_LEVEL=4

TA signing (production):
  script/sign.py --key /path/to/private_key.pem --uuid <ta_uuid>
```

### Trusty (Google's TEE for Pixel)

```
Trusty architecture:
  - Runs on ARM TrustZone (S-EL1)
  - Provides Trusty API (not GlobalPlatform)
  - Used by: Keymaster, Weaver, Gatekeeper, Fingerprint
  - Communication: Android → Trusty via /dev/trusty-ipc-dev0
  - Trusted Apps (.trustyapp)

Keymaster in Trusty:
  Key generation → Trusty → never leaves secure world
  Encryption/decryption → Trusty → returns result only
  Attestation → Trusty signs with hardware-backed key
```

### Write Your Own TA — Hands-on

```bash
# Setup OP-TEE dev environment
git clone https://github.com/OP-TEE/build.git
cd build
make -j$(nproc) toolchains
make -j$(nproc) QEMU

# Run OP-TEE + Normal World Linux
make QEMU_XTERM=1 run

# Inside QEMU Linux:
optee_example_hello_world    # Run built-in example

# Build your own TA:
# 1. Create ta/ with TA_CreateEntryPoint, TA_InvokeCommandEntryPoint, etc.
# 2. Create host/ with TEEC_OpenSession, TEEC_InvokeCommand
# 3. Cross-compile, sign, deploy to /lib/optee_armtz/
```

### Advanced TEE Topics
- **Secure Storage**: RPMB on eMMC — anti-rollback, replay-protected
- **Secure Time**: TEE-controlled monotonic counter
- **Widevine L1**: DRM in TEE — decrypted video never exposed to normal world
- **FIDO2/WebAuthn**: U2F keys in TEE
- **Payment**: EMVCo certified TEE (Google Pay, Samsung Pay)
- **Remote Attestation**: prove to remote server that key is TEE-backed

---

## LEVEL 10: Real Engineering — The Top

### Upstream Contribution

```
Linux Kernel contribution workflow:
  1. Find subsystem: https://lore.kernel.org/lists.html
  2. Read Documentation/process/submitting-patches.rst
  3. Write patch → ./scripts/checkpatch.pl --strict
  4. git format-patch -1 → send to maintainer + mailing list
  5. Address review comments → v2, v3, ...
  6. Maintainer picks up → linux-next → Linus merge window

AOSP contribution:
  1. git clone AOSP → make change
  2. repo upload → Gerrit code review
  3. Address comments → get +2 → merged
```

### Performance Engineering

```
Methodology:
  1. MEASURE FIRST: don't optimize what you haven't profiled
  2. Establish baseline: perf stat, perf record, simpleperf
  3. Find bottleneck: flame graphs, tracepoints
  4. Fix: algorithm → data structure → cache → code gen
  5. Verify: same workload, same metrics, before/after

Profiling Stack (top to bottom):
  Perfetto (system-wide trace)
  simpleperf (CPU sampling)
  ftrace (kernel function trace)
  perf (hardware counters)
  FlameGraph (visualization)
  
Key Metrics:
  - IPC (instructions per cycle) — <1 means stall
  - Cache miss rate (L1/L2/L3)
  - Branch misprediction rate
  - TLB miss rate
  - Scheduler: context switch rate, wakeup latency
```

### Code Review — Critical Eye

```
Checklist (per patch):
  [ ] Concurrency: are there race conditions? lock ordering?
  [ ] Memory: is every allocation freed? use-after-free?
  [ ] Error paths: are all errors handled? goto cleanup?
  [ ] Integer safety: overflow/underflow in arithmetic?
  [ ] Input validation: bounds check on all user/kernel boundaries?
  [ ] API contract: does function adhere to documented behavior?
  [ ] Performance: any O(N²) where N can grow large?
  [ ] Backward compatibility: does it break existing interfaces?
  [ ] Security: does it expand attack surface?
  [ ] Testability: can this be tested? are tests included?
```

### Reading Production Code

```
Code to study DEEPLY:
  1. Linux kernel: kernel/sched/fair.c (CFS), mm/page_alloc.c
  2. AOSP: SurfaceFlinger, AMS, SystemServer
  3. Fuchsia: Zircon kernel object system
  4. seL4: verified kernel source
  5. SQLite: famously well-tested (~1000x more test code than production code)

Reading technique:
  - Start from main entry point → trace execution
  - Draw call graph on paper
  - For each function: what's the contract? what are the pre/post conditions?
  - Find the data structures first — code follows data
```

### Mentality of a TOP Engineer

```
TOP Engineer habits:
  ✓ RTFM (Read The F***ing Manual) — ARM ARM, Intel SDM, Linux man pages
  ✓ Read the source — not the blog post, the ACTUAL CODE
  ✓ Measure, don't guess — perf, ftrace, flame graphs
  ✓ Write tests that break — not tests that pass
  ✓ Understand WHY, not just WHAT — first principles
  ✓ Contribute upstream — the best way to learn is to be reviewed
  ✓ Teach others — writing docs/presentations deepens your understanding
  ✓ Assume you're wrong — double-check everything
  ✓ Complexity is the enemy — simplicity is the highest form
  ✓ Never stop learning — this curriculum is just the start
```

---

## 📅 12-Month Study Plan

| Month | Level | Focus |
|-------|-------|-------|
| **1** | 1-2 | C/Assembly mastery + xv6 labs 1-6 |
| **2** | 2-3 | xv6 labs 7-11 + Linux kernel book Ch 1-5 |
| **3** | 3 | Linux kernel: scheduler (fair.c), memory (page_alloc.c), RCU |
| **4** | 3-4 | Linux kernel: sync primitives + AOSP: init, zygote, SystemServer |
| **5** | 4 | AOSP: SurfaceFlinger, AudioFlinger, Camera HAL |
| **6** | 4-5 | AOSP: Binder driver, ART runtime + Firmware: TF-A, U-Boot, AVB |
| **7** | 5-6 | Firmware deep dive + Fuchsia/Zircon architecture |
| **8** | 6-7 | seL4 paper + TLA+ basics + Zircon source study |
| **9** | 7-8 | Formal methods practice + CVE research methodology |
| **10** | 8-9 | Fuzzing setup (syzkaller) + OP-TEE TA development |
| **11** | 9-10 | TEE project + upstream contribution (send first patch) |
| **12** | 10 | Performance engineering + code review + capstone project |

---

## 🎯 Capstone Projects (เลือก 1)

### Project A: Build Your Own Microkernel
```
Spec:
  - ARM64 (AArch64), EL1
  - Boot on QEMU virt machine
  - EL0 user-space with 2 syscalls (write, yield)
  - Page table setup (identity map → separate address spaces)
  - Context switch between 2 user threads
  - UART output for debugging
```

### Project B: Write a Linux Kernel Module
```
Build a character device driver that:
  - Implements open/read/write/ioctl/mmap/release
  - Uses RCU for read-heavy data structure
  - Implements proper error handling and resource cleanup
  - Has measurable performance (compare against /dev/zero)
  - Submit concept to LKML for review
```

### Project C: Port a HAL to AIDL
```
Take an existing HIDL HAL → rewrite as AIDL:
  1. Define .aidl interface
  2. Implement server-side (vendor process)
  3. Implement client-side (system service)
  4. Write VTS tests
  5. SELinux policy for new service
```

### Project D: Find & Report a Real CVE
```
1. Choose target: Android kernel, AOSP framework, or vendor HAL
2. Map attack surface
3. Static analysis + fuzzing
4. Triage crashes → determine exploitability
5. Write PoC
6. Report to vendor / AOSP security team
7. Write up findings (blog / conference submission)
```

---

## 👥 Team Assignment — 12-Month Plan

| Member | Primary Focus | Secondary | Capstone |
|--------|--------------|-----------|----------|
| **NOVA** ⚡ | Levels 1-3 (Foundation) + All overview | System architecture | Project A (Microkernel) |
| **CYPHER** 🔐 | Levels 1-3 (Kernel) + Level 9 (TEE) | Level 8 (Security) | Project D (CVE) |
| **AURA** ✨ | Level 4 (Graphics) + Level 6 (Fuchsia) | Level 7 (Formal UI specs) | Project C (HAL AIDL) |
| **FORGE** 🏗️ | Level 2 (xv6) + Level 4 (ART/Binder) | Level 7 (TLA+) | Project B (Kernel Module) |
| **FLUX** 🔄 | Level 3 (Kernel Build) + Level 5 (Firmware) | Level 10 (Profiling) | CI/CD pipeline for AOSP |
| **VECTOR** 🎯 | Level 4 (HAL) + Level 5 (DT/Firmware) | Level 9 (TEE) | Project C (HAL AIDL) |
| **EMBER** 🔥 | Level 8 (Security/Fuzzing) + Level 10 (QA) | Level 2 (xv6) | Project D (CVE) |

---

## 📚 Essential Reading List (Own These Books)

| # | Book | Why |
|---|------|-----|
| 1 | K&R C Programming Language | C bible |
| 2 | CSAPP (Computer Systems: A Programmer's Perspective) | Architecture bible |
| 3 | Linux Kernel Development (Love) | Kernel entry point |
| 4 | Linux Kernel Programming 2E (Billimoria, 2024) | Modern kernel development |
| 5 | ARM Architecture Reference Manual | ARM64 authority |
| 6 | Inside the Android OS (Meike, 2021) | Android internals |
| 7 | 《Android Runtime源码解析》(史宁宁, 2022) | ART deep dive |
| 8 | xv6 Book (RISC-V edition) | Teaching OS |
| 9 | The Art of UNIX Programming (Raymond) | Systems philosophy |
| 10 | Code Complete 2 (McConnell) | Software engineering |
| 11 | Designing Data-Intensive Applications (Kleppmann) | Systems thinking |
| 12 | Operating Systems: Three Easy Pieces (Remzi) | Core OS concepts |

---

## 🧭 Resources Index

| Category | Resource |
|----------|----------|
| **OS Foundation** | [xv6 Book](https://pdos.csail.mit.edu/6.S081/2024/xv6/book-riscv-rev4.pdf), [OSDev Wiki](https://wiki.osdev.org) |
| **Linux Kernel** | [kernel.org/doc](https://kernel.org/doc), [LWN.net](https://lwn.net), [kernelnewbies](https://kernelnewbies.org) |
| **AOSP/Android** | [source.android.com](https://source.android.com), [cs.android.com](https://cs.android.com), [[android-rom-learning-repos]] |
| **Firmware** | [TF-A](https://github.com/ARM-software/arm-trusted-firmware), [coreboot](https://coreboot.org), [TianoCore](https://github.com/tianocore/edk2) |
| **New OS** | [Fuchsia](https://fuchsia.dev), [seL4](https://sel4.systems), [Zircon](https://fuchsia.googlesource.com/fuchsia/+/refs/heads/main/zircon/) |
| **Formal Methods** | [Learn TLA+](https://learntla.com), [l4v proofs](https://github.com/seL4/l4v) |
| **Security** | [syzkaller](https://github.com/google/syzkaller), [AOSP Security](https://source.android.com/docs/security) |
| **TEE** | [OP-TEE](https://optee.readthedocs.io), [Trusty](https://source.android.com/docs/security/features/trusty) |
| **Papers** | [USENIX Security](https://www.usenix.org/conference/usenixsecurity25), [ACM CCS](https://www.sigsac.org/ccs.html), [NDSS](https://www.ndss-symposium.org) |

---

**Why:** Complete TOP OS Engineer curriculum — from C programming to verified kernels, from xv6 to Fuchsia. Systematically structured 10 levels with 12-month plan.
**How to apply:** Follow levels in order. Each team member specializes in their assigned area. Weekly study sessions. Monthly progress reviews.
