---
name: workflow-analysis
description: วิเคราะห์ GemLogin workflows — อ่าน DB, trace node execution, identify bottlenecks, measure timing
metadata:
  type: skill
  category: gemlogin
  owner: lumi
---

# 📊 Workflow Analysis Guide

> วิเคราะห์ workflow GemLogin — จาก SQLite DB สู่ execution logs สู่ performance optimization
> อัปเดตล่าสุด: 2026-06-29

---

## 1. Preparation — Backup First

```bash
# ก่อนทำอะไร — backup db.db ทุกครั้ง
cp /path/to/gemlogin/data/db.db /path/to/backup/db-$(date +%Y%m%d-%H%M%S).db

# Export workflow เป็น .gemlogin (single-line JSON)
# ใช้ผ่าน gemlogin-mcp หรือ export จาก UI
```

---

## 2. Read DB Schema

### Basic Schema Inspection

```sql
-- List all workflows
SELECT id, name, version, description, created_at, updated_at FROM workflows;

-- List all profiles
SELECT id, name, platform, status, created_at FROM profiles;

-- Get all nodes for a workflow
SELECT n.id, n.label, n.data, n.position_x, n.position_y, n."order"
FROM nodes n
JOIN workflows w ON n.workflow_id = w.id
WHERE w.name = 'Workflow Name'
ORDER BY n."order";

-- Get all edges for a workflow
SELECT e.id, e.source_node_id, e.target_node_id, e.source_handle, e.target_handle, e.data
FROM edges e
JOIN workflows w ON e.workflow_id = w.id
WHERE w.name = 'Workflow Name';
```

### Advanced Schema Analysis

```sql
-- Count nodes by label type
SELECT n.label, COUNT(*) as count
FROM nodes n
JOIN workflows w ON n.workflow_id = w.id
WHERE w.name = 'Workflow Name'
GROUP BY n.label
ORDER BY count DESC;

-- Find orphaned nodes (no incoming edge)
SELECT n.id, n.label
FROM nodes n
JOIN workflows w ON n.workflow_id = w.id
LEFT JOIN edges e ON n.id = e.target_node_id
WHERE w.name = 'Workflow Name' AND e.id IS NULL AND n.label != 'trigger';

-- Find nodes without outgoing edges (not including end)
SELECT n.id, n.label
FROM nodes n
JOIN workflows w ON n.workflow_id = w.id
LEFT JOIN edges e ON n.id = e.source_node_id
WHERE w.name = 'Workflow Name' AND e.id IS NULL AND n.label != 'end';

-- Check condition completeness
SELECT n.id, n.data->>'groups' as conditions
FROM nodes n
JOIN workflows w ON n.workflow_id = w.id
WHERE w.name = 'Workflow Name' AND n.label = 'conditions';

-- Count edges per condition group
SELECT n.id, n.label, COUNT(e.id) as edge_count
FROM nodes n
JOIN workflows w ON n.workflow_id = w.id
LEFT JOIN edges e ON e.source_node_id = n.id
WHERE w.name = 'Workflow Name' AND n.label = 'conditions'
GROUP BY n.id;
```

---

## 3. Trace Node Execution

### Execution Log Analysis (From .gemlogin JSON)

```python
import json

def analyze_workflow(filepath):
    with open(filepath) as f:
        wf = json.load(f)
    
    nodes = wf.get('drawflow', {}).get('nodes', [])
    edges = wf.get('drawflow', {}).get('edges', [])
    
    print(f"=== Workflow: {wf.get('name', 'Unknown')} v{wf.get('version', '?')} ===")
    print(f"Nodes: {len(nodes)} | Edges: {len(edges)}")
    
    # Node distribution
    labels = {}
    for n in nodes:
        label = n.get('label', 'unknown')
        labels[label] = labels.get(label, 0) + 1
    
    print(f"\n--- Node Distribution ---")
    for label, count in sorted(labels.items(), key=lambda x: -x[1]):
        print(f"  {label}: {count}")
    
    # Edge connectivity
    node_ids = {n['id'] for n in nodes}
    edge_source_ids = {e['source'] for e in edges}
    edge_target_ids = {e['target'] for e in edges}
    
    unreachable = node_ids - edge_target_ids - {'trigger-node-id'}
    disconnected = node_ids - edge_source_ids - {'end-node-id'}
    
    if unreachable:
        print(f"\n⚠️ Potentially unreachable nodes: {unreachable}")
    if disconnected:
        print(f"\n⚠️ Nodes without outgoing edges: {disconnected}")
    
    # Loop structure
    loops = [n for n in nodes if n.get('label') in ('loop-data', 'loop-breakpoint', 'repeat-task')]
    print(f"\n--- Loop Structure ---")
    for lp in loops:
        if lp['label'] == 'loop-data':
            data = lp.get('data', {})
            print(f"  LOOP: {data.get('loopId', '?')} — {data.get('loopThrough', '?')} ({data.get('fromNumber', '?')} → {data.get('toNumber', '?')})")
        elif lp['label'] == 'loop-breakpoint':
            data = lp.get('data', {})
            print(f"  BREAK: {data.get('loopId', '?')}")
        elif lp['label'] == 'repeat-task':
            data = lp.get('data', {})
            print(f"  REPEAT: {data.get('repeatFor', '?')} times")
    
    # Selector coverage
    selectors = []
    for n in nodes:
        data = n.get('data', {})
        if 'selector' in data:
            selectors.append({'node': n['id'], 'label': n['label'], 'selector': data['selector']})
    
    print(f"\n--- Selectors ({len(selectors)} total) ---")
    for s in selectors:
        has_fallback = s['selector'].startswith('//')
        print(f"  [{s['label']}] {s['selector'][:80]}... {'✅' if has_fallback else '⚠️ no fallback?'}")

    return labels
```

### Execution Path Tracing

```
[trigger]
  → [open-url] → [tab-loaded] ✓
    → [element-exists (selector="#main")]
      ├── match → [event-click] → [delay] → [press-key]
      └── fallback → [reload-tab] → [tab-loaded] → [loop-breakpoint (loopId: retry)]
  → [loop-breakpoint (loopId: mainloop)]
    ├── continue → [loop-data] (next iteration)
    └── break → [end]
```

**Key things to trace:**
1. Trigger → first action — มี edge ถึงไหม?
2. ทุก `element-exists` มีทั้ง match + fallback edge หรือไม่?
3. Loop `loop-breakpoint` — edge ที่กลับไป loop ไป node ไหน?
4. `conditions` — edge ไปครบทุก group หรือมี group ที่ไม่มี edge?
5. `end` — reachable จากทุก terminal path?

---

## 4. Performance Analysis

### Timing Measurement

```sql
-- Node execution timing from execution_logs
SELECT n.label, AVG(e.execution_time_ms) as avg_time,
       MAX(e.execution_time_ms) as max_time,
       COUNT(*) as run_count
FROM execution_logs e
JOIN nodes n ON e.node_id = n.id
JOIN workflows w ON n.workflow_id = w.id
WHERE w.name = 'Workflow Name'
GROUP BY n.label
ORDER BY avg_time DESC;
```

### Bottleneck Detection Matrix

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Node execution time | < 500ms | 500-2000ms | > 2000ms |
| Loop iteration time | < 5s | 5-15s | > 15s |
| Selector timeout rate | < 1% | 1-5% | > 5% |
| Error rate (nextBlockId=null) | 0% | < 1% | > 1% |
| Total workflow runtime | < 60s | 60-300s | > 300s |
| Fallback usage rate | < 10% | 10-30% | > 30% |

### Common Bottlenecks

1. **Excessive delays** — delay > 10s ที่ไม่จำเป็น → reduce to 3-7s random
2. **Stale selectors** — fallback ถูกใช้ > 30% → update main selector
3. **Deep loop nesting** — nested loops > 2 levels → flatten or split workflow
4. **Large media upload** — upload > 30s → pre-compress images
5. **Redundant navigation** — navigate page ทุก iteration → cache URL or minimize
6. **High condition count** — > 10 groups → split into sub-workflows
7. **Missing waitForSelector** — click element without waiting → add waitForSelector

---

## 5. Complexity Scoring

Score butละ workflow จาก 1-10:

| Factor | Score 1-3 (Simple) | Score 4-6 (Moderate) | Score 7-10 (Complex) |
|--------|-------------------|---------------------|---------------------|
| Node count | < 20 | 20-80 | > 80 |
| Loop depth | 0 | 1-2 levels | > 2 levels |
| Condition groups | 0-2 | 3-6 | > 6 |
| Selector count | < 5 | 5-15 | > 15 |
| JS blocks | 0 | 1-3 | > 3 |
| File I/O | 0 | 1-3 | > 3 |

**Total complexity** = average of all factors

**Maintainability assessment:**
- 1-3: Easy to maintain — clear flow, low touch
- 4-6: Moderate — need documentation, periodic review
- 7-10: High maintenance — recommend refactoring, breaking into smaller workflows

---

## 6. Anti-Pattern Detection

### Automatic Anti-Pattern Scan

```python
def detect_anti_patterns(filepath):
    with open(filepath) as f:
        wf = json.load(f)
    
    nodes = wf.get('drawflow', {}).get('nodes', [])
    edges = wf.get('drawflow', {}).get('edges', [])
    issues = []
    
    for n in nodes:
        data = n.get('data', {})
        label = n.get('label', '')
        nid = n.get('id', '?')
        
        # Anti-pattern 1: IIFE wrapper
        if label == 'javascript-code':
            code = data.get('code', '')
            if '(() =>' in code or '(function()' in code:
                issues.append(f"❌ [{nid}] IIFE wrapper in javascript-code")
            if 'async' in code and 'function' in code:
                issues.append(f"⚠️ [{nid}] Async function wrapper in javascript-code")
        
        # Anti-pattern 2: Wrong delay format
        if label == 'delay':
            time_val = str(data.get('time', ''))
            if 'random(' in time_val:
                issues.append(f"❌ [{nid}] Wrong delay format: {time_val} — use 'N,M'")
        
        # Anti-pattern 3: Missing fallback for element-exists
        if label == 'element-exists':
            outgoing = [e for e in edges if e['source'] == nid]
            if len(outgoing) < 2:
                issues.append(f"⚠️ [{nid}] element-exists has {len(outgoing)} edges (need 2: match + fallback)")
        
        # Anti-pattern 4: Conditions missing groups
        if label == 'conditions':
            groups = data.get('groups', [])
            if len(groups) == 0:
                issues.append(f"❌ [{nid}] Conditions has no groups")
            
            # Check condition handle naming
            for e in [e for e in edges if e['source'] == nid]:
                handle = e.get('sourceHandle', '')
                if 'output-cond-' in handle:
                    issues.append(f"❌ [{nid}] Wrong condition handle format: {handle} — use output-{groupId}")
        
        # Anti-pattern 5: element-scroll missing fields
        if label == 'element-scroll':
            if len(data) < 17:
                issues.append(f"⚠️ [{nid}] element-scroll has {len(data)} fields (need ~18)")
        
        # Anti-pattern 6: Missing waitForSelector on event-click
        if label == 'event-click':
            if not data.get('waitForSelector', False):
                issues.append(f"⚠️ [{nid}] event-click without waitForSelector")
        
        # Anti-pattern 7: Loop ID mismatch
        if label == 'loop-breakpoint':
            loop_id = data.get('loopId', '')
            matching_loop = [x for x in nodes if x.get('label') == 'loop-data' and x.get('data', {}).get('loopId') == loop_id]
            if not matching_loop:
                issues.append(f"❌ [{nid}] loop-breakpoint '{loop_id}' has no matching loop-data")
    
    return issues
```

### Top Anti-Patterns ที่พบบ่อย

| # | Anti-Pattern | Severity | Detection |
|---|-------------|----------|-----------|
| 1 | IIFE wrapper in JS | 🔴 Critical | Static analysis |
| 2 | `random(N,M)` in delay | 🔴 Critical | Static analysis |
| 3 | Missing fallback on element-exists | 🟡 High | Edge count |
| 4 | `output-cond-` in sourceHandle | 🔴 Critical | Edge inspect |
| 5 | element-scroll incomplete fields | 🟡 High | Field count |
| 6 | Missing waitForSelector | 🟡 Medium | Data inspect |
| 7 | Loop ID mismatch | 🔴 Critical | Cross-reference |
| 8 | Empty condition groups | 🟡 Medium | Data inspect |
| 9 | No end node | 🔴 Critical | Node list |
| 10 | Disconnected nodes | 🟡 Medium | Edge tracing |

---

## 7. Analysis Report Template

```
📖 **LUMI Analysis Report**

### Workflow: [Name] v[Version]
- Analyzed: [Date]
- Source: [File path / DB export]

### 📊 Quick Stats
| Metric | Value |
|--------|-------|
| Nodes | N |
| Edges | N |
| Loops | N |
| Condition Groups | N |
| Selectors | N (N with fallback) |
| Complexity Score | N/10 |
| Est. Runtime | N seconds |

### 🔍 Key Findings
1. **[Issue/Pattern Name]**
   - What: [...]
   - Evidence: [...]
   - Impact: [high/medium/low]
   - Recommendation: [...]

### ⚡ Performance
- Total estimated runtime: Ns
- Top 3 bottlenecks:
  1. [...] (Ns)
  2. [...] (Ns)
  3. [...] (Ns)

### ✅ What's Working
- [Pattern/design ที่ดี]
- [Selector ที่ stable]
- [Loop structure ที่ clean]

### ❌ Anti-Patterns Found
- [Anti-pattern list with severity]

### 📋 Recommended Actions
| Priority | Action | Assignee | Status |
|----------|--------|----------|--------|
| P0 | [...] | ARKA 🔧 | Awaiting GEMMY approval |
| P1 | [...] | LUMI 📖 (validate) | — |
| P2 | [...] | — | — |

### 📎 Evidence
- [Execution log snippet]
- [Timing data]
- [Screenshot references]
```
