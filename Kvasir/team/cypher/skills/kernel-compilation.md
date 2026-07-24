# Kernel Compilation — ARM64 Cross-Compile Guide

## Toolchain Setup

### Option A: AOSP Prebuilts (recommended)
```bash
# Within AOSP source
export PATH=<AOSP_ROOT>/prebuilts/clang/host/linux-x86/clang-r487747/bin:$PATH
export PATH=<AOSP_ROOT>/prebuilts/gcc/linux-x86/aarch64/aarch64-linux-android-4.9/bin:$PATH
```

### Option B: Standalone Clang (for non-AOSP builds)
```bash
# Download from Android Gerrit or GitHub releases
wget https://android.googlesource.com/platform/prebuilts/clang/host/linux-x86/+archive/refs/heads/main/clang-r487747.tar.gz
tar -xzf clang-r487747.tar.gz
export PATH=$(pwd)/clang-r487747/bin:$PATH
```

## Build Commands

### Basic kernel build
```bash
# One-shot
make ARCH=arm64 O=out CC=clang \
  CLANG_TRIPLE=aarch64-linux-gnu- \
  CROSS_COMPILE=aarch64-linux-android- \
  vendor/<codename>-defconfig

make ARCH=arm64 O=out CC=clang \
  CLANG_TRIPLE=aarch64-linux-gnu- \
  CROSS_COMPILE=aarch64-linux-android- \
  -j$(nproc) 2>&1 | tee build.log
```

### Build with LTO (performance)
```bash
# Add to defconfig or command line
CONFIG_LTO_CLANG_FULL=y
CONFIG_THINLTO=y  # Faster than full LTO

# Build command with LTO flag
make ... LD=ld.lld AR=llvm-ar NM=llvm-nm OBJCOPY=llvm-objcopy OBJDUMP=llvm-objdump \
  STRIP=llvm-strip LLVM=1 LLVM_IAS=1
```

### Build kernel modules
```bash
make ARCH=arm64 O=out ... modules
make ARCH=arm64 O=out ... modules_install INSTALL_MOD_PATH=./modules
```

## Defconfig Management

### Create device defconfig
```bash
# From base defconfig + fragment
make ARCH=arm64 O=out vendor/<base>-defconfig
./scripts/kconfig/merge_config.sh -O out \
  arch/arm64/configs/vendor/<base>-defconfig \
  arch/arm64/configs/vendor/<device>-fragment.config
cp out/.config arch/arm64/configs/vendor/<device>_defconfig
```

### Common defconfig flags for custom ROM
```config
CONFIG_IKHEADERS=y
CONFIG_KALLSYMS=y
CONFIG_DEBUG_KERNEL=n
CONFIG_BLK_DEV_IO_TRACE=y
CONFIG_STACKTRACE=y
CONFIG_STRICT_MEMORY_RWX=y
CONFIG_RCU_BOOST=y
```

## Output

After successful build:
```
out/arch/arm64/boot/Image           # Kernel image
out/arch/arm64/boot/Image.gz        # Compressed
out/arch/arm64/boot/dts/qcom/*.dtb  # Device tree blobs
out/arch/arm64/boot/dtbo.img        # DTBO image
```

## AnyKernel3 Packaging

```bash
# Clone AnyKernel3 template
git clone https://github.com/osm0sis/AnyKernel3
cp out/arch/arm64/boot/Image.gz <anykernel>/
cp out/arch/arm64/boot/dtb <anykernel>/dtb  # If standalone
cd <anykernel>
zip -r9 <kernel>-<device>-<version>.zip * -x .git README.md *placeholder
```
