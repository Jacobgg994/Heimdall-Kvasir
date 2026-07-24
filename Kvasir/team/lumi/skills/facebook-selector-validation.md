---
name: facebook-selector-validation
description: ตรวจสอบว่า Facebook XPath selectors ยังใช้ได้อยู่ — detect UI changes, document fallback patterns
metadata:
  type: skill
  category: gemlogin
  owner: lumi
---

# 🔍 Facebook Selector Validation Guide

> ตรวจสอบและ validate selectors ใน GemLogin workflow — จับ Facebook UI changes ก่อน workflow พัง
> อัปเดตล่าสุด: 2026-06-29

---

## 1. Why Validate Facebook Selectors?

Facebook เปลี่ยน UI layout selector บ่อย — โดยเฉพาะ:
- **หลังอัปเดต major** — layout overhaul ทุก 2-3 เดือน
- **A/B testing** — profile 的不同 อาจเห็น selector ต่างกัน
- **Platform version** — mobile web / desktop / lite ใช้ DOM structure ต่างกัน
- **Language setting** — `@aria-label` เปลี่ยนตามภาษา

**Selector risk levels:**
| Risk | Description | Check Frequency |
|------|-------------|-----------------|
| 🔴 High | `contains(@class, ...)` — class name เปลี่ยนบ่อย | ทุกสัปดาห์ |
| 🟡 Medium | `@aria-label` — stable กว่า class แต่เปลี่ยนได้ | ทุก 2 สัปดาห์ |
| 🟢 Low | `starts-with(@aria-label, ...)` / `normalize-space(.)` — stable ที่สุด | ทุกเดือน |

---

## 2. Selector Validation Process

### Step 1: Extract Selectors from Workflow

```python
import json

def extract_selectors(filepath):
    with open(filepath) as f:
        wf = json.load(f)
    
    selectors = []
    nodes = wf.get('drawflow', {}).get('nodes', [])
    
    for n in nodes:
        data = n.get('data', {})
        label = n.get('label', '')
        nid = n.get('id', '?')
        
        selector = data.get('selector', '')
        wait_timeout = data.get('waitSelectorTimeout', 5000)
        
        if selector:
            selectors.append({
                'node_id': nid,
                'node_label': label,
                'selector': selector,
                'timeout': wait_timeout,
                'has_wait': data.get('waitForSelector', False)
            })
    
    return selectors
```

### Step 2: Categorize Selectors

| Category | Pattern | Example | Stability |
|----------|---------|---------|-----------|
| **Navigation** | `@aria-label` | `//a[@aria-label="Home"]` | 🟢 High |
| **Actions** | `normalize-space(.)` | `//*[normalize-space(.)="Share"]` | 🟢 High |
| **StartsWith** | `starts-with(@aria-label,...)` | `//div[starts-with(@aria-label,"Like:")]` | 🟢 High |
| **Contains** | `contains(@aria-label,...)` | `//a[contains(@aria-label,"profile")]` | 🟡 Medium |
| **Class-based** | `contains(@class,...)` | `//div[contains(@class,"x1n2onrg")]` | 🔴 High |
| **Position-based** | `[N]` or `last()` | `(//div[@role="textbox"])[1]` | 🔴 High |
| **Text content** | `text()` or `.` | `//span[text()="Like"]` | 🟡 Medium |

### Step 3: Test Selectors on Live Profile

วิธีทดสอบ selector ว่าใช้ได้:

```javascript
// 1. เปิด Facebook บน GemLogin profile
// 2. ใช้ Developer Tools หรือ CDP Runtime.evaluate

// ทดสอบ selector
const selector = '//div[@aria-label="Like"]';
const result = document.evaluate(
  selector,
  document,
  null,
  XPathResult.FIRST_ORDERED_NODE_TYPE,
  null
);
console.log('Found:', result.singleNodeValue !== null);

// นับจำนวน matches
const snapshot = document.evaluate(
  selector,
  document,
  null,
  XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
  null
);
console.log('Count:', snapshot.snapshotLength);

// รายละเอียด element ที่เจอ
if (result.singleNodeValue) {
  console.log('Tag:', result.singleNodeValue.tagName);
  console.log('Visible:', result.singleNodeValue.offsetParent !== null);
  console.log('Text:', result.singleNodeValue.textContent?.trim());
}
```

### Step 4: Batch Validation Script

```python
import json
import subprocess
import sys

def batch_validate_selectors(workflow_path, cdp_url):
    """Validate all selectors via CDP"""
    selectors = extract_selectors(workflow_path)
    
    results = []
    for s in selectors:
        # Inject test via CDP Runtime.evaluate
        test_script = f"""
        (() => {{
            const selector = {json.dumps(s['selector'])};
            try {{
                const result = document.evaluate(
                    selector, document, null,
                    XPathResult.FIRST_ORDERED_NODE_TYPE, null
                );
                const found = result.singleNodeValue !== null;
                const visible = found ? result.singleNodeValue.offsetParent !== null : false;
                const tag = found ? result.singleNodeValue.tagName : '';
                return JSON.stringify({{found, visible, tag, selector}});
            }} catch(e) {{
                return JSON.stringify({{found: false, error: e.message, selector}});
            }}
        }})()
        """
        
        # ส่ง CDP command
        # (Implementation depends on CDP connection method)
        
        results.append({
            'selector': s['selector'],
            'node_label': s['node_label'],
            'status': 'valid' if found else 'stale',
            'visible': visible,
            'node_id': s['node_id']
        })
    
    # Summary
    valid = sum(1 for r in results if r['status'] == 'valid')
    stale = sum(1 for r in results if r['status'] == 'stale')
    
    print(f"✅ Valid: {valid}/{len(results)}")
    print(f"❌ Stale: {stale}/{len(results)}")
    
    if stale > 0:
        print("\n=== Stale Selectors ===")
        for r in results:
            if r['status'] == 'stale':
                print(f"  [{r['node_label']}] {r['selector'][:80]}")
    
    return results
```

---

## 3. Selector Health Scoring

### Scoring Criteria

| Factor | Score | Weight |
|--------|-------|--------|
| Selector type stability | 0-10 | 40% |
| Fallback availability | 0/10 | 25% |
| Validation history | 0-10 | 20% |
| Wait timeout adequacy | 0/10 | 15% |

**Selector Health = weighted average**

### Score Interpretation

| Score | Meaning | Action |
|-------|---------|--------|
| 8-10 | 🟢 Healthy | No action needed |
| 5-7 | 🟡 Warning | Monitor, plan refresh |
| 3-4 | 🟠 Deteriorating | Schedule re-validation this week |
| 0-2 | 🔴 Critical | Immediate replacement needed |

### Example Score Calculation

```
Selector: //div[@aria-label="Like"]

Type stability: @aria-label → 8/10 (stable but can change with i18n)
Fallback: has fallback → 10/10
Validation history: last validated 2 weeks ago → 7/10 (not recent)
Wait timeout: 5000ms → 10/10

Weighted = (8 × 0.40) + (10 × 0.25) + (7 × 0.20) + (10 × 0.15)
        = 3.2 + 2.5 + 1.4 + 1.5
        = 8.6 ✅ Healthy
```

---

## 4. Detecting Facebook UI Changes

### Signs that Facebook has changed UI

1. **Selector health drops** — automated validation shows > 20% stale rate
2. **Fallback usage spikes** — `element-exists` fallback path ถูกใช้ > 30% ใน logs
3. **New CSS classes** — `contains(@class, "x...")` selectors ล้มเหลวบ่อย (Meta เปลี่ยน class name ทุก build)
4. **Timeout increase** — elements ใช้เวลา load นานกว่าปกติ (อาจมี A/B test layer)
5. **DOM structure shift** — target element อยู่ลึกขึ้น/ตื้นขึ้นใน DOM tree

### Automated Change Detection

```python
def detect_ui_change(previous_report, current_results):
    """Compare selector health between two validation runs"""
    changes = []
    
    for curr in current_results:
        prev = next(
            (p for p in previous_report if p['selector'] == curr['selector']),
            None
        )
        if prev:
            if prev['status'] == 'valid' and curr['status'] == 'stale':
                changes.append({
                    'selector': curr['selector'],
                    'change': 'VALID → STALE',
                    'severity': 'HIGH',
                    'action': 'Immediate replacement needed'
                })
            elif prev['status'] == 'stale' and curr['status'] == 'valid':
                changes.append({
                    'selector': curr['selector'],
                    'change': 'STALE → VALID (UI reverted?)',
                    'severity': 'INFO',
                    'action': 'Monitor — possible A/B test cycle'
                })
    
    if changes:
        print(f"⚠️ Detected {len(changes)} selector changes:")
        for c in changes:
            print(f"  [{c['severity']}] {c['change']} — {c['selector'][:60]}")
    else:
        print("✅ No selector changes detected")
    
    return changes
```

---

## 5. Fallback Pattern Documentation

### Standard Fallback Pairs

| Main Selector | Fallback Selector | Notes |
|--------------|-------------------|-------|
| `//a[@aria-label="Facebook"]` | `//a[contains(@href,"facebook.com")]` | Logo always has FB link |
| `//div[@aria-label="Create a post"]` | `//span[text()="Create a post"]` | Use text if aria missing |
| `//div[@aria-label="Like"][@aria-pressed="false"]` | `//div[contains(@aria-label,"Like")]` | Broader match as fallback |
| `//div[@aria-label="Post"]` | `//span[text()="Post"]` | Button text as fallback |
| `//div[@role="textbox" and @aria-label="Create a post"]` | `//div[@role="textbox"][1]` | Position-based last resort |
| `//div[starts-with(@aria-label, "Write a comment")]` | `//div[@role="textbox"]` | Any textbox as fallback |
| `//*[normalize-space(.)="Share"]` | `//*[contains(text(),"Share")]` | Partial match fallback |

### Fallback Documentation Format

```
Selector Pair #N: [Action Name]
──────────────────────────────────────────
Main:     //a[@aria-label="Home"]
Fallback: //a[@contains(@href, "/home")]
Platform: Desktop Facebook (all profiles)
Risk:     🟢 Low — aria-label stable
Last validated: 2026-06-15
Notes:    Fallback only needed if FB changes Home label
```

---

## 6. Selector Replacement Decision Tree

```
Selector ใช้ไม่ได้?
    │
    ├── selector type = class-based?
    │       ├── Yes → 🔴 HIGH priority — class เปลี่ยนบ่อย
    │       │         → Replace with @aria-label หรือ normalize-space(.)
    │       └── No → 🟡 MEDIUM priority
    │
    ├── fallback ใช้ได้?
    │       ├── Yes → ใช้ fallback ชั่วคราว + schedule refresh
    │       └── No → 🔴 HIGH priority — workflow will fail
    │
    ├── same element มีหลาย selectors?
    │       ├── Yes → merge หรือเลือกตัวที่ stable ที่สุด
    │       └── No → ออกแบบ selector ใหม่จาก DOM ปัจจุบัน
    │
    └── เป็น A/B test variation?
            ├── Yes → document ว่าเป็น variant + ใช้ method หลายทาง
            └── No → replace selector ปกติ
```

---

## 7. Validation Report Template

```
🔍 **Selector Validation Report**

### Workflow: [Name] v[Version]
- Validated: [Date]
- Profile used: [Profile ID]
- Browser: [Chrome/Firefox/Brave]

### 📊 Overall Health
| Metric | Value |
|--------|-------|
| Total Selectors | N |
| Valid | N (N%) |
| Stale | N (N%) |
| Untested | N |
| Avg Selector Health | N/10 |

### ❌ Stale Selectors (Need Replacement)
| Node | Selector | Staleness | Fallback Available | Priority |
|------|----------|-----------|-------------------|----------|
| [...] | [...] | [days] | Yes/No | P0/P1/P2 |

### 🟡 Warning Selectors (Deteriorating)
| Node | Selector | Health Score | Recommendation |
|------|----------|-------------|---------------|
| [...] | [...] | 5.2/10 | Refresh within 7 days |

### ✅ Healthy Selectors
| Category | Count | Notes |
|----------|-------|-------|
| Navigation | N | All stable |
| Actions | N | All stable |
| Interactions | N | All stable |

### 📋 Recommended Actions
1. Replace N stale selectors → assign ARKA 🔧
2. Re-test on 3 different profiles after change
3. Schedule next validation: [Date]

### 📎 Evidence
- [CDP validation results]
- [Screenshot of stale selectors]
```

---

## 8. Schedule & Maintenance

| Task | Frequency | Owner |
|------|-----------|-------|
| Full selector scan (all workflows) | Monthly | LUMI 📖 |
| High-risk selectors check | Weekly | LUMI 📖 |
| After Facebook major update | Immediate | LUMI 📖 |
| After workflow modification | Before deploy | ARKA 🔧 |
| New workflow review | Before first deploy | LUMI 📖 + GEMMY 💎 |
