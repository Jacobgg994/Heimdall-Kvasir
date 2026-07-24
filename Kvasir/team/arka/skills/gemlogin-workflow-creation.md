---
name: gemlogin-workflow-creation
description: สร้าง GemLogin workflows จาก scratch — ใช้ real export format, single-line JSON, edge format ถูกต้อง
metadata:
  type: skill
  category: gemlogin
  owner: arka
---

# 🔧 GemLogin Workflow Creation Guide

> สร้าง workflow automation สำหรับ GemLogin Browser — ตั้งแต่ trigger จนถึง end node
> อัปเดตล่าสุด: 2026-06-29

---

## 1. Workflow Structure (Real Export Format)

GemLogin export เป็น single-line JSON มี structure ดังนี้:

```json
{"id":"","name":"Workflow Name","version":"1.0","description":"","trigger":{"type":"manual","parameters":[...]},"drawflow":{"nodes":[...],"edges":[...]},"data":{}}
```

**กฎ:**
- ต้องเป็น single-line JSON — ไม่มี line break (GemLogin editor รองรับเฉพาะ single-line)
- ไม่มี `id` ที่ root — export จะไม่ include `id` (ให้ GemLogin generate เอง)
- `trigger.parameters` ต้องตรงกับตัวแปรที่ใช้ใน workflow
- ทุก node ต้องมี `label` ที่ GemLogin รองรับ

---

## 2. Trigger Setup

```json
{
  "type": "manual",
  "parameters": [
    {
      "id": "random-uuid",
      "name": "profileFolderPath",
      "label": "Profile Folder",
      "type": "filepath",
      "description": "Path to profile folder",
      "defaultValue": "C:\\Users\\Admin\\Downloads\\profiles",
      "placeholder": "Enter profile path",
      "data": { "required": true, "masks": false, "useMask": false, "unmaskValue": "" }
    },
    {
      "id": "random-uuid",
      "name": "enableLike",
      "label": "Enable Like",
      "type": "checkbox",
      "description": "Like posts",
      "defaultValue": true,
      "data": { "required": false, "masks": false, "useMask": false, "unmaskValue": "" }
    }
  ]
}
```

**Parameter types ที่รองรับ:**
| type | ใช้เมื่อ | example |
|------|---------|---------|
| `divider` | แบ่ง section | `{"type": "divider", "label": "Section Name"}` |
| `label` | ข้อความอธิบาย | `{"type": "label", "label": "Instructions here"}` |
| `checkbox` | boolean option | `{"defaultValue": true/false}` |
| `string` | text input | `{"defaultValue": "", "placeholder": "..."}` |
| `filepath` | path ไฟล์ | `{"defaultValue": "C:\\path\\to\\file"}` |
| `number` | จำนวน | `{"defaultValue": 5}` |
| `inline` | spacing | `{"type": "inline"}` |

---

## 3. Node Types & Structure

### Common Node Fields
```json
{
  "id": "node-uuid",
  "label": "event-click",
  "data": { ... },
  "position": { "x": 100, "y": 200 },
  "className": "",
  "input": 1,
  "output": 1
}
```

### Node Label Reference

| label | data fields สําคัญ | output |
|-------|-------------------|--------|
| `trigger` | `parameters: [...]` | 1 |
| `open-url` | `url: string` | 1 |
| `tab-loaded` | `url: string` | 1 |
| `event-click` | `selector: string`, `waitForSelector: true/false`, `waitSelectorTimeout: number` | 1 |
| `element-exists` | `selector: string` | 2 (exists/not) |
| `element-scroll` | 18 fields — position, smooth, timeout, wait-for-element, etc. | 1 |
| `delay` | `time: "3,7"` | 1 |
| `press-key` | `mode: "insert"`, `key: string`, `selector: string` | 1 |
| `javascript-code` | `code: string` (top-level statements, **ไม่ IIFE**) | 1 |
| `loop-data` | `loopId: string`, `loopThrough: "numbers"/"data"`, `fromNumber`, `toNumber` | 1 |
| `loop-breakpoint` | `loopId: string` | 2 (continue/break) |
| `repeat-task` | `repeatFor: number` or `"{{variables.count}}"` | 1 |
| `increase-variable` | `name: string`, `value: number` | 1 |
| `insert-data` | `tableName: string`, `columns: [...]`, `values: [...]` | 1 |
| `read-file-text` | `path: string`, `encoding: "utf8"/"ascii"`, `readMode: "aline"/"all"/"number"` | 1 |
| `split-data` | `delimiter: string`, `variable: string` | 1 |
| `get-file-path` | `path: string`, `filter: string` | 1 |
| `commandPro` | `command: string`, `decode: "utf8"` | 1 |
| `clipboard` | `action: "copy"/"paste"` | 1 |
| `file-action` | `action: "write"/"append"/"delete"`, `filePath: string`, `content: string`, `writeMode: "create"/"append"`, `appendMode: "newLine"/"sameLine"` | 1 |
| `reload-tab` | — | 1 |
| `hover-element` | `selector: string` | 1 |
| `forms` | `selector: string`, `values: string` | 1 |
| `upload-file` | `selector: string`, `filePath: string` | 1 |
| `mouse-move` | `x: number`, `y: number`, `selector: string` | 1 |
| `random` | `type: "number"/"fraction"`, `fromValue: number`, `toValue: number` | 1 |
| `conditions` | `groups: [...]` | N+1 (N groups + fallback) |
| `end` | — | 0 |
| `set-variable` | `name: string`, `value: string` | 1 |
| `delete-data` | `name: string` | 1 |
| `tab-url` | — | 1 |

---

## 4. Edge Format

```json
{
  "id": "vueflow__edge-{sourceId}-output-{n}-{targetId}-input-1",
  "type": "bezier",
  "source": "{sourceNodeId}",
  "target": "{targetNodeId}",
  "sourceHandle": "{sourceNodeId}-output-{n}",
  "targetHandle": "{targetNodeId}-input-1",
  "updatable": true,
  "selectable": true,
  "data": {},
  "label": "",
  "markerEnd": { "type": "arrowclosed", "width": 20, "height": 20, "color": "#b1b1b7" }
}
```

**กฎ Edge:**
- `type` ต้องเป็น `"bezier"` เสมอ
- `markerEnd` ต้องมี `{ "type": "arrowclosed", "width": 20, "height": 20, "color": "#b1b1b7" }`
- แหล่งที่มาของ `sourceHandle`: ถ้าเป็น node ปกติ ใช้ `{nodeId}-output-1`
- ถ้าเป็น `element-exists` หรือ `conditions`: output แรก = exists/match, output ที่สอง = fallback
- **Condition handles**: `{nodeId}-output-{conditionGroupId}` — ห้ามใช้ `output-cond-{id}`

---

## 5. Conditions Schema

```json
{
  "id": "condition-node-id",
  "label": "conditions",
  "data": {
    "groups": [
      {
        "id": "likeEnabled",
        "name": "Like enabled?",
        "conditions": [
          ["{{variables.enableLike}}", "eq", "true"],
          ["{{variables.pageId}}", "ne", ""]
        ]
      },
      {
        "id": "commentEnabled",
        "name": "Comment enabled?",
        "conditions": [
          ["{{variables.enableComment}}", "eq", "true"]
        ]
      }
    ]
  },
  "position": { "x": 500, "y": 200 },
  "className": "",
  "input": 1,
  "output": 2
}
```

**กฎ Conditions:**
- ใช้ triplet schema: `[left, op, right]`
- operators: `eq`, `ne`, `gt`, `lt`, `gte`, `lte`, `contains`, `not contains`, `regex`
- แต่ละ group มี `id` ที่ไม่ซ้ำ
- sourceHandle edge: `{nodeId}-output-{groupId}` ไม่ใช่ `{nodeId}-output-cond-{groupId}`
- output สุดท้าย = fallback (ไม่มีใน groups)

---

## 6. Loop Design

### Pattern: loop-data → ... → loop-breakpoint

```json
// loop-data node
{
  "id": "main-loop-data",
  "label": "loop-data",
  "data": {
    "loopId": "mainloop",
    "loopThrough": "numbers",
    "fromNumber": 1,
    "toNumber": 10
  }
}

// loop-breakpoint node (ใช้ loopId เดียวกัน)
{
  "id": "main-loop-break",
  "label": "loop-breakpoint",
  "data": {
    "loopId": "mainloop"
  }
}
```

**กฎ Loop:**
- `loopId` ต้องตรงกันระหว่าง `loop-data` และ `loop-breakpoint`
- `loop-through: "numbers"` = วนตามช่วง
- `loop-through: "data"` = วนตาม array ใน `loopData`
- loop-breakpoint edge ที่ return ไป loop: วิ่งจาก loop-breakpoint ไปยัง node ถัดไป (ไม่ใช่ไป loop-data)
- สุดท้ายของ loop: edge วิ่งออกจาก loop-breakpoint ไปยัง node หลัง loop

---

## 7. JavaScript Block Rules

```javascript
// ✅ ถูกต้อง — top-level statements
let result = [];
const elements = document.querySelectorAll('.selector');
elements.forEach(el => result.push(el.textContent));
return JSON.stringify(result);

// ❌ ผิด — IIFE wrapper
(() => {
  let result = [];
  // ...
})();

// ❌ ผิด — async function wrapper
async function run() {
  // ...
}
```

**กฎ JS Blocks:**
- ห้าม IIFE wrapper `(()=>{...})()`
- ห้าม `async function` wrapper
- `await` ใช้ได้ใน top-level
- `SetVariable` เรียกที่ top-level หลัง await
- return ค่าผ่าน top-level statement

---

## 8. Delay Format

```json
// Random delay (seconds.minutes)
{ "label": "delay", "data": { "time": "3,7" } }

// Fixed delay
{ "label": "delay", "data": { "time": "5" } }
```

**กฎ Delay:**
- Random: ใช้ `"N,M"` — ห้าม `"random(N,M)"` หรือ `"random(N, M)"`
- ค่าเป็นวินาที — `"3,7"` = ระหว่าง 3 ถึง 7 วินาที
- Fixed: ใช้ตัวเลขตรง

---

## 9. BlockBasicWithFallback — Complete Example

```json
{
  "id": "click-like-btn",
  "label": "event-click",
  "data": {
    "selector": "//div[@aria-label='Like']",
    "waitForSelector": true,
    "waitSelectorTimeout": 5000,
    "clickType": "clickOnce",
    "mouseClickType": "leftClick",
    "x": 0,
    "y": 0,
    "moveMouse": false,
    "clickPosition": "elementCenter",
    "clickCount": 1,
    "delayBeforeClick": 0,
    "delayAfterClick": 0,
    "delayBeforeMouseMove": 0,
    "clickDelay": 0,
    "scrollToElement": false,
    "scrollPosition": "middle",
    "displayScrollAnimation": false,
    "scrollAnimationDirection": "default",
    "saveElement": false,
    "script": ""
  },
  "position": { "x": 300, "y": 200 },
  "className": "",
  "input": 1,
  "output": 1
}
```

---

## 10. Workflow Template — Quick Start

```json
{"name":"My Workflow","version":"1.0","description":"","trigger":{"type":"manual","parameters":[{"id":"trigger-param-1","name":"actionCount","label":"Number of actions","type":"number","description":"","defaultValue":5,"placeholder":"","data":{"required":true,"masks":false,"useMask":false,"unmaskValue":""}}]},"drawflow":{"nodes":[{"id":"trigger-node","label":"trigger","data":{},"position":{"x":0,"y":200},"className":"","input":1,"output":1},{"id":"end-node","label":"end","data":{},"position":{"x":800,"y":200},"className":"","input":1,"output":0}],"edges":[{"id":"vueflow__edge-trigger-node-output-1-end-node-input-1","type":"bezier","source":"trigger-node","target":"end-node","sourceHandle":"trigger-node-output-1","targetHandle":"end-node-input-1","updatable":true,"selectable":true,"data":{},"label":"","markerEnd":{"type":"arrowclosed","width":20,"height":20,"color":"#b1b1b7"}}]},"data":{}}
```

---

## 11. Validation Checklist

ก่อนส่ง workflow ให้ GEMMY review:

- [ ] Single-line JSON (ไม่มี line break)
- [ ] `id` ไม่มีที่ root level
- [ ] มี trigger node (type: manual, มี parameters)
- [ ] มี end node
- [ ] ทุก node มี label ที่ GemLogin รองรับ
- [ ] ทุก condition group มี `id` ไม่ซ้ำ
- [ ] condition sourceHandle ใช้ `output-{id}` ไม่ใช่ `output-cond-{id}`
- [ ] edge type = `bezier`
- [ ] edge markerEnd = `arrowclosed`
- [ ] delay format `"N,M"` — ไม่ `random()`
- [ ] javascript-code ไม่มี IIFE wrapper
- [ ] loop-data + loop-breakpoint ใช้ loopId ตรงกัน
- [ ] ทดสอบบน 1 real GemLogin profile (log ไม่มี `nextBlockId = null`)
- [ ] ทุก XPath มี fallback selector
- [ ] main path กับ fallback path แยกทาง visually
- [ ] trigger parameters ตรงกับ variables ใน workflow
