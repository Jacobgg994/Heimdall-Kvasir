import sqlite3
import json
import sys

db_path = r"C:\Users\Admin\.gemlogin\db.db"
script_id = "riM1BtDib4BtrGICKPzPe"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT script FROM apps WHERE id = ?", (script_id,))
row = cursor.fetchone()
script_json = json.loads(row[0])
params = script_json.get("trigger", {}).get("parameters", [])

# Build native blocks
new_nodes = [
    {
        "id": "trigger_node",
        "type": "BlockBasic",
        "position": {"x": 50, "y": 50},
        "data": {
            "icon": "riPlayLine",
            "type": "manual",
            "parameters": params
        },
        "label": "trigger"
    },
    {
        "id": "open_tiktok",
        "type": "BlockBasicWithFallback",
        "position": {"x": 300, "y": 50},
        "data": {
            "icon": "riLink",
            "url": "https://www.tiktok.com/upload?lang=en",
            "delay": "2000"
        },
        "label": "open-url"
    },
    {
        "id": "get_video_path",
        "type": "BlockBasicWithFallback",
        "position": {"x": 550, "y": 50},
        "data": {
            "icon": "riFileTextLine",
            "pathFolder": "{{video_source_path}}",
            "assignVariable": True,
            "variableName": "selected_video"
        },
        "label": "get-file-path"
    },
    {
        "id": "upload_video",
        "type": "BlockBasicWithFallback",
        "position": {"x": 800, "y": 50},
        "data": {
            "icon": "riFileUploadLine",
            "selector": "input[type='file']",
            "filePaths": ["{{variables.selected_video}}"],
            "delay": "5000"
        },
        "label": "upload-file"
    },
    {
        "id": "delay_for_processing",
        "type": "BlockDelay",
        "position": {"x": 1050, "y": 50},
        "data": {
            "icon": "riTimerLine",
            "time": "5000"
        },
        "label": "delay"
    },
    {
        "id": "type_description",
        "type": "BlockBasicWithFallback",
        "position": {"x": 1300, "y": 50},
        "data": {
            "icon": "riInputCursorMove",
            "selector": "//div[@contenteditable='true']",
            "findBy": "xpath",
            "value": "{{captions_file_path}} {{hashtags_file_path}}",
            "delay": "2000"
        },
        "label": "forms"
    },
    {
        "id": "click_post",
        "type": "BlockBasicWithFallback",
        "position": {"x": 1550, "y": 50},
        "data": {
            "icon": "riCursorLine",
            "selector": "//button[contains(., 'Post')]",
            "findBy": "xpath",
            "delay": "3000"
        },
        "label": "event-click"
    }
]

new_edges = [
    {"id": "e1", "source": "trigger_node", "target": "open_tiktok", "sourceHandle": "trigger_node-output-1", "targetHandle": "open_tiktok-input-1", "type": "bezier", "markerEnd": "arrowclosed"},
    {"id": "e2", "source": "open_tiktok", "target": "get_video_path", "sourceHandle": "open_tiktok-output-1", "targetHandle": "get_video_path-input-1", "type": "bezier", "markerEnd": "arrowclosed"},
    {"id": "e3", "source": "get_video_path", "target": "upload_video", "sourceHandle": "get_video_path-output-1", "targetHandle": "upload_video-input-1", "type": "bezier", "markerEnd": "arrowclosed"},
    {"id": "e4", "source": "upload_video", "target": "delay_for_processing", "sourceHandle": "upload_video-output-1", "targetHandle": "delay_for_processing-input-1", "type": "bezier", "markerEnd": "arrowclosed"},
    {"id": "e5", "source": "delay_for_processing", "target": "type_description", "sourceHandle": "delay_for_processing-output-1", "targetHandle": "type_description-input-1", "type": "bezier", "markerEnd": "arrowclosed"},
    {"id": "e6", "source": "type_description", "target": "click_post", "sourceHandle": "type_description-output-1", "targetHandle": "click_post-input-1", "type": "bezier", "markerEnd": "arrowclosed"}
]

script_json["drawflow"] = {
    "nodes": new_nodes,
    "edges": new_edges,
    "viewport": {"x": 0, "y": 0, "zoom": 0.8}
}

cursor.execute("UPDATE apps SET script = ? WHERE id = ?", (json.dumps(script_json, ensure_ascii=False), script_id))
conn.commit()
conn.close()
print("Converted to native GemLogin blocks successfully.")
