---
name: gemlogin-debugging
description: วิธีแก้ปัญหา Workflow GemLogin ที่พัง — error messages, สาเหตุ, วิธีแก้
metadata:
  type: skill
  category: gemlogin
  owner: gemmy
---

# 🔧 GemLogin Debugging Guide

## Error Patterns & Solutions

| Error | สาเหตุ | วิธีแก้ |
|-------|--------|---------|
| `Cannot read properties of undefined (reading 'insert')` | IIFE wrapper ใน javascript-code | ลบ `(()=>{})()` — ใช้ top-level |
| `Cannot read properties of undefined (reading 'list')` | conditions schema ไม่ใช่ triplet | ตรวจสอบ items: ต้องเป็น `[{...},{...},{...}]` |
| `nextBlockId = null` | edges sourceHandle ไม่ตรงกับ condition id | เช็ค sourceHandle = `node-id-output-cond-[id]` |
| Workflow ไม่เริ่มทำงาน | ไม่มี trigger object | เพิ่ม `trigger: { type: "manual", parameters: [...] }` |
| Node ไม่แสดงใน editor | label ว่างเปล่า | ใส่ label ให้ทุก node |
| Click ไม่ทำงาน | selector หาไม่เจอ | ใช้ `waitForSelector: true`, เพิ่ม `waitSelectorTimeout` |
| Loop วิ่งไม่หยุด | loop-breakpoint edge กลับไปผิดที่ | edge ต้องไปที่ node ถัดไป — ไม่ใช่ไป loop-data |
| `SetVariable` ไม่ทำงาน | เรียกใน async IIFE | เรียกที่ top-level หลัง await |
| เปิดหน้าไม่ขึ้น | url ว่างหรือ format ผิด | เช็ค url — ใช้ `https://` เต็มรูปแบบ |
| delay ไม่ random | ใช้ `random(3,7)` | ใช้ `"3,7"` แทน |

---

## Validation Script

```python
import json

def validate_workflow(filepath):
    with open(filepath) as f:
        wf = json.load(f)
    
    errors = []
    nodes = wf.get('drawflow', {}).get('nodes', [])
    edges = wf.get('drawflow', {}).get('edges', [])
    trigger = wf.get('trigger', {})
    
    # 1. Check trigger
    if trigger.get('type') != 'manual':
        errors.append("❌ trigger.type != 'manual'")
    if not trigger.get('parameters'):
        errors.append("❌ trigger ไม่มี parameters")
    
    # 2. Check nodes
    node_ids = set()
    for n in nodes:
        nid = n.get('id', '?')
        node_ids.add(nid)
        
        if not n.get('label'):
            errors.append(f"❌ Node {nid}: label ว่าง")
        
        if n.get('label') == 'delay':
            time_val = n.get('data', {}).get('time', '')
            if 'random(' in str(time_val):
                errors.append(f"❌ Node {nid}: ใช้ random() ใน delay: {time_val}")
        
        if n.get('label') == 'javascript-code':
            code = n.get('data', {}).get('code', '')
            if '(() =>' in code or '(function()' in code:
                errors.append(f"❌ Node {nid}: มี IIFE wrapper")
        
        if n.get('label') == 'element-scroll':
            ndata = n.get('data', {})
            if len(ndata) < 18:
                errors.append(f"❌ Node {nid}: element-scroll มีแค่ {len(ndata)} fields (ต้อง 18)")
    
    # 3. Check edges
    for e in edges:
        src = e.get('source')
        tgt = e.get('target')
        if src not in node_ids:
            errors.append(f"❌ Edge {e.get('id','?')}: source '{src}' ไม่มีอยู่จริง")
        if tgt not in node_ids:
            errors.append(f"❌ Edge {e.get('id','?')}: target '{tgt}' ไม่มีอยู่จริง")
    
    # 4. Check has end node
    has_end = any(n.get('label') == 'end' for n in nodes)
    if not has_end:
        errors.append("❌ ไม่มี end node")
    
    if errors:
        print(f"❌ {filepath} — {len(errors)} errors:")
        for e in errors:
            print(f"  {e}")
        return False
    else:
        print(f"✅ {filepath} — {len(nodes)} nodes, {len(edges)} edges — OK")
        return True
```

---

## Quick Checklist ก่อน Deploy

```
ก่อน deploy workflow:
□ 1.  validate ด้วย Python script ข้างบน
□ 2.  ทดสอบบน 1 profile ก่อน (ไม่ใช่ multiple)
□ 3.  เช็ค log ว่าไม่มี nextBlockId = null
□ 4.  ทดสอบครบทุก branch (conditions match + fallback)
□ 5.  ทดสอบ loop — วิ่งครบตามจำนวนที่ตั้ง
□ 6.  ทดสอบ edge case — url ว่าง, ตัวแปรไม่ครบ
□ 7.  delay ทำงานจริง — timing สมเหตุสมผล
□ 8.  ไม่มี IIFE ใน javascript-code
□ 9.  trigger params ตรงกับตัวแปรที่ใช้ใน workflow
□ 10. file-action เขียนไฟล์ถูก path
```
