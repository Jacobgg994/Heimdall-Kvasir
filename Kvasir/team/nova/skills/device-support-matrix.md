# Device Support Matrix

## Device Selection Criteria

| Criterion | Minimum | Preferred | Notes |
|-----------|---------|-----------|-------|
| **SoC** | Snapdragon 7xx+ | Snapdragon 8xx | Best CAF/Linux support |
| **RAM** | 4 GB | 6 GB+ | Android 14+ needs 4GB minimum |
| **Kernel** | 4.19+ | 5.10+ | Older kernels need heavy backporting |
| **Bootloader** | Unlockable | Treble-compatible | Project Treble required for seamless |
| **Community** | 5+ ROMs | 20+ ROMs | Indicates good device support |
| **Source** | Kernel source released | GKI-compatible | Essential for custom kernel |

## SoC Compatibility Matrix

| SoC | Linux Version | CAF Tag | GPU | Notes |
|-----|--------------|---------|-----|-------|
| SD865 (sm8250) | 5.10+ | LA.UM.9.12 | Adreno 650 | Mature, well-supported |
| SD888 (sm8350) | 5.10+ | LA.UM.9.12 | Adreno 660 | Heat issues in FDE |
| SD8 Gen1 (sm8450) | 5.10+ | LA.UM.9.12 | Adreno 730 | Needs good cooling |
| SD8+ Gen1 (sm8475) | 5.10+ | LA.UM.9.12 | Adreno 730 | TSMC fab = better |
| Dimensity 8100 | 5.10+ | MTK | Mali-G610 | MTK is harder to support |
| Tensor G1 (s5e9845) | 5.10+ | Exynos | Mali-G78 | Samsung-specific patches |

## Kernel Version Requirements

| AOSP Version | Min Kernel | Recommended Kernel | GKI |
|-------------|-----------|-------------------|-----|
| Android 13 | 4.19 | 5.10 | 5.10 |
| Android 14 | 5.10 | 5.15 | 5.15 |
| Android 15 | 5.15 | 6.1 | 6.1 |

## Feature & Device Mapping

```
Feature Ready       ├── Device A (SD865) ── All good
                    ├── Device B (SD8G1) ── Camera HAL pending
                    └── Device C (Dimensity) ── Boot only
```

## Device Tier System

| Tier | Condition | Release Treatment |
|------|-----------|-------------------|
| **Tier 1** | All HALs work, no major bugs | Ship with Stable |
| **Tier 2** | Core features work, minor bugs | Ship with Beta |
| **Tier 3** | Boot only, basic functionality | Experimental only |
| **Tier 4** | Doesn't boot or major blocker | Hold until resolved |
