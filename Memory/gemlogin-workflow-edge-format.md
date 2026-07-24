---
name: gemlogin-workflow-edge-format
description: GemLogin workflow edge handle format — conditions use output-{id} not output-cond-{id}
metadata:
  type: reference
  created: 2026-07-24
  originSessionId: 99ca41cb-3229-41ef-8b4c-1541286d772f
  modified: 2026-07-24T09:58:19.949Z
---

# GemLogin Workflow — Edge Handle Format

## Condition Nodes (BlockConditions)

```json
// CORRECT: sourceHandle format is output-{conditionId}
"sourceHandle": "check-what-output-both"

// WRONG: do NOT use output-cond-{conditionId}
"sourceHandle": "check-what-output-cond-both"
```

## Regular Nodes

```json
// Main output
"sourceHandle": "nodeId-output-1"
// Fallback output  
"sourceHandle": "nodeId-output-fallback"
// Target input
"targetHandle": "nodeId-input-1"
```

## Full Edge Object (VueFlow format)

```json
{
  "id": "vueflow__edge-{source}{sourceHandle}-{target}{targetHandle}",
  "type": "bezier",
  "source": "nodeId",
  "target": "nodeId",
  "sourceHandle": "nodeId-output-1",
  "targetHandle": "nodeId-input-1",
  "updatable": true,
  "selectable": true,
  "data": {},
  "label": "",
  "markerEnd": "arrowclosed",
  "animated": false,
  "sourceX": 0, "sourceY": 0,
  "targetX": 0, "targetY": 0
}
```

Fallback edges add: `"style": "stroke: #ff6b6b"`

## DB Fields (apps table)

| Column | Format |
|--------|--------|
| id | MongoDB ObjectId (24 hex chars) |
| script | JSON string (not object) |
| createdAt/updatedAt | `YYYY-MM-DD HH:MM:SS.000 +00:00` |

## Key Lessons

1. **Edge handles**: conditions use `output-{id}` not `output-cond-{id}`
2. **Edge type**: must be `"bezier"` with `"markerEnd": "arrowclosed"`
3. **script column**: stores JSON as **string**, not nested object
4. **Cloud mode**: local DB changes get overwritten — need UI import or DevTools inject
5. **ID format**: MongoDB ObjectId (24 hex) not random strings

**Why:** Spent hours debugging why edges didn't render and imports failed
**How to apply:** When building GemLogin workflow JSON, use `output-{conditionId}` for conditions, ensure `type: bezier` and `markerEnd: arrowclosed` on every edge, insert script as JSON string in DB
