import sqlite3
import json
import random
import string
import os

db_path = r"C:\Users\Admin\.gemlogin\db.db"
js_file = "yt_booster_logic.js"

def gen_id(length=21):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

with open(js_file, 'r', encoding='utf-8') as f:
    js_code = f.read()

new_id = gen_id()
script_name = "YouTube View Booster Elite"

params = [
    {"id": "p1", "name": "target_urls", "label": "YouTube URLs / Search Keywords", "type": "string", "description": "One per line", "defaultValue": "", "placeholder": "Enter URLs or Keywords"},
    {"id": "p2", "name": "min_watch_sec", "label": "Minimum Watch Time (sec)", "type": "number", "description": "", "defaultValue": "60", "placeholder": "60"},
    {"id": "p3", "name": "max_watch_sec", "label": "Maximum Watch Time (sec)", "type": "number", "description": "", "defaultValue": "180", "placeholder": "180"},
    {"id": "p4", "name": "interaction_rate", "label": "Interaction Chance (%)", "type": "number", "description": "Like/Sub chance", "defaultValue": "20", "placeholder": "20"},
    {"id": "p5", "name": "search_mode", "label": "Enable Search-First Mode", "type": "checkbox", "description": "Search on YT instead of direct link", "defaultValue": True, "placeholder": ""}
]

script_json = {
    "id": new_id,
    "name": script_name,
    "icon": "riYoutubeLine",
    "folderId": "",
    "content": None,
    "connectedTable": None,
    "drawflow": {
        "nodes": [
            {
                "id": "trigger_node",
                "type": "BlockBasic",
                "data": {
                    "icon": "riPlayLine",
                    "type": "manual",
                    "parameters": params
                },
                "label": "trigger",
                "position": {"x": 0, "y": 0}
            },
            {
                "id": "js_node",
                "type": "BlockBasicWithFallback",
                "data": {
                    "icon": "riCodeSSlashLine",
                    "code": js_code,
                    "timeout": "600000",
                    "context": "website"
                },
                "label": "javascript-code",
                "position": {"x": 300, "y": 0}
            }
        ],
        "edges": [
            {
                "id": "e1",
                "source": "trigger_node",
                "target": "js_node",
                "sourceHandle": "trigger_node-output-1",
                "targetHandle": "js_node-input-1",
                "type": "bezier",
                "markerEnd": "arrowclosed"
            }
        ],
        "viewport": {"x": 50, "y": 50, "zoom": 1}
    },
    "trigger": {
        "parameters": params
    },
    "version": "1.0.0",
    "createdAt": 1779526000000,
    "updatedAt": 1779526000000
}

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# columns: id, user_id, name, description, version, script, table, input, enabale_input, metadata, expired_at, type, createdAt, updatedAt
cursor.execute(
    "INSERT INTO apps (id, name, version, script, type, createdAt, updatedAt) VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'))",
    (new_id, script_name, "1.0.0", json.dumps(script_json, ensure_ascii=False), "local")
)

conn.commit()
conn.close()

print(f"Successfully created new script: {script_name} (ID: {new_id})")
