---
name: gemlogin-real-examples
description: ตัวอย่างจริงจากสคริปต์ 801 — node structure, edge routing, trigger parameters, conditions schema
metadata:
  type: skill
  category: gemlogin
  owner: gemmy
---

# 📋 GemLogin Real Examples — ถอดจากสคริปต์ 8 ไฟล์จริง

> แหล่งที่มา: `/mnt/d/skills/WorkflowGemlogin/801/`
> ถอดเมื่อ: 2026-06-29

---

## 1. (Faccebook) Warm Facebook.gemlogin

**ขนาด:** 70 nodes, 85 edges
**Internal name:** `(Faccebook) Warm Facebook`

### Node Distribution
| Type | Count |
|------|-------|
| BlockBasicWithFallback | 47 |
| BlockRepeatTask | 8 |
| BlockLoopBreakpoint | 5 |
| BlockConditions | 4 |
| BlockDelay | 4 |
| BlockBasic | 2 |

### Labels Used (BlockBasicWithFallback)
`event-click` (ส่วนมาก), `element-exists`, `element-scroll`, `random`, `insert-data`, `increase-variable`, `mouse-move`, `open-url`, `tab-loaded`, `delete-data`, `loop-data`, `read-file-text`

### ตัวอย่าง Node: open-url
```json
{
  "id": "eodj5ap",
  "type": "BlockBasicWithFallback",
  "label": "open-url",
  "position": {"x": 100, "y": 200},
  "data": {
    "active": true,
    "customUserAgent": false,
    "delay": 5000,
    "description": "",
    "disableBlock": false,
    "icon": "riLink",
    "newTab": false,
    "url": "https://www.facebook.com/friends",
    "userAgent": "",
    "waitForNavigation": "domcontentloaded",
    "waitTabLoaded": false
  }
}
```

### ตัวอย่าง Node: element-scroll
```json
{
  "id": "bh740gl",
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

### ตัวอย่าง Node: insert-data
```json
{
  "id": "bh740gl",
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

---

## 2. (Facebook) Add Friends from Groups or Page 1.0.gemlogin

**ขนาด:** 13 nodes, 14 edges
**Internal name:** `(Facebook) Add Friends from Groups or Page 1.0`

### Node Distribution
| Type | Count |
|------|-------|
| BlockBasicWithFallback | 8 |
| BlockBasic | 2 |
| BlockRepeatTask | 2 |
| BlockConditions | 1 |

### Labels Used
`open-url`, `tab-loaded`, `event-click`, `element-exists`, `press-key`, `delay`

### Workflow Structure (Simplest)
```
trigger → open-url → tab-loaded → element-exists → conditions
  ├─ match → press-key (add friend) → delay → event-click (confirm)
  └─ fallback → event-click (skip) → delay
```

### ตัวอย่าง Edge
```json
{
  "id": "vueflow__edge-ahq8x9j-output-1-fpnbfzv-input-1",
  "type": "bezier",
  "source": "ahq8x9j",
  "target": "fpnbfzv",
  "sourceHandle": "ahq8x9j-output-1",
  "targetHandle": "fpnbfzv-input-1"
}
```

---

## 3. (Facebook) Create Page 1.1.gemlogin

**ขนาด:** 41 nodes, 45 edges
**Internal name:** `(Facebook) Create Page 1.1`

### Node Distribution
| Type | Count |
|------|-------|
| BlockBasicWithFallback | 29 |
| BlockConditions | 4 |
| BlockDelay | 4 |
| BlockBasic | 2 |
| BlockRepeatTask | 2 |

### ตัวอย่าง Node: press-key (พิมพ์ชื่อ Page)
```json
{
  "id": "...",
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
    "settings": {"blockTimeout": "50000"}
  }
}
```

### ตัวอย่าง Node: upload-file
```json
{
  "id": "...",
  "type": "BlockBasicWithFallback",
  "label": "upload-file",
  "data": {
    "delay": 5000,
    "description": "Add profile picture",
    "disableBlock": false,
    "filePaths": ["C:\\path\\to\\profile.jpg"],
    "findBy": "xpath",
    "folderPath": "",
    "icon": "riFileUploadLine",
    "isFolderPath": false,
    "selector": "//span[contains(text(), \"Add profile picture\")]",
    "waitForSelector": false,
    "waitSelectorTimeout": 5000
  }
}
```

---

## 4. (Facebook) Like && Comment 1.6.gemlogin

**ขนาด:** 83 nodes, 102 edges
**Internal name:** `(Facebook) Like && Comment 1.6`

### Node Distribution
| Type | Count |
|------|-------|
| BlockBasicWithFallback | 63 |
| BlockConditions | 9 |
| BlockLoopBreakpoint | 5 |
| BlockDelay | 4 |
| BlockBasic | 2 |

### Trigger Parameters (14 params)
```
- Divider: "Like Comment"
- Label: "Please choose only one option."
- Checkbox: usePersonalProfile (default: true)
- Checkbox: usePageProfile (default: false)
- Divider: "Change page"
- Label: info text
- String: pageIdFolderPath (default: C:\Users\Admin\Downloads\UID)
- Divider/Inline spacing
- Filepath: link_post (default: C:\Users\Admin\Downloads\linkPost.txt)
- Checkbox: enableLike (default: true)
- Checkbox: enableComment (default: true)
- Filepath: commentFilePath (default: C:\Users\Admin\Downloads\Comments.txt)
- Checkbox: deleteUsedComments (default: false)
```

### Conditions Schema Example (Real)
```json
{
  "conditions": [
    {
      "id": "2E2D02IC3wcUwcZOkRwv-",
      "name": "Like",
      "conditions": [
        {
          "id": "GjGzgwbZ58SdIPBHmUfuW",
          "conditions": [
            {
              "id": "SmxHGwFZUkNK_LkYHwg3d",
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
  ]
}
```

### Condition with element#exists
```json
{
  "items": [
    {"type": "element#exists", "category": "value", "data": {"selector": "//span[text()=\"Add to story\"]"}}
  ]
}
```

---

## 5. (Facebook) Post Page 1.9.gemlogin

**ขนาด:** 230 nodes, 298 edges — ใหญ่ที่สุดใน 801
**Internal name:** `(Facebook) Post Page 1.9`

### Node Distribution
| Type | Count |
|------|-------|
| BlockBasicWithFallback | 179 |
| BlockDelay | 18 |
| BlockConditions | 15 |
| BlockRepeatTask | 11 |
| BlockLoopBreakpoint | 6 |
| BlockBasic | 1 |

### Labels Used (ครบทุก label ที่มี)
`open-url`, `tab-loaded`, `event-click`, `element-exists`, `element-scroll`, `press-key`, `random`, `loop-data`, `forms`, `clipboard`, `file-action`, `javascript-code`, `increase-variable`, `read-file-text`, `insert-data`, `upload-file`, `mouse-move`, `reload-tab`, `hover-element`, `delete-data`, `split-data`

### Trigger Parameters (51 params — มากที่สุด)
ตัวอย่างกลุ่ม parameters:
- **Content type selection:** postOnlyPictures, postOnlyVideos, postGif, postMixPicturesVideos, postMixGifPictures
- **Count settings:** picturePostCount, videoPostCount, gifPostCount, mixedPostPictureCount, mixedPostVideoCount
- **Target:** Post_Wall, Post_Group, Group_join, File_idGroups
- **File paths:** fileCountFilePath, captionFolderPath, hashtagFolderPath, mediaFolderPath, gifMediaFolderPath, mediaVideosFolderPath
- **Post-interaction:** reactToPost, commentAfterPosting, removeUsedComments
- **Location:** useIndonesiaLocation, useThailandLocation + 6 ภาคของไทย

### ตัวอย่าง Node: forms (type: text-field)
```json
{
  "type": "BlockBasicWithFallback",
  "label": "forms",
  "data": {
    "assignVariable": false,
    "clearValue": true,
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
    "selector": "//div[@role=\"textbox\" and starts-with(@aria-placeholder, \"What's on your mind\")]",
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

---

## 6. (Facebook) Share 1.6.gemlogin

**ขนาด:** 61 nodes, 74 edges
**Internal name:** `(Facebook) Share 1.6`

### Node Distribution
| Type | Count |
|------|-------|
| BlockBasicWithFallback | 40 |
| BlockConditions | 9 |
| BlockDelay | 5 |
| BlockLoopBreakpoint | 4 |
| BlockBasic | 3 |

### ตัวอย่าง Node: file-action (write)
```json
{
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
    "inputData": "{{variables.LinkPost}}|{{profileName}}",
    "selectorType": "txt",
    "writeMode": "append"
  }
}
```

### ตัวอย่าง Node: clipboard
```json
{
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

---

## 7. (SEO) 1.0.gemlogin

**ขนาด:** 43 nodes, 45 edges
**Internal name:** `(SEO) 1.0`

### Node Distribution
| Type | Count |
|------|-------|
| BlockBasicWithFallback | 29 |
| BlockRepeatTask | 5 |
| BlockBasic | 3 |
| BlockDelay | 3 |
| BlockLoopBreakpoint | 2 |
| BlockConditions | 1 |

### Labels Used
`open-url`, `element-scroll`, `javascript-code`, `delay`, `repeat-task`, `loop-breakpoint`, `random`

### Edge SourceHandle Distribution
| Type | Count |
|------|-------|
| output-1 | 37 |
| output-{group_id} | 7 |
| output-fallback | 1 |

---

## 8. Post Status v.6.gemlogin

**ขนาด:** 53 nodes, 59 edges
**Internal name:** `Post Status v.6`

### Node Distribution
| Type | Count |
|------|-------|
| BlockBasicWithFallback | 40 |
| BlockConditions | 5 |
| BlockLoopBreakpoint | 5 |
| BlockBasic | 2 |
| BlockDelay | 1 |

### Labels Used
`open-url`, `element-exists`, `event-click`, `javascript-code`, `commandPro`, `split-data`, `delay`, `loop-breakpoint`, `read-file-text`, `increase-variable`, `press-key`, `insert-data`

### ตัวอย่าง Node: commandPro (Mac)
```json
{
  "label": "commandPro",
  "data": {
    "assignVariable": false,
    "command": "curl -L -k -A \"Mozilla/5.0\" \"{{variables.loopimage}}\" -o /tmp/temp_fb.jpg && osascript -e 'set the clipboard to (read (POSIX file \"/tmp/temp_fb.jpg\") as JPEG picture)'",
    "delay": 0,
    "description": "MacOS",
    "icon": "riTerminalBoxLine",
    "regex": "",
    "type": "terminal",
    "variableName": ""
  }
}
```

### ตัวอย่าง Node: commandPro (Windows)
```json
{
  "label": "commandPro",
  "data": {
    "assignVariable": false,
    "command": "if (!(Test-Path 'C:\\tmp')) { New-Item -ItemType Directory -Path 'C:\\tmp' }; Invoke-WebRequest -Uri '{{variables.loopimage}}' -OutFile 'C:\\tmp\\image_{{profileId}}.jpg' -UseBasicParsing",
    "delay": 0,
    "description": "Windows",
    "icon": "riTerminalBoxLine",
    "regex": "",
    "type": "powershell",
    "variableName": ""
  }
}
```

---

## สรุป: Complete Field Inventory (All Labels X All Fields)

### BlockBasicWithFallback — Field Usage Matrix

| Field | event-click | open-url | element-exists | element-scroll | press-key | loop-data | read-file-text | random | insert-data | javascript-code | forms | mouse-move | increase-variable | upload-file | file-action | clipboard | split-data | delete-data | commandPro | get-file-path | hover-element | tab-loaded | reload-tab |
|-------|:-----------:|:--------:|:--------------:|:--------------:|:---------:|:---------:|:--------------:|:-----:|:-----------:|:---------------:|:-----:|:----------:|:-----------------:|:-----------:|:-----------:|:---------:|:----------:|:-----------:|:----------:|:-------------:|:------------:|:----------:|:----------:|
| delay | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| description | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | |
| disableBlock | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| icon | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| findBy | ✓ | | ✓ | ✓ | ✓ | | | | | | ✓ | ✓ | | ✓ | | | | | | | ✓ | | |
| selector | ✓ | | ✓ | ✓ | ✓ | | | | | | ✓ | ✓ | | ✓ | | | | | | | ✓ | | |
| waitForSelector | ✓ | | ✓ | ✓ | | ✓ | | | | | ✓ | ✓ | | ✓ | | | | | | | ✓ | | |
| waitSelectorTimeout | ✓ | | ✓ | ✓ | | ✓ | | | | | ✓ | ✓ | | ✓ | | | | | | | ✓ | | |
| markEl | ✓ | | ✓ | ✓ | | | | | | | ✓ | ✓ | | | | | | | | | ✓ | | |
| multiple | ✓ | | | ✓ | | | | | | | ✓ | ✓ | | | | | | | | | ✓ | | |
| settings | ✓ | | | | ✓ | | | | | | ✓ | ✓ | | | | | | | | | | | |
| selectOption | ✓ | | | | | | | | | | | | | | | | | | | | | | |
| humanClick | ✓ | | | | | | | | | | | | | | | | | | | | | | |
| x | ✓ | | | ✓ | | | | | | | | ✓ | | | | | | | | | | | |
| y | ✓ | | | ✓ | | | | | | | | ✓ | | | | | | | | | | | |
| url | | ✓ | | | | | | | | | | | | | | | | | | | | | |
| active | | ✓ | | | | | | | | | | | | | | | | | | | | | |
| newTab | | ✓ | | | | | | | | | | | | | | | | | | | | | |
| waitTabLoaded | | ✓ | | | | | | | | | | | | | | | | | | | | | |
| userAgent | | ✓ | | | | | | | | | | | | | | | | | | | | | |
| customUserAgent | | ✓ | | | | | | | | | | | | | | | | | | | | | |
| waitForNavigation | | ✓ | | | | | | | | | | | | | | | | | | | | | |
| scrollY | | | | ✓ | | | | | | | | | | | | | | | | | | | |
| scrollX | | | | ✓ | | | | | | | | | | | | | | | | | | | |
| smooth | | | | ✓ | | | | | | | | | | | | | | | | | | | |
| incY | | | | ✓ | | | | | | | | | | | | | | | | | | | |
| incX | | | | ✓ | | | | | | | | | | | | | | | | | | | |
| humanScroll | | | | ✓ | | | | | | | | | | | | | | | | | | | |
| scrollIntoView | | | | ✓ | | | | | | | | | | | | | | | | | | | |
| throwError | | | ✓ | | | | | | | | | | | | | | | | | | | | |
| timeout | | | ✓ | | | | | | | ✓ | | | | | | | | | | | | | |
| tryCount | | | ✓ | | | | | | | | | | | | | | | | | | | | |
| waitBetweenRetries | | | ✓ | | | | | | | | | | | | | | | | | | | | |
| action | | | | | ✓ | | | | | | | | | | ✓ | | | | | | | | |
| keysToPress | | | | | ✓ | | | | | | | | | | | | | | | | | | |
| keys | | | | | ✓ | | | | | | | | | | | | | | | | | | |
| level | | | | | ✓ | | | | | | | | | | | | | | | | | | |
| pressTime | | | | | ✓ | | | | | | | | | | | | | | | | | | |
| $breakpoint | | | | | ✓ | | | | | | | | | | | | | | | | | | |
| variableName | | | | | | ✓ | ✓ | ✓ | | | ✓ | | ✓ | | | ✓ | ✓ | | | ✓ | | | |
| loopId | | | | | | ✓ | | | | | | | | | | | | | | | | | |
| loopThrough | | | | | | ✓ | | | | | | | | | | | | | | | | | |
| fromNumber | | | | | | ✓ | | ✓ | | | | | | | | | | | | | | | |
| toNumber | | | | | | ✓ | | ✓ | | | | | | | | | | | | | | | |
| startIndex | | | | | | ✓ | | | | | | | | | | | | | | | | | |
| maxLoop | | | | | | ✓ | | | | | | | | | | | | | | | | | |
| loopData | | | | | | ✓ | | | | | | | | | | | | | | | | | |
| reverseLoop | | | | | | ✓ | | | | | | | | | | | | | | | | | |
| resumeLastWorkflow | | | | | | ✓ | | | | | | | | | | | | | | | | | |
| referenceKey | | | | | | ✓ | | | | | | | | | | | | | | | | | |
| elementSelector | | | | | | ✓ | | | | | | | | | | | | | | | | | |
| path | | | | | | | ✓ | | | | | | | | | | | | | | | | |
| mode | | | | | | | ✓ | | | | | | | | | | ✓ | | | | | | |
| deleteLine | | | | | | | ✓ | | | | | | | | | | | | | | | | |
| delimiter | | | | | | | ✓ | | | | | | | | ✓ | | ✓ | | | | | | |
| randomEnable | | | | | | | ✓ | | | | | | | | | | | | | | | | |
| assignVariable | | | | | | | ✓ | | | | | | | | | ✓ | ✓ | | | ✓ | | | |
| type | | | | | | | | ✓ | | | | | | | | ✓ | | | ✓ | | | | |
| command | | | | | | | | ✓ | | | | | | | | | | | ✓ | | | | |
| categories | | | | | | | | ✓ | | | | | | | | | | | | | | | |
| language | | | | | | | | ✓ | | | | | | | | | | | | | | | |
| block | | | | | | | | | ✓ | | | | | | | | | | | | | | |
| blockId | | | | | | | | | ✓ | | | | | | | | | | | | | | |
| dataList | | | | | | | | | ✓ | | | | | | | | | | | | | | |
| code | | | | | | | | | | ✓ | | | | | | | | | | | | | |
| context | | | | | | | | | | ✓ | | | | | | | | | | | | | |
| everyNewTab | | | | | | | | | | ✓ | | | | | | | | | | | | | |
| preloadScripts | | | | | | | | | | ✓ | | | | | | | | | | | | | |
| runBeforeLoad | | | | | | | | | | ✓ | | | | | | | | | | | | | |
| clearValue | | | | | | | | | | | ✓ | | | | | | | | | | | | |
| value | | | | | | | | | | | ✓ | | | | | | | | | | | | |
| events | | | | | | | | | | | ✓ | | | | | | | | | | | | |
| getValue | | | | | | | | | | | ✓ | | | | | | | | | | | | |
| saveData | | | | | | | | | | | ✓ | | | | | ✓ | | | | | | | |
| selected | | | | | | | | | | | ✓ | | | | | | | | | | | | |
| selectOptionBy | | | | | | | | | | | ✓ | | | | | | | | | | | | |
| optionPosition | | | | | | | | | | | ✓ | | | | | | | | | | | | |
| typingDelay | | | | | | | | | | | ✓ | | | | | | | | | | | | |
| increaseBy | | | | | | | | | | | | | ✓ | | | | | | | | | | |
| filePaths | | | | | | | | | | | | | | ✓ | | | | | | | | | |
| folderPath | | | | | | | | | | | | | | ✓ | | | | | | | | | |
| isFolderPath | | | | | | | | | | | | | | ✓ | | | | | | | | | |
| writeMode | | | | | | | | | | | | | | | ✓ | | | | | | | | |
| appendMode | | | | | | | | | | | | | | | ✓ | | | | | | | | |
| inputData | | | | | | | | | | | | | | | ✓ | | | | | | | | |
| filePath | | | | | | | | | | | | | | | ✓ | | | | | | | | |
| selectorType | | | | | | | | | | | | | | | ✓ | | | | | | | | |
| deleteFileFolder | | | | | | | | | | | | | | | ✓ | | | | | | | | |
| dataToCopy | | | | | | | | | | | | | | | | ✓ | | | | | | | |
| copySelectedText | | | | | | | | | | | | | | | | ✓ | | | | | | | |
| dataColumn | | | | | | | | | | | | | | | | ✓ | | | | | | | |
| valueSplit | | | | | | | | | | | | | | | | | ✓ | | | | | | |
| indexPosition | | | | | | | | | | | | | | | | | ✓ | | | | | | |
| isTrimWhitespaces | | | | | | | | | | | | | | | | | ✓ | | | | | | |
| deleteList | | | | | | | | | | | | | | | | | | ✓ | | | | | |
| command | | | | | | | | | | | | | | | | | | | ✓ | | | | |
| regex | | | | | | | | | | | | | | | | | | | ✓ | | | | |
| pathFolder | | | | | | | | | | | | | | | | | | | | ✓ | | | |
| folderName | | | | | | | | | | | | | | | | | | | | ✓ | | | |
| fileType | | | | | | | | | | | | | | | | | | | | ✓ | | | |
| isAddSubFolder | | | | | | | | | | | | | | | | | | | | ✓ | | | |
| isFileType | | | | | | | | | | | | | | | | | | | | ✓ | | | |
