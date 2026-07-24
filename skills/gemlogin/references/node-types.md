# GemLogin Workflow Node Types (v5.0.8)

Complete catalog of all GemLogin workflow node types extracted from production database (49 workflows).

## Node Anatomy

Every node in GemLogin `drawflow` follows this structure:

```json
{
  "id": "unique_7_char_id",
  "type": "BlockType",
  "label": "human-readable-label",
  "initialized": false,
  "position": { "x": 0, "y": 0 },
  "data": {
    "icon": "riIconName",
    "disableBlock": false,
    "description": "",
    "...type-specific fields..."
  },
  "events": {},
  "blockId": "same-as-id"  // optional
}
```

**Key rules:**
- Nodes live in `script → drawflow → nodes` (object keyed by node id)
- Edges live in `script → drawflow → edges` (object keyed by edge id)
- `type` determines block behavior; `label` is the human name
- Many executable nodes share `type: "BlockBasicWithFallback"` — real kind identified by `label`

---

## All Node Types (9 types, 49 labels)

### 1. BlockBasicWithFallback
The most common type — general-purpose action blocks. Label determines actual behavior.

| Label | Icon | Category | Description |
|-------|------|----------|-------------|
| `open-url` | riGlobalLine | 🌐 Navigation | Open/navigate to URL |
| `event-click` | riCursorLine | 🖱️ Interaction | Click an element by XPath/CSS |
| `clipboard` | riClipboardLine | 📋 Data | Read/write clipboard (⚠️ not supported in background) |
| `file-action` | riFileTextLine | 📁 File | File read/write/delete operations |
| `command` | riTerminalBoxLine | ⚡ System | Run shell command |
| `commandPro` | riTerminalBoxLine | ⚡ System | Advanced command execution |
| `press-key` | riKeyboardLine | ⌨️ Input | Send keyboard key presses |
| `element-scroll` | riScrollToBottomLine | 📜 Scroll | Scroll element/page |
| `hover-element` | riFocus2Line | 🖱️ Interaction | Hover mouse over element |
| `mouse-move` | riMouseLine | 🖱️ Interaction | Move mouse to coordinates |
| `forms` | riInputField | 📝 Form | Fill form fields |
| `get-text` | riText | 📖 Extract | Extract text from element |
| `get-file-path` | riFolderLine | 📁 File | Get file path |
| `read-file-text` | riFileTextLine | 📁 File | Read text file contents |
| `upload-file` | riUploadLine | 📤 Upload | Upload file to page |
| `take-screenshot` | riCameraLine | 📸 Media | Capture screenshot |
| `close-tab` | riCloseLine | 🌐 Tab | Close current browser tab |
| `reload-tab` | riRefreshLine | 🌐 Tab | Reload current page |
| `go-back` | riArrowGoBackLine | 🌐 Nav | Navigate back |
| `tab-loaded` | riCheckLine | 🌐 Tab | Wait for tab to load |
| `tab-url` | riLink | 🌐 Tab | Get/check current tab URL |
| `infor-tabs` | riInformationLine | 🌐 Tab | Get info about open tabs |
| `resource-status` | riCheckDoubleLine | 🔍 Check | Check resource/HTTP status |
| `element-exists` | riCheckboxCircleLine | 🔍 Check | Check if element exists |
| `cookie` | riCookieLine | 🍪 Data | Get/set cookies |
| `random` | riShuffleLine | 🎲 Logic | Generate random value |
| `delay` | riTimerLine | ⏱️ Timing | Wait/pause |
| `increase-variable` | riAddLine | 🔢 Logic | Increment variable |
| `regex-variable` | riCodeLine | 🔧 Logic | Regex on variable |
| `split-data` | riSplitCellsHorizontal | 📊 Data | Split data string |
| `insert-data` | riDatabase2Line | 📊 Data | Insert data into source |
| `delete-data` | riDeleteBinLine | 📊 Data | Delete data |
| `loop-data` | riLoopLeftLine | 🔄 Loop | Loop over data items |
| `webhook` | riWebhookLine | 🌐 API | Call webhook URL |
| `google-sheets` | riGoogleLine | 📊 API | Google Sheets integration |
| `block-package` | riPackageLine | 📦 Package | Run sub-workflow package |
| `javascript-code` | riCodeBoxLine | 💻 Code | Run custom JavaScript |
| `gem-ai` | riRobotLine | 🤖 AI | GemLogin AI block |
| `Gemlogin-Ai` | riRobotLine | 🤖 AI | GemLogin AI (alternate) |
| `chat-gpt` | riOpenaiLine | 🤖 AI | ChatGPT integration |
| `deep-seek` | riOpenaiLine | 🤖 AI | DeepSeek integration |
| `grok` | riOpenaiLine | 🤖 AI | Grok integration |

### 2. BlockConditions
| Label | Icon | Description |
|-------|------|-------------|
| `conditions` | riAB | Branch router — splits flow based on variable value. Each outgoing edge has a `sourceHandle` matching a condition id like `<node-id>-output-cond-<name>`. |

### 3. BlockDelay
| Label | Icon | Description |
|-------|------|-------------|
| `delay` | riTimerLine | Timed delay block (dedicated type) |

### 4. BlockLoopBreakpoint
| Label | Icon | Description |
|-------|------|-------------|
| `loop-breakpoint` | riStopLine | Loop control point. Key fields: `loopId` (which loop), `clearLoop` (exit/reset loop) |

### 5. BlockNote
| Label | Icon | Description |
|-------|------|-------------|
| `note` | riStickyNoteLine | Sticky note — documentation only, not executed |

### 6. BlockPackage
| Label | Icon | Description |
|-------|------|-------------|
| `block-package` | riPackageLine | Sub-workflow / package runner |

### 7. 🆕 BlockPointToPoint (v5.0.8)
| Label | Icon | Description |
|-------|------|-------------|
| `point-to-point` | riLinksLine | **Teleport / Jump node** — redirects execution to another node by `targetId` |

### 8. BlockRepeatTask
| Label | Icon | Description |
|-------|------|-------------|
| `repeat-task` | riRepeatLine | Repeat a task section |

### 9. BlockBasic
| Label | Icon | Description |
|-------|------|-------------|
| `trigger` | riFlashlightLine | Workflow entry point / manual trigger |
| `end` | riStopCircleLine | Workflow end point |

---

## 🆕 Point-to-Point Deep Dive

### Structure
```json
{
  "id": "15svxnl",
  "type": "BlockPointToPoint",
  "label": "point-to-point",
  "data": {
    "icon": "riLinksLine",
    "disableBlock": false,
    "description": "",
    "targetId": "p6cpfm8"       // ← THE KEY FIELD
  }
}
```

### Behavior
- Execution arrives via a normal incoming edge
- Instead of following outgoing edges, execution **immediately jumps** to the node with ID matching `targetId`
- PTP nodes have **NO outgoing edges** — the jump is the only way out
- Target node MUST exist in the same workflow

### Visual
```
Before (linear):
  [A]──→[B]──→[C]──→[D]──→[E]

With PTP (skip B,C,D):
  [A]──→[PTP]~~⤵
           [B]──→[C]──→[D]──→[E]
  PTP.targetId = "E的id"
```

### Real Example (TEST workflow)
```
[delay] ──edge──→ [point-to-point] ──targetId──→ [open-url]
                  id: 15svxnl                      id: p6cpfm8
                  targetId: "p6cpfm8"
```

### When to Use PTP
| Scenario | Why PTP |
|----------|---------|
| **Error recovery** | On error → jump back to retry start |
| **Skip ahead** | Condition met → skip optional steps |
| **Fast exit** | Done early → jump to end |
| **Branch merge** | Multiple branches converge at one point without long edges |
| **Loop restart** | Reset loop without full iteration |

### When NOT to Use PTP
| Scenario | Better choice |
|----------|--------------|
| Simple branching | `conditions` block |
| Normal loop control | `loop-breakpoint` with `clearLoop` |
| Sequential flow | Normal edges |
| Conditional skip | `conditions` → different branch |

### Patching a PTP Node
```python
# Set target
node["data"]["targetId"] = "<target_node_id>"

# Add description for documentation
node["data"]["description"] = "Jump to login retry on error"
```

### ⚠️ Pitfalls
- **Dangling target**: If `targetId` points to deleted node → workflow hangs
- **Infinite loops**: PTP → target → PTP → target → ...
- **Uninitialized state**: Jumping past initialization/cleanup nodes
- **Thread confusion**: In loop contexts, PTP may not clear iteration state
- **Debug difficulty**: Jumps are invisible in edge view — always add description

---

## Creating Nodes Programmatically

### Minimal new node
```python
import random, string

def new_node(node_type, label, x, y, **data):
    node_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
    return {
        "id": node_id,
        "type": node_type,
        "label": label,
        "initialized": False,
        "position": {"x": x, "y": y},
        "data": {
            "icon": "riCursorLine",
            "disableBlock": False,
            "description": "",
            **data
        },
        "events": {}
    }

# Example: create PTP node
ptp = new_node("BlockPointToPoint", "point-to-point", 500, 300,
               icon="riLinksLine", targetId="login_retry_node")
```

### Connecting nodes with edge
```python
def new_edge(source_id, target_id, source_handle=None):
    edge_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
    return {
        "id": edge_id,
        "source": source_id,
        "target": target_id,
        "sourceHandle": source_handle or f"{source_id}-output-1"
    }
```

### Insert into workflow
```python
import json
with open("workflow.gemlogin", "r") as f:
    wf = json.load(f)

# Read shape first
nodes = wf["script"]["drawflow"]["nodes"]
edges = wf["script"]["drawflow"]["edges"]

# Add node
new = new_node("BlockPointToPoint", "point-to-point", 600, 400,
               icon="riLinksLine", targetId="some_existing_node")
nodes[new["id"]] = new

# Route: disconnect old edge, insert PTP in middle
old_edge = edges.pop("old_edge_id")
edges[new_edge_id_1] = new_edge(old_edge["source"], new["id"], old_edge["sourceHandle"])
# PTP uses targetId, not edges, for output

with open("workflow.gemlogin", "w") as f:
    json.dump(wf, f, ensure_ascii=False, indent=2)
```

---

## Summary: All 9 Block Types

| # | Type | Count | Purpose |
|---|------|-------|---------|
| 1 | `BlockBasicWithFallback` | ~40 labels | General actions (click, type, scroll, AI, API...) |
| 2 | `BlockConditions` | 1 label | Branch router |
| 3 | `BlockDelay` | 1 label | Timed delay |
| 4 | `BlockLoopBreakpoint` | 1 label | Loop control |
| 5 | `BlockNote` | 1 label | Documentation |
| 6 | `BlockPackage` | 1 label | Sub-workflow |
| 7 | **`BlockPointToPoint`** | 🆕 1 label | **Teleport/jump** |
| 8 | `BlockRepeatTask` | 1 label | Task repeater |
| 9 | `BlockBasic` | 3 labels | Trigger, end, gem-ai |
