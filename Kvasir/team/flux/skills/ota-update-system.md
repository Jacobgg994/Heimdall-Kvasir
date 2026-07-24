# OTA Update System — A/B (Seamless) Updates

## OTA Types

| Type | Size | Reboot Required | Use Case |
|------|------|-----------------|----------|
| **Full OTA** | 1.5-2.5 GB | Yes | Initial install, major version upgrade |
| **Incremental OTA** | 50-500 MB | Yes | Monthly security patch, minor update |
| **Delta OTA** | 10-100 MB | Yes | Critical patch, small fix |
| **A/B Seamless** | Full | No (background install) | All updates |

## A/B (Seamless) Update Architecture

```
Slot A (current)
├── boot_a
├── system_a
└── vendor_a

Slot B (inactive)
├── boot_b
├── system_b
└── vendor_b
```

### Update Flow
```
1. Download OTA in background
2. Apply to inactive slot while system runs
3. Set new slot as active
4. Reboot → bootloader loads new slot
5. On success, mark slot as good
6. On failure, fallback to old slot
```

## OTA Package Generation

### Full OTA
```bash
# Generate full OTA
make otapackage -j$(nproc)

# Output: out/target/product/<device>/<device>-ota-<timestamp>.zip
```

### Incremental OTA
```bash
# Need target_files for both old and new build
./build/tools/releasetools/ota_from_target_files \
  -i out/target/product/<device>/previous-target_files.zip \
  -k build/make/target/product/security/testkey \
  out/target/product/<device>/obj/PACKAGING/target_files_intermediates/<device>-target_files-<hash>.zip \
  incremental-ota-update.zip
```

## OTA Signing

### Sign OTA package
```bash
# Using signapk
java -jar out/host/linux-x86/framework/signapk.jar \
  -w build/make/target/product/security/releasekey.x509.pem \
  build/make/target/product/security/releasekey.pk8 \
  unsigned-ota.zip signed-ota.zip
```

### Keys
| Key | Purpose |
|-----|---------|
| `testkey` | Development builds |
| `releasekey` | Production releases |
| `platform` | Platform-signed apps |

## OTA Configuration

### Build Flags
```makefile
# BoardConfig.mk
AB_OTA_UPDATER := true
AB_OTA_PARTITIONS := boot system vendor dtbo
```

### OTA Config File
```xml
<!-- META-INF/com/android/otacert in OTA zip -->
<policy>
    <update type="ab">
        <payload>
            <offset>...</offset>
            <size>...</size>
            <metadata_size>...</metadata_size>
            <metadata_signature>...</metadata_signature>
            <hash>sha256:...</hash>
        </payload>
        <properties>
            <property name="ota-type" value="AB" />
            <property name="pre-device" value="<codename>" />
        </properties>
    </update>
</policy>
```

## OTA Server Setup (Simple)

```python
# Simple Python-based OTA server for testing
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class OTAHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # OTA client checks for update
        if self.path == '/api/v1/check_update':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"version":"14.0-20260724","url":"/ota/update.zip"}')
        else:
            super().do_GET()

HTTPServer(('0.0.0.0', 8080), OTAHandler).serve_forever()
```

## Testing OTA

```bash
# Force update check
adb shell am broadcast -a android.intent.action.CHECK_OTA

# Manually trigger update
adb shell update_engine_client --payload file:///data/ota/update.zip \
  --update --headers="\
  FILE_HASH=<sha256>,\
  FILE_SIZE=<size>,\
  METADATA_HASH=<sha256>,\
  METADATA_SIZE=<size>"

# Check slot status
adb shell update_engine_client --status
```
