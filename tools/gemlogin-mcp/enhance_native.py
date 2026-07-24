import sqlite3
import json

db_path = r"C:\Users\Admin\.gemlogin\db.db"
script_id = "riM1BtDib4BtrGICKPzPe"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT script FROM apps WHERE id = ?", (script_id,))
row = cursor.fetchone()
script_json = json.loads(row[0])
params = script_json.get("trigger", {}).get("parameters", [])

# Enhanced Native Blocks with Conditions
new_nodes = [
    {
        "id": "trigger_node",
        "type": "BlockBasic",
        "position": {"x": 0, "y": 200},
        "data": { "icon": "riPlayLine", "type": "manual", "parameters": params },
        "label": "trigger"
    },
    {
        "id": "open_tiktok",
        "type": "BlockBasicWithFallback",
        "position": {"x": 250, "y": 200},
        "data": { "icon": "riLink", "url": "https://www.tiktok.com/upload?lang=en", "delay": "3000" },
        "label": "open-url"
    },
    {
        "id": "check_login",
        "type": "BlockConditions",
        "position": {"x": 500, "y": 200},
        "data": {
            "icon": "riAB",
            "conditions": [
                {
                    "id": "c1",
                    "name": "Not Logged In",
                    "conditions": [
                        {
                            "id": "sub1",
                            "conditions": [
                                {
                                    "id": "item1",
                                    "items": [{"type": "element#exists", "category": "value", "data": {"selector": "//button[contains(., 'Log in')]"}, "id": "check_login_btn"}]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        "label": "conditions"
    },
    {
        "id": "get_video_path",
        "type": "BlockBasicWithFallback",
        "position": {"x": 750, "y": 300},
        "data": { "icon": "riFileTextLine", "pathFolder": "{{video_source_path}}", "assignVariable": True, "variableName": "selected_video" },
        "label": "get-file-path"
    },
    {
        "id": "upload_video",
        "type": "BlockBasicWithFallback",
        "position": {"x": 1000, "y": 300},
        "data": { "icon": "riFileUploadLine", "selector": "input[type='file']", "filePaths": ["{{variables.selected_video}}"], "delay": "5000" },
        "label": "upload-file"
    },
    {
        "id": "wait_for_editor",
        "type": "BlockBasicWithFallback",
        "position": {"x": 1250, "y": 300},
        "data": { "icon": "riFocus3Line", "findBy": "xpath", "selector": "//div[@contenteditable='true']", "timeout": "60000" },
        "label": "element-exists"
    },
    {
        "id": "type_description",
        "type": "BlockBasicWithFallback",
        "position": {"x": 1500, "y": 300},
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
        "id": "wait_post_btn",
        "type": "BlockDelay",
        "position": {"x": 1750, "y": 300},
        "data": { "icon": "riTimerLine", "time": "7000" },
        "label": "delay"
    },
    {
        "id": "click_post",
        "type": "BlockBasicWithFallback",
        "position": {"x": 2000, "y": 300},
        "data": {
            "icon": "riCursorLine",
            "selector": "//button[contains(., 'Post')]",
            "findBy": "xpath",
            "delay": "3000"
        },
        "label": "event-click"
    },
    {
        "id": "error_login",
        "type": "BlockBasicWithFallback",
        "position": {"x": 750, "y": 100},
        "data": { "icon": "riErrorWarningLine", "description": "Please login to TikTok first!" },
        "label": "log-data"
    }
]

new_edges = [
    {"id": "e1", "source": "trigger_node", "target": "open_tiktok", "sourceHandle": "trigger_node-output-1", "targetHandle": "open_tiktok-input-1", "type": "bezier", "markerEnd": "arrowclosed"},
    {"id": "e2", "source": "open_tiktok", "target": "check_login", "sourceHandle": "open_tiktok-output-1", "targetHandle": "check_login-input-1", "type": "bezier", "markerEnd": "arrowclosed"},
    # Condition: If NOT logged in (c1) -> error_login
    {"id": "e3_err", "source": "check_login", "target": "error_login", "sourceHandle": "check_login-output-c1", "targetHandle": "error_login-input-1", "type": "bezier", "markerEnd": "arrowclosed", "style": "stroke: #ff6b6b"},
    # Condition: Default (fallback) -> get_video_path
    {"id": "e3_ok", "source": "check_login", "target": "get_video_path", "sourceHandle": "check_login-output-fallback", "targetHandle": "get_video_path-input-1", "type": "bezier", "markerEnd": "arrowclosed"},
    {"id": "e4", "source": "get_video_path", "target": "upload_video", "sourceHandle": "get_video_path-output-1", "targetHandle": "upload_video-input-1", "type": "bezier", "markerEnd": "arrowclosed"},
    {"id": "e5", "source": "upload_video", "target": "wait_for_editor", "sourceHandle": "upload_video-output-1", "targetHandle": "wait_for_editor-input-1", "type": "bezier", "markerEnd": "arrowclosed"},
    {"id": "e6", "source": "wait_for_editor", "target": "type_description", "sourceHandle": "wait_for_editor-output-1", "targetHandle": "type_description-input-1", "type": "bezier", "markerEnd": "arrowclosed"},
    {"id": "e7", "source": "type_description", "target": "wait_post_btn", "sourceHandle": "type_description-output-1", "targetHandle": "wait_post_btn-input-1", "type": "bezier", "markerEnd": "arrowclosed"},
    {"id": "e8", "source": "wait_post_btn", "target": "click_post", "sourceHandle": "wait_post_btn-output-1", "targetHandle": "click_post-input-1", "type": "bezier", "markerEnd": "arrowclosed"}
]

script_json["drawflow"] = {
    "nodes": new_nodes,
    "edges": new_edges,
    "viewport": {"x": 0, "y": 0, "zoom": 0.6}
}

cursor.execute("UPDATE apps SET script = ? WHERE id = ?", (json.dumps(script_json, ensure_ascii=False), script_id))
conn.commit()
conn.close()
print("Enhanced native script with conditions successfully.")
