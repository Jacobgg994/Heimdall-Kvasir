# GemLogin Workflow Builder

สร้างไฟล์ `.gemlogin` สำหรับ import เข้า GemLogin โดยตรง

## กฎสำคัญ (ต้องอ่านก่อนสร้าง)

1. **COPY REAL EXPORT FORMAT** — ใช้ `Cookie login.gemlogin` เป็น template ห้ามสร้างจากศูนย์
2. **ไฟล์ต้องเป็น SINGLE LINE JSON** — ไม่มี indent, ไม่มี wrapper object
3. **ไม่มี `id` ที่ top level** — GemLogin จะ generate id เองตอน import
4. **Trigger params ต้องมี `data: true` และ `id`** — ทุก parameter ต้องมี 2 ฟิลด์นี้
5. **Edges ต้องมี `type: "bezier"`, `markerEnd: "arrowclosed"`** — ห้ามขาด
6. **Fallback edges ต้องมี `style: "stroke: #ff6b6b"`**
7. **Condition sourceHandle**: `{nodeId}-output-{conditionId}` — ไม่ใช่ `output-cond-`
8. **Top-level keys**: `extVersion`, `name`, `icon`, `version`, `table`, `description`, `isProtected`, `includedWorkflows`, `author`, `globalData`, `settings`, `trigger`, `drawflow`
9. **Trigger node data** ต้องมี `observeElement`, `preferParamsInTab`, `interval`, `delay`, `date`, `time` ฯลฯ
10. **drawflow keys**: `nodes`, `edges`, `position`, `zoom`, `viewport`

## Template Structure

```python
wf = {
    "extVersion": 2,
    "name": "WORKFLOW NAME",
    "icon": "riGlobalLine",
    "version": "1.0.0",
    "table": [],
    "description": "",
    "isProtected": False,
    "includedWorkflows": {},
    "author": "ARKA",
    "globalData": {},
    "settings": {COPY_FROM_REAL_WORKFLOW},
    "trigger": {
        "icon": "riPlayLine", "disableBlock": False, "description": "",
        "type": "manual", "interval": 0, "delay": 0,
        "date": "", "time": "", "url": "", "shortcut": "",
        "activeInInput": True, "isUrlRegex": False,
        "days": [], "contextMenuName": "", "contextTypes": [],
        "preferParamsInTab": True,
        "observeElement": {COPY_FROM_REAL},
        "parameters": [
            {"name": "param1", "label": "Label", "type": "filepath", "defaultValue": "", "placeholder": "", "data": True, "id": "x1"}
        ]
    },
    "drawflow": {
        "nodes": [...],
        "edges": [...],
        "position": [0, 0],
        "zoom": 0.65,
        "viewport": {"x": 0, "y": 0, "zoom": 0.65}
    }
}
```

## Node Templates

### Trigger Node
```python
{
    "id": "trig", "type": "BlockBasic", "label": "trigger", "initialized": False,
    "position": {"x": 100, "y": 150},
    "data": {
        "icon": "riPlayLine", "disableBlock": False, "description": "",
        "type": "manual", "interval": 0, "delay": 0,
        "date": "", "time": "", "url": "", "shortcut": "",
        "activeInInput": True, "isUrlRegex": False,
        "days": [], "contextMenuName": "", "contextTypes": [],
        "parameters": [...SAME_AS_TRIGGER_PARAMS...],
        "preferParamsInTab": True,
        "observeElement": {...}
    }
}
```

### Event Click Node
```python
{
    "id": "...", "type": "BlockBasicWithFallback", "label": "event-click", "initialized": False,
    "position": {"x": 0, "y": 0},
    "data": {
        "icon": "riCursorLine", "disableBlock": False, "description": "...",
        "x": "", "y": "", "findBy": "xpath",
        "waitForSelector": True, "waitSelectorTimeout": 15000,
        "selector": "//xpath", "markEl": False, "multiple": False,
        "selectOption": "leftClick", "delay": 2000, "humanClick": True
    }
}
```

### Upload File Node
```python
{
    "id": "...", "type": "BlockBasicWithFallback", "label": "upload-file", "initialized": False,
    "position": {"x": 0, "y": 0},
    "data": {
        "icon": "riUploadCloudLine", "disableBlock": False, "description": "...",
        "filePath": "{{variables.filename}}", "findBy": "xpath",
        "selector": "//div[@role='dialog']//input[@type='file']",
        "delay": 3000
    }
}
```

### Open URL Node
```python
{
    "id": "...", "type": "BlockBasicWithFallback", "label": "open-url", "initialized": False,
    "position": {"x": 0, "y": 0},
    "data": {
        "icon": "riLink", "disableBlock": False,
        "url": "https://...", "userAgent": "",
        "description": "...", "waitTabLoaded": True,
        "customUserAgent": False, "newTab": False, "active": True, "delay": 2000
    }
}
```

### JavaScript Code Node
```python
{
    "id": "...", "type": "BlockBasicWithFallback", "label": "javascript-code", "initialized": False,
    "position": {"x": 0, "y": 0},
    "data": {
        "icon": "riCodeSSlashLine", "disableBlock": False, "description": "...",
        "timeout": "10000", "context": "website",
        "code": "...JS CODE...",
        "preloadScripts": [], "everyNewTab": False, "runBeforeLoad": False, "delay": 0
    }
}
```

### Delay Node
```python
{
    "id": "...", "type": "BlockDelay", "label": "delay", "initialized": False,
    "position": {"x": 0, "y": 0},
    "data": {"icon": "riTimerLine", "delay": 4000, "description": "..."}
}
```

### End Node
```python
{
    "id": "end", "type": "BlockBasic", "label": "end", "initialized": False,
    "position": {"x": 0, "y": 0},
    "data": {"icon": "riFlagLine"}
}
```

### Note Node
```python
{
    "id": "...", "type": "BlockNote", "label": "note", "initialized": False,
    "position": {"x": 0, "y": 0},
    "data": {"icon": "riFileEditLine", "note": "...", "drawing": False,
             "width": 350, "height": 60, "color": "blue", "fontSize": "large"}
}
```

## Edge Template

```python
def mkedge(src, tgt, src_h=None, tgt_h=None, label="", style=None):
    sh = src_h or f"{src}-output-1"
    th = tgt_h or f"{tgt}-input-1"
    return {
        "id": f"vueflow__edge-{src}{sh}-{tgt}{th}",
        "type": "bezier",
        "source": src, "target": tgt,
        "sourceHandle": sh, "targetHandle": th,
        "updatable": True, "selectable": True, "data": {},
        "label": label, "markerEnd": "arrowclosed",
        "sourceX": 0, "sourceY": 0, "targetX": 0, "targetY": 0,
        **({"style": style} if style else {})
    }
```

## Layout Rules

- Notes: y=10
- Trigger + Main flow: y=150
- Profile pic actions: y=380
- Cover actions: y=580
- Fallback: y=780
- x spacing: ~350px between sequential nodes
- zoom: 0.65

## Save Format

```python
with open('output.gemlogin', 'w', encoding='utf-8') as f:
    json.dump(wf, f, ensure_ascii=False)  # NO INDENT = single line!
```

## Reference File

ตัวอย่างของจริง: `C:\Users\Admin\Downloads\Cookie login.gemlogin`

## Team

- ARKA 🔧: Workflow Creator (ใต้ GEMMY 💎)
- GEMMY 💎: Automation Lead

## Related Skills

- `gemlogin`: connect GemLogin MCP
- `gemlogin-facebook`: Facebook automation patterns
- `gemlogin-edit`: DB-first workflow editing
