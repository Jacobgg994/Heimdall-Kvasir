---
name: gemlogin-block-reference
description: รายละเอียดทุก Block Type ใน GemLogin — ชื่อ, fields, schema, ข้อควรระวัง
metadata:
  type: skill
  category: gemlogin
  owner: gemmy
---

# 📐 GemLogin Block Reference — ฉบับสมบูรณ์ (Real Schema จาก 801)

> อัปเดตล่าสุด: 2026-06-29 — จากการถอดสคริปต์จริง 8 ไฟล์ใน 801
> แหล่งที่มา: `/mnt/d/skills/WorkflowGemlogin/801/`

## ⚠️ กฎเหล็กก่อนสร้าง

1. **label อยู่ที่ top-level `n['label']`** — ไม่ใช่ `n['data']['label']` (data.label ว่างเสมอ)
2. **ทุก block ต้องใส่ field ครบตาม label** — แต่ละ label มีชุด fields ต่างกัน
3. **delay ใช้ `"N,M"`** — ไม่ใช่ `"random(N,M)"`
4. **javascript-code ห้าม IIFE** — `(()=>{})()` พังทันที
5. **conditions ใช้ nested schema** — 3-level: group → subgroup → items (triplet)
6. **edges sourceHandle** — ใช้ `node-id-output-<group_id>` สำหรับ conditions match
7. **trigger ต้องมี type: "manual" + parameters**
8. **BlockBasicWithFallback = label กำหนด field set** — แต่ละ label มีชุด data fields เฉพาะ
9. **ไม่มี BlockNote ใน real scripts** — ไม่ต้องสร้าง
10. **node `settings` field** = `{"blockTimeout": "50000"}` สำหรับปรับ timeout เฉพาะ node

---

## Top-Level Node Structure

```json
{
  "id": "unique-node-id",
  "type": "BlockBasicWithFallback",
  "label": "event-click",           // ← label อยู่ที่นี้!
  "position": {"x": 0, "y": 0},
  "data": {
    // fields ตาม label
    "description": "",
    "disableBlock": false,
    "icon": "riCursorLine",
    ...
  }
}
```

---

## Workflow-Level Settings (เหมือนกันทุกไฟล์จริง)

```json
{
  "settings": {
    "publicId": "",
    "blockDelay": 0,
    "saveLog": true,
    "debugMode": false,
    "restartTimes": 3,
    "notification": true,
    "execContext": "popup",
    "reuseLastState": false,
    "inputAutocomplete": true,
    "onError": "stop-workflow",
    "executedBlockOnWeb": false
  }
}
```

---

## Trigger Node (BlockBasic)

```json
{
  "type": "BlockBasic",
  "label": "trigger",
  "data": {
    "icon": "riPlayLine",
    "disableBlock": false,
    "type": "manual",
    "delay": 5,
    "interval": 60,
    "time": "00:00",
    "date": "",
    "days": [],
    "isUrlRegex": false,
    "url": "",
    "shortcut": "",
    "contextMenuName": "",
    "contextTypes": [],
    "activeInInput": false,
    "preferParamsInTab": false,
    "observeElement": {
      "selector": "",
      "baseSelector": "",
      "matchPattern": "",
      "targetOptions": {},
      "baseElOptions": {}
    },
    "parameters": [
      {
        "id": "unique-id",
        "name": "param_name",
        "label": "แสดงผลใน UI",
        "type": "checkbox|string|filepath|number|divider|label|inline",
        "description": "คำอธิบาย",
        "defaultValue": true or "",
        "placeholder": "Hint text",
        "data": {
          "required": true
        }
      }
    ]
  }
}
```

### Trigger Parameter Types

| type | data keys | ใช้เมื่อ |
|------|-----------|---------|
| `checkbox` | `{"required": true}` | เปิด/ปิด option |
| `string` | `{"masks": false, "required": true, "useMask": false, "unmaskValue": ""}` | path โฟลเดอร์ |
| `filepath` | `{"required": true}` | path ไฟล์ .txt |
| `number` | `{"required": true}` | ตัวเลข |
| `divider` | `{"thickness": 1, "marginTop": 5, "marginBottom": 5, "label": "Section Name"}` | แบ่ง section |
| `label` | `{"text": "...", "variant": "info"}` | ข้อความอธิบาย |
| `inline` | `{"height": 10}` | inline spacing |

### End Node (BlockBasic)

```json
{
  "type": "BlockBasic",
  "label": "end",
  "data": {
    "icon": "riFlagLine",
    "disableBlock": false
  }
}
```

---

## Browser Blocks

### open-url

ใช้กับ: navigate ไป URL

```json
{
  "type": "BlockBasicWithFallback",
  "label": "open-url",
  "data": {
    "active": true,
    "customUserAgent": false,
    "delay": 0,
    "description": "",
    "disableBlock": false,
    "icon": "riLink",
    "newTab": false,
    "url": "https://www.facebook.com/",
    "userAgent": "",
    "waitForNavigation": "domcontentloaded",
    "waitTabLoaded": false
  }
}
```

**Fields (11):** `active, customUserAgent, delay, description, disableBlock, icon, newTab, url, userAgent, waitForNavigation, waitTabLoaded`

### event-click

ใช้กับ: คลิก element

```json
{
  "type": "BlockBasicWithFallback",
  "label": "event-click",
  "data": {
    "delay": 0,
    "description": "Home",
    "disableBlock": false,
    "findBy": "xpath",
    "humanClick": false,
    "icon": "riCursorLine",
    "markEl": false,
    "multiple": false,
    "selectOption": "leftClick",
    "selector": "//a[@role=\"link\" and @aria-label=\"Home\"]",
    "settings": {"blockTimeout": "50000"},
    "waitForSelector": false,
    "waitSelectorTimeout": 5000,
    "x": "",
    "y": ""
  }
}
```

**Fields (15):** `delay, description, disableBlock, findBy, humanClick, icon, markEl, multiple, selectOption, selector, settings, waitForSelector, waitSelectorTimeout, x, y`

### element-exists

ใช้กับ: ตรวจว่า element บนหน้าจอมีอยู่หรือไม่

```json
{
  "type": "BlockBasicWithFallback",
  "label": "element-exists",
  "data": {
    "delay": 0,
    "description": "",
    "disableBlock": false,
    "findBy": "xpath",
    "icon": "riFocus3Line",
    "markEl": false,
    "selector": "//a[@role=\"link\" and @aria-label=\"Home\"]",
    "throwError": false,
    "timeout": 5000,
    "tryCount": 3,
    "waitBetweenRetries": 0
  }
}
```

**Fields (11):** `delay, description, disableBlock, findBy, icon, markEl, selector, throwError, timeout, tryCount, waitBetweenRetries`

### element-scroll

ใช้กับ: scroll หน้าเว็บ

```json
{
  "type": "BlockBasicWithFallback",
  "label": "element-scroll",
  "data": {
    "delay": "{{variables.delay}}000",
    "description": "",
    "disableBlock": false,
    "findBy": "cssSelector",
    "humanScroll": false,
    "icon": "riMouseLine",
    "incX": false,
    "incY": true,
    "markEl": false,
    "multiple": false,
    "scrollIntoView": false,
    "scrollX": "",
    "scrollY": 1000,
    "selector": "html",
    "smooth": true,
    "waitForSelector": false,
    "waitSelectorTimeout": 5000,
    "x": "",
    "y": ""
  }
}
```

**Fields (19):** `delay, description, disableBlock, findBy, humanScroll, icon, incX, incY, markEl, multiple, scrollIntoView, scrollX, scrollY, selector, smooth, waitForSelector, waitSelectorTimeout, x, y`

### mouse-move

ใช้กับ: เลื่อนเมาส์ไปยัง element

```json
{
  "type": "BlockBasicWithFallback",
  "label": "mouse-move",
  "data": {
    "delay": 2000,
    "description": "Friends",
    "disableBlock": false,
    "findBy": "xpath",
    "icon": "riDragMoveFill",
    "markEl": false,
    "multiple": false,
    "selector": "//a[@role=\"link\" and @aria-label=\"Friends\"]",
    "settings": {"blockTimeout": "10000"},
    "waitForSelector": false,
    "waitSelectorTimeout": 5000,
    "x": "",
    "y": ""
  }
}
```

**Fields (13):** `delay, description, disableBlock, findBy, icon, markEl, multiple, selector, settings, waitForSelector, waitSelectorTimeout, x, y`

### press-key

ใช้กับ: พิมพ์ข้อความใน input field

```json
{
  "type": "BlockBasicWithFallback",
  "label": "press-key",
  "data": {
    "action": "multiple-keys",
    "delay": 2000,
    "description": "Name Page",
    "disableBlock": false,
    "findBy": "xpath",
    "icon": "riKeyboardLine",
    "keys": "",
    "keysToPress": "{{variables.namePage}}",
    "level": "Browser",
    "pressTime": 100,
    "selector": "//span[text()=\"Page name (required)\"]/following-sibling::input",
    "settings": {"blockTimeout": "50000"},
    "$breakpoint": false
  }
}
```

**Fields (13):** `$breakpoint, action, delay, description, disableBlock, findBy, icon, keys, keysToPress, level, pressTime, selector, settings`

### forms

ใช้กับ: กรอกฟอร์ม (version ใหม่ของ input-text)

```json
{
  "type": "BlockBasicWithFallback",
  "label": "forms",
  "data": {
    "assignVariable": false,
    "clearValue": true,
    "dataColumn": "",
    "delay": 3000,
    "description": "wall",
    "disableBlock": false,
    "events": [],
    "findBy": "xpath",
    "getValue": false,
    "icon": "riInputCursorMove",
    "markEl": false,
    "multiple": false,
    "optionPosition": 1,
    "saveData": false,
    "selectOptionBy": "value",
    "selected": true,
    "selector": "//div[@role=\"textbox\" and ...]",
    "settings": {"blockTimeout": "100000"},
    "type": "text-field",
    "typingDelay": 0,
    "value": "{{variables.final_text}}\n\n{{variables.Hashtags}} .",
    "variableName": "",
    "waitForSelector": false,
    "waitSelectorTimeout": 5000
  }
}
```

**Fields (24):** `assignVariable, clearValue, dataColumn, delay, description, disableBlock, events, findBy, getValue, icon, markEl, multiple, optionPosition, saveData, selectOptionBy, selected, selector, settings, type, typingDelay, value, variableName, waitForSelector, waitSelectorTimeout`

### hover-element

ใช้กับ: hover element

```json
{
  "type": "BlockBasicWithFallback",
  "label": "hover-element",
  "data": {
    "delay": 2000,
    "description": "",
    "disableBlock": false,
    "findBy": "xpath",
    "icon": "mdiCursorDefaultClickOutline",
    "markEl": false,
    "multiple": false,
    "selector": "//div[@aria-label=\"Like\"]",
    "waitForSelector": false,
    "waitSelectorTimeout": 5000
  }
}
```

**Fields (10):** `delay, description, disableBlock, findBy, icon, markEl, multiple, selector, waitForSelector, waitSelectorTimeout`

### tab-loaded

ใช้กับ: รอให้หน้าโหลดเสร็จ

```json
{
  "type": "BlockBasicWithFallback",
  "label": "tab-loaded",
  "data": {
    "delay": 0,
    "disableBlock": false,
    "icon": "riTimerFlashLine"
  }
}
```

**Fields (3):** `delay, disableBlock, icon`

### reload-tab

ใช้กับ: reload หน้าเว็บ

```json
{
  "type": "BlockBasicWithFallback",
  "label": "reload-tab",
  "data": {
    "delay": 0,
    "disableBlock": false,
    "icon": "riRestartLine"
  }
}
```

**Fields (3):** `delay, disableBlock, icon`

---

## Control Flow Blocks

### conditions (ต้องใช้ nested schema)

```json
{
  "type": "BlockConditions",
  "label": "conditions",
  "data": {
    "icon": "riAB",
    "disableBlock": false,
    "description": "",
    "delay": 0,
    "conditions": [
      {
        "id": "group-1-id",
        "name": "Group Name",
        "conditions": [
          {
            "id": "sub-group-id",
            "conditions": [
              {
                "id": "item-group-id",
                "items": [
                  {"type": "value", "category": "value", "data": {"value": "{{variables.enableLike}}"}},
                  {"type": "eq", "category": "compare"},
                  {"type": "value", "category": "value", "data": {"value": "true"}}
                ]
              }
            ]
          }
        ]
      }
    ],
    "retryConditions": false,
    "retryCount": 10,
    "retryTimeout": 1000
  }
}
```

### Condition Item Types

| type | category | มี data? | ใช้สำหรับ |
|------|----------|----------|----------|
| `value` | `value` | `{"value": "..."}` | ค่าตัวแปรหรือ literal |
| `eq` | `compare` | **ไม่มี data** | เท่ากับ |
| `neq` | `compare` | **ไม่มี data** | ไม่เท่ากับ |
| `gt` | `compare` | **ไม่มี data** | มากกว่า |
| `lt` | `compare` | **ไม่มี data** | น้อยกว่า |
| `contains` | `compare` | **ไม่มี data** | มีข้อความ |
| `element#exists` | `value` | `{"selector": "//xpath"}` | ตรวจ element |

**โครงสร้างเงื่อนไขแบบ 3-level:**
```
Level 1: Root conditions array [{id, name, conditions:[...]}]
Level 2: Sub-group [{id, conditions:[...]}]
Level 3: Items [{id, items:[value, compare, value]}]
         หรือ [{id, items:[element#exists]}]
```

**Edge routing สำหรับ conditions:**
```
{node-id}-output-{group_id}       → match branch
{node-id}-output-fallback          → else branch
```

**ข้อสังเกตจาก 801:**
- `output-1` ก็เจอใน real scripts (กลุ่มที่ไม่มีชื่อ)
- ส่วนใหญ่ใช้ `output-{random_id}` สำหรับ named groups
- `output-fallback` สำหรับ else/not-match

### repeat-task

```json
{
  "type": "BlockRepeatTask",
  "label": "repeat-task",
  "data": {
    "disableBlock": false,
    "icon": "riRepeat2Line",
    "repeatFor": "{{variables.feedViewCount}}"
  }
}
```

**Fields (3):** `disableBlock, icon, repeatFor`

**หมายเหตุ:** `repeatFor` ใช้ variable หรือตัวเลขก็ได้ เช่น `"5"` หรือ `"{{variables.count}}"`

### loop-data

```json
{
  "type": "BlockBasicWithFallback",
  "label": "loop-data",
  "data": {
    "delay": 0,
    "description": "mainloop",
    "disableBlock": false,
    "elementSelector": "",
    "fromNumber": 1,
    "icon": "riRefreshLine",
    "loopData": [],
    "loopId": "mainloop",
    "loopThrough": "numbers",
    "maxLoop": 0,
    "referenceKey": "",
    "resumeLastWorkflow": false,
    "reverseLoop": false,
    "startIndex": 0,
    "toNumber": 1000,
    "variableName": "",
    "waitForSelector": false,
    "waitSelectorTimeout": 5000
  }
}
```

**Fields (18):** `delay, description, disableBlock, elementSelector, fromNumber, icon, loopData, loopId, loopThrough, maxLoop, referenceKey, resumeLastWorkflow, reverseLoop, startIndex, toNumber, variableName, waitForSelector, waitSelectorTimeout`

### loop-breakpoint

```json
{
  "type": "BlockLoopBreakpoint",
  "label": "loop-breakpoint",
  "data": {
    "clearLoop": false,
    "disableBlock": false,
    "icon": "riStopLine",
    "loopId": "mainloop"
  }
}
```

**Fields (4):** `clearLoop, disableBlock, icon, loopId`

**สำคัญ:** 
- edges วิ่งออกจาก loop-breakpoint → ไปที่ node ถัดไป (ไม่ใช่กลับไปที่ loop-data)
- `loopId` ต้องตรงกับ loop-data ที่ต้องการ break

---

## Delay

```json
{
  "type": "BlockDelay",
  "label": "delay",
  "data": {
    "disableBlock": false,
    "icon": "riTimerLine",
    "time": 2000
  }
}
```

**Fields (3):** `disableBlock, icon, time`

**`time` field:**
- `2000` = 2 วิ คงที่ (number type — ไม่ใช่ string!)
- `"3,7"` = random 3-7 วิ (string แบบคอมม่า)

---

## JavaScript Code

```json
{
  "type": "BlockBasicWithFallback",
  "label": "javascript-code",
  "data": {
    "code": "const index = Number(RefData(\"variables\", \"number_page\"));\nconst id_list = RefData(\"variables\", \"list_page\");\n...",
    "context": "website",
    "delay": 0,
    "description": "set URL",
    "disableBlock": false,
    "everyNewTab": false,
    "icon": "riCodeSSlashLine",
    "preloadScripts": [],
    "runBeforeLoad": false,
    "timeout": 20000
  }
}
```

**Fields (10):** `code, context, delay, description, disableBlock, everyNewTab, icon, preloadScripts, runBeforeLoad, timeout`

**API function ที่ใช้ได้ใน JS blocks:**
- `RefData("variables", "name")` — อ่านค่า variable
- `SetVariable("name", value)` — ตั้งค่า variable
- `await page.evaluate(() => ...)` — รัน JavaScript บนหน้าเว็บ (async)

**กฎ:**
- ❌ ห้าม `(() => { ... })()` wrapper
- ✅ Top-level statements โดยตรง
- ✅ ใช้ `RefData` / `SetVariable` API โดยตรง
- ❌ `return;` ใช้ไม่ได้ (ทำให้เกิด `reading 'insert'` error)
- `context: "website"` คือค่า default ที่ใช้จริง

---

## Data Blocks

### read-file-text

ใช้กับ: อ่านไฟล์ .txt ทีละบรรทัด

```json
{
  "type": "BlockBasicWithFallback",
  "label": "read-file-text",
  "data": {
    "assignVariable": false,
    "delay": 0,
    "deleteLine": true,
    "delimiter": "",
    "description": "",
    "disableBlock": false,
    "icon": "riFileTextLine",
    "mode": "aline",
    "path": "{{variables.pageNameFilePath}}",
    "randomEnable": true,
    "variableName": "namePage"
  }
}
```

**Fields (11):** `assignVariable, delay, deleteLine, delimiter, description, disableBlock, icon, mode, path, randomEnable, variableName`

**`mode` options:**
- `"aline"` — อ่านทีละบรรทัด (sequential)
- `"allValue"` หรืออื่นๆ

### write-file / file-action

ใช้กับ: เขียนไฟล์

```json
{
  "type": "BlockBasicWithFallback",
  "label": "file-action",
  "data": {
    "action": "Write",
    "appendMode": "newLine",
    "delay": 0,
    "deleteFileFolder": "",
    "delimiter": "",
    "description": "เก็บLinkPost",
    "disableBlock": false,
    "filePath": "{{variables.postLinksFilePath}}",
    "icon": "riFileTextLine",
    "inputData": "{{variables.LinkPost}}|{{profileName}}|{{loopData.pageloop}}",
    "selectorType": "txt",
    "writeMode": "append"
  }
}
```

**Fields (12):** `action, appendMode, delay, deleteFileFolder, delimiter, description, disableBlock, filePath, icon, inputData, selectorType, writeMode`

### insert-data (insertData)

ใช้กับ: insert ข้อมูลลง data table ใน GL

```json
{
  "type": "BlockBasicWithFallback",
  "label": "insert-data",
  "data": {
    "block": "insertData",
    "blockId": "tk9ytpe",
    "dataList": [
      {"type": "variable", "name": "viewFeed", "value": "false"}
    ],
    "delay": 0,
    "description": "",
    "disableBlock": false,
    "icon": "riDatabase2Line"
  }
}
```

**Fields (7):** `block, blockId, dataList, delay, description, disableBlock, icon`

**dataList items:**
```json
{"type": "variable", "name": "varName", "value": "varValue"}
```

### random

ใช้กับ: สุ่มค่า

```json
{
  "type": "BlockBasicWithFallback",
  "label": "random",
  "data": {
    "categories": "simple",
    "command": "",
    "delay": 0,
    "description": "",
    "disableBlock": false,
    "fromNumber": 5,
    "icon": "riDiceLine",
    "language": "EN",
    "toNumber": 10,
    "type": "number",
    "variableName": "delay"
  }
}
```

**Fields (11):** `categories, command, delay, description, disableBlock, fromNumber, icon, language, toNumber, type, variableName`

### increase-variable

ใช้กับ: เพิ่มค่าตัวแปรทีละ 1

```json
{
  "type": "BlockBasicWithFallback",
  "label": "increase-variable",
  "data": {
    "delay": 1000,
    "description": "",
    "disableBlock": false,
    "icon": "riIncreaseDecreaseLine",
    "increaseBy": 1,
    "variableName": "notificationReadRounds"
  }
}
```

**Fields (6):** `delay, description, disableBlock, icon, increaseBy, variableName`

### upload-file

ใช้กับ: อัปโหลดไฟล์

```json
{
  "type": "BlockBasicWithFallback",
  "label": "upload-file",
  "data": {
    "delay": 5000,
    "description": "Add profile picture",
    "disableBlock": false,
    "filePaths": ["path/to/file.jpg"],
    "findBy": "xpath",
    "folderPath": "",
    "icon": "riFileUploadLine",
    "isFolderPath": false,
    "selector": "//span[contains(text(), \"Add\")]",
    "waitForSelector": false,
    "waitSelectorTimeout": 5000
  }
}
```

**Fields (11):** `delay, description, disableBlock, filePaths, findBy, folderPath, icon, isFolderPath, selector, waitForSelector, waitSelectorTimeout`

### clipboard

ใช้กับ: จัดการ clipboard

```json
{
  "type": "BlockBasicWithFallback",
  "label": "clipboard",
  "data": {
    "assignVariable": true,
    "copySelectedText": false,
    "dataColumn": "",
    "dataToCopy": "",
    "delay": 0,
    "description": "เก็บเป็นตัวแปร",
    "disableBlock": false,
    "icon": "riClipboardLine",
    "saveData": false,
    "type": "get",
    "variableName": "LinkPost"
  }
}
```

**Fields (11):** `assignVariable, copySelectedText, dataColumn, dataToCopy, delay, description, disableBlock, icon, saveData, type, variableName`

### delete-data

ใช้กับ: ลบข้อมูล (variable)

```json
{
  "type": "BlockBasicWithFallback",
  "label": "delete-data",
  "data": {
    "delay": 0,
    "deleteList": [
      {"type": "variable", "variableName": "delay", "columnId": "[all]"}
    ],
    "description": "",
    "disableBlock": false,
    "icon": "riDeleteBin7Line"
  }
}
```

**Fields (5):** `delay, deleteList, description, disableBlock, icon`

### split-data

ใช้กับ: split string เป็น array

```json
{
  "type": "BlockBasicWithFallback",
  "label": "split-data",
  "data": {
    "assignVariable": true,
    "delay": 0,
    "delimiter": ",",
    "description": "",
    "disableBlock": false,
    "icon": "riSortAsc",
    "indexPosition": 1,
    "isTrimWhitespaces": true,
    "mode": "allValue",
    "valueSplit": "{{variables.hashtag}}",
    "variableName": "hashtag"
  }
}
```

**Fields (11):** `assignVariable, delay, delimiter, description, disableBlock, icon, indexPosition, isTrimWhitespaces, mode, valueSplit, variableName`

### get-file-path

ใช้กับ: เลือกไฟล์จาก folder

```json
{
  "type": "BlockBasicWithFallback",
  "label": "get-file-path",
  "data": {
    "assignVariable": true,
    "delay": 0,
    "description": "",
    "disableBlock": false,
    "fileType": "",
    "folderName": "",
    "icon": "riFileTextLine",
    "isAddSubFolder": false,
    "isFileType": false,
    "pathFolder": "{{variables.profileImageFolderPath}}",
    "variableName": "Profile_pic"
  }
}
```

**Fields (11):** `assignVariable, delay, description, disableBlock, fileType, folderName, icon, isAddSubFolder, isFileType, pathFolder, variableName`

### commandPro

ใช้กับ: รัน shell command

```json
{
  "type": "BlockBasicWithFallback",
  "label": "commandPro",
  "data": {
    "assignVariable": false,
    "command": "curl -L -k -A \"Mozilla/5.0\" \"{{variables.loopimage}}\" -o /tmp/temp_fb.jpg",
    "delay": 0,
    "description": "MacOS",
    "icon": "riTerminalBoxLine",
    "regex": "",
    "type": "terminal",
    "variableName": ""
  }
}
```

**Fields (8):** `assignVariable, command, delay, description, icon, regex, type, variableName`

---

## Edge Format

```json
{
  "id": "vueflow__edge-{source}-output-{n}-{target}-input-1",
  "type": "bezier",
  "source": "source-node-id",
  "target": "target-node-id",
  "sourceHandle": "source-node-id-output-1",
  "targetHandle": "target-node-id-input-1",
  "updatable": true,
  "selectable": true,
  "data": {},
  "label": "",
  "markerEnd": {"type": "arrowclosed", "width": 20, "height": 20, "color": "#b1b1b7"}
}
```

### Edge SourceHandle Types

| Format | ใช้เมื่อ |
|--------|---------|
| `{node-id}-output-1` | Default (ทุก node type) |
| `{node-id}-output-fallback` | conditions else branch |
| `{node-id}-output-{group_id}` | conditions match branch (random string) |

**ข้อสังเกต:** sourceHandle ใน real scripts ใช้ `{random_id}-output-{n}` pattern โดยที่ `{random_id}` คือ node id จริง

---

## Checklist ก่อน Export

- [ ] ทุก node มี `label` (ใช้ top-level `n['label']` — ไม่ใช่ data.label)
- [ ] `trigger` มี `type: "manual"` + parameters ครบ
- [ ] แต่ละ `BlockBasicWithFallback` มี field ครบตาม label
- [ ] `conditions` ใช้ nested schema (ไม่ใช่ flat)
- [ ] `delay` ใช้ `N,M` format (string) หรือ number
- [ ] `javascript-code` ไม่มี IIFE
- [ ] edges sourceHandle ถูกต้อง
- [ ] มี `trigger` node และ `end` node
