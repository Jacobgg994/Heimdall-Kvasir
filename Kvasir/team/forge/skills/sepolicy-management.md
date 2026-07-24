# SELinux Policy Management

## Policy File Locations

| Path | Purpose |
|------|---------|
| `system/sepolicy/` | Core AOSP SELinux policy |
| `system/sepolicy/private/` | Private (OEM-hidden) policy |
| `system/sepolicy/public/` | Public policy (vendor-accessible) |
| `system/sepolicy/vendor/` | Vendor-specific policy |
| `device/<oem>/<codename>/sepolicy/` | Device-specific policy |
| `device/<oem>/<codename>/sepolicy/vendor/` | Device vendor policy |

## Device-Specific Policy Structure

```
device/<oem>/<codename>/sepolicy/
├── vendor/
│   ├── file_contexts          # File labeling (additions)
│   ├── genfs_contexts         # Pseudo-filesystem contexts
│   ├── property_contexts      # System property security contexts
│   ├── service_contexts       # Service labeling
│   └── <domain>.te            # Domain type enforcement rules
```

## Common Policy Additions

### 1. Custom System Service (from FORGE's custom service)
```
# device/<oem>/<codename>/sepolicy/vendor/kvasir_service.te
type kvasir_service, domain;
type kvasir_service_exec, exec_type, file_type, vendor_file_type;

init_daemon_domain(kvasir_service)

allow kvasir_service self:capability { net_admin sys_admin };
allow kvasir_service system_prop:property_service set;
allow kvasir_service system_server:binder { call transfer };
```

### 2. New System Property
```
# device/<oem>/<codename>/sepolicy/vendor/property_contexts
ro.kvasir.version     u:object_r:system_prop:s0
persist.kvasir.debug  u:object_r:system_prop:s0
```

### 3. Custom HAL Access
```
# device/<oem>/<codename>/sepolicy/vendor/hal_custom.te
type hal_custom, domain;
type hal_custom_exec, exec_type, file_type, vendor_file_type;
hal_server_domain(hal_custom)

allow hal_custom self:capability { net };
allow hal_custom system_data_file:dir rw_dir_perms;
```

## Writing .te Files

### Syntax
```
# allow <source> <target>:<class> { <permissions> };
# neverallow <source> <target>:<class> { <permissions> };

# Example: allow kvasir service to read system properties
allow kvasir_service system_prop:file read;

# Example: never allow system_server to execute arbitrary code
neverallow system_server self:process execmem;
```

### Common Permission Sets
```makefile
# Use macros from global_macros
r_file_perms        # read, open, getattr, lock
w_file_perms        # write, append
rw_file_perms       # read + write
x_file_perms        # execute
rw_dir_perms        # read, write directory
create_file_perms   # create, setattr, rename, unlink, etc.
```

## Debugging SELinux Denials

```bash
# Check for denials in real-time
adb logcat -b events | grep avc

# Read full denial from dmesg
adb shell dmesg | grep avc

# Generate policy from denials (quick fix - not for production)
adb shell setenforce 0  # Temporarily disable
# ... test your feature ...
adb shell setenforce 1  # Re-enable

# Generate policy from denials using audit2allow
adb shell dmesg | grep avc | audit2allow -p out/target/product/<device>/root/sepolicy
```

## Understanding AVC Denial Messages

```
avc: denied { read } for pid=1234 comm="kvasir_service" name="property"
    scontext=u:r:kvasir_service:s0
    tcontext=u:object_r:system_prop:s0
    tclass=file permissive=0

Interpretation:
- denied { read }        → Operation denied
- comm="kvasir_service"  → Source domain
- tcontext=...system_prop → Target label
- tclass=file            → Object class
- permissive=0           → Actually enforced (not just logged)
```

## Neverallow Rules — What NOT to Do

```makefile
# These are enforced at build time and compile-time checked
# NEVER add these to device policy:

neverallow { domain -init -shell } kernel:system { sys_nice };
neverallow { domain -init } self:capability sys_admin;
neverallow { appdomain } self:process execmem;
```

## Compile and Deploy

```bash
# Rebuild just sepolicy
make sepolicy -j$(nproc)

# Full rebuild if policy affects init
make bootimage -j$(nproc)

# Test policy
adb root
adb shell setenforce 1
# Run your feature and check for denials
```
