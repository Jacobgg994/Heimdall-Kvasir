import sqlite3
import json
import sys
import os

db_path = r"C:\Users\Admin\.gemlogin\db.db"
script_id = "riM1BtDib4BtrGICKPzPe"
js_file = "tiktok_script.js"

if not os.path.exists(js_file):
    print(f"Error: {js_file} not found")
    sys.exit(1)

with open(js_file, 'r', encoding='utf-8') as f:
    js_code = f.read()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Fetch current script JSON
cursor.execute("SELECT script FROM apps WHERE id = ?", (script_id,))
row = cursor.fetchone()
if not row:
    print(f"Error: Script {script_id} not found in database")
    sys.exit(1)

script_json = json.loads(row[0])

# 2. Update the drawflow to a minimal one with one JS block
# We keep the original parameters but replace the nodes
params = script_json.get("trigger", {}).get("parameters", [])

new_drawflow = {
    "nodes": [
        {
            "id": "Yjr1MoQRgKQkMFtjfiDOH",
            "type": "BlockBasic",
            "initialized": False,
            "position": {"x": 0, "y": 0},
            "data": {
                "icon": "riPlayLine",
                "disableBlock": False,
                "description": "",
                "type": "manual",
                "parameters": params
            },
            "label": "trigger"
        },
        {
            "id": "js_code_block",
            "type": "BlockBasicWithFallback",
            "initialized": False,
            "position": {"x": 300, "y": 0},
            "data": {
                "icon": "riCodeSSlashLine",
                "disableBlock": False,
                "description": "Professional TikTok Poster",
                "timeout": "300000",
                "context": "website",
                "code": js_code,
                "preloadScripts": [],
                "everyNewTab": False,
                "runBeforeLoad": False,
                "delay": 0
            },
            "label": "javascript-code"
        }
    ],
    "edges": [
        {
            "id": "edge_1",
            "source": "Yjr1MoQRgKQkMFtjfiDOH",
            "target": "js_code_block",
            "sourceHandle": "Yjr1MoQRgKQkMFtjfiDOH-output-1",
            "targetHandle": "js_code_block-input-1",
            "type": "bezier",
            "markerEnd": "arrowclosed"
        }
    ],
    "viewport": {"x": 0, "y": 0, "zoom": 1}
}

script_json["drawflow"] = new_drawflow
# Also update trigger parameters just in case
script_json["trigger"]["parameters"] = params

new_script_str = json.dumps(script_json, ensure_ascii=False)

# 3. Update database
cursor.execute("UPDATE apps SET script = ? WHERE id = ?", (new_script_str, script_id))
conn.commit()
conn.close()

print(f"Successfully updated script {script_id} in database.")
