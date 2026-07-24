import sqlite3
import json
import random
import string

db_path = r"C:\Users\Admin\.gemlogin\db.db"
new_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(21))
script_name = "FB Smart Scheduler (Matrix Edition)"

params = [
    {"id": "c1", "name": "category", "label": "Category", "type": "string", "description": "Select: UFABRO, FOOTBALL, SLOT, CASINO", "defaultValue": "SLOT", "placeholder": "Category Name"},
    {"id": "r1", "name": "round", "label": "Post Round", "type": "string", "description": "Select: 1st, 2nd, 3rd", "defaultValue": "1st", "placeholder": "1st, 2nd or 3rd"},
    {"id": "m1", "name": "media_folder", "label": "Media Root Folder", "type": "string", "description": "Folder containing subfolders for each category", "defaultValue": "", "placeholder": "C:\\Media"},
    {"id": "cp1", "name": "caption_file", "label": "Caption Source (.txt)", "type": "filepath", "description": "", "defaultValue": "", "placeholder": "Select file"},
    {"id": "pg1", "name": "pages_list", "label": "Target Pages (.txt)", "type": "filepath", "description": "List of Page IDs or URLs", "defaultValue": "", "placeholder": "Select file"}
]

# Mapping the Matrix from Image
# UFABRO: 1st:1P, 2nd:1P, 3rd:1V
# FOOTBALL: 1st:1P, 2nd:1P, 3rd:1V
# SLOT: 1st:2P+1V, 2nd:2P+1V, 3rd:2P+1V
# CASINO: 1st:1P, 2nd:1P, 3rd:1V

# For the sake of a "Detailed Native Script", I will use a JS block to calculate the count 
# to avoid 12 branches of native conditions which would be unreadable. 
# BUT I will use native blocks for all browser actions as requested.

js_calc_logic = """
const cat = category.toUpperCase();
const rnd = round.toLowerCase();
let photos = 0;
let videos = 0;

if (cat === 'SLOT') {
    photos = 2;
    videos = 1;
} else if (rnd === '3rd') {
    photos = 0;
    videos = 1;
} else {
    photos = 1;
    videos = 0;
}

SetVariable('target_photos', photos);
SetVariable('target_videos', videos);
console.log(`[Matrix] Category: ${cat}, Round: ${rnd} -> Photos: ${photos}, Videos: ${videos}`);
"""

new_nodes = [
    {
        "id": "start",
        "type": "BlockBasic",
        "position": {"x": 0, "y": 0},
        "data": { "icon": "riPlayLine", "type": "manual", "parameters": params },
        "label": "trigger"
    },
    {
        "id": "logic_calc",
        "type": "BlockBasicWithFallback",
        "position": {"x": 250, "y": 0},
        "data": { "icon": "riCodeSSlashLine", "code": js_calc_logic, "description": "Matrix Logic Calculator" },
        "label": "javascript-code"
    },
    {
        "id": "loop_pages",
        "type": "BlockRepeatTask",
        "position": {"x": 500, "y": 0},
        "data": { "icon": "riRepeat2Line", "repeatFor": "5" }, # Example: 5 accounts
        "label": "repeat-task"
    },
    {
        "id": "open_fb_page",
        "type": "BlockBasicWithFallback",
        "position": {"x": 750, "y": 0},
        "data": { "icon": "riLink", "url": "https://www.facebook.com/me", "delay": "3000" },
        "label": "open-url"
    },
    {
        "id": "click_create_post",
        "type": "BlockBasicWithFallback",
        "position": {"x": 1000, "y": 0},
        "data": { "icon": "riCursorLine", "selector": "//span[text()='Photo/video']", "findBy": "xpath" },
        "label": "event-click"
    },
    {
        "id": "upload_media",
        "type": "BlockBasicWithFallback",
        "position": {"x": 1250, "y": 0},
        "data": { 
            "icon": "riFileUploadLine", 
            "selector": "input[type='file']", 
            "filePaths": ["{{media_folder}}"], 
            "delay": "5000" 
        },
        "label": "upload-file"
    },
    {
        "id": "type_caption",
        "type": "BlockBasicWithFallback",
        "position": {"x": 1500, "y": 0},
        "data": { 
            "icon": "riInputCursorMove", 
            "selector": "div[aria-label^='What\\'s on your mind']", 
            "value": "{{caption_file}}",
            "delay": "2000"
        },
        "label": "forms"
    },
    {
        "id": "click_post",
        "type": "BlockBasicWithFallback",
        "position": {"x": 1750, "y": 0},
        "data": { "icon": "riCursorLine", "selector": "//div[@aria-label='Post']", "findBy": "xpath" },
        "label": "event-click"
    }
]

new_edges = [
    {"id": "e1", "source": "start", "target": "logic_calc", "sourceHandle": "start-output-1", "targetHandle": "logic_calc-input-1", "type": "bezier", "markerEnd": "arrowclosed"},
    {"id": "e2", "source": "logic_calc", "target": "loop_pages", "sourceHandle": "logic_calc-output-1", "targetHandle": "loop_pages-input-1", "type": "bezier", "markerEnd": "arrowclosed"},
    {"id": "e3", "source": "loop_pages", "target": "open_fb_page", "sourceHandle": "loop_pages-output-1", "targetHandle": "open_fb_page-input-1", "type": "bezier", "markerEnd": "arrowclosed"},
    {"id": "e4", "source": "open_fb_page", "target": "click_create_post", "sourceHandle": "open_fb_page-output-1", "targetHandle": "click_create_post-input-1", "type": "bezier", "markerEnd": "arrowclosed"},
    {"id": "e5", "source": "click_create_post", "target": "upload_media", "sourceHandle": "click_create_post-output-1", "targetHandle": "upload_media-input-1", "type": "bezier", "markerEnd": "arrowclosed"},
    {"id": "e6", "source": "upload_media", "target": "type_caption", "sourceHandle": "upload_media-output-1", "targetHandle": "type_description-input-1", "type": "bezier", "markerEnd": "arrowclosed"},
    {"id": "e7", "source": "type_caption", "target": "click_post", "sourceHandle": "type_caption-output-1", "targetHandle": "click_post-input-1", "type": "bezier", "markerEnd": "arrowclosed"}
]

script_json = {
    "id": new_id,
    "name": script_name,
    "icon": "riFacebookCircleLine",
    "drawflow": {
        "nodes": new_nodes,
        "edges": new_edges,
        "viewport": {"x": 0, "y": 100, "zoom": 0.7}
    },
    "trigger": { "parameters": params },
    "version": "1.0.0"
}

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute(
    "INSERT INTO apps (id, name, version, script, type, createdAt, updatedAt) VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'))",
    (new_id, script_name, "1.0.0", json.dumps(script_json, ensure_ascii=False), "local")
)
conn.commit()
conn.close()
print(f"Successfully created complex matrix script: {script_name}")
