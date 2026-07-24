import sqlite3
import json
import random
import string
import os

db_path = r"C:\Users\Admin\.gemlogin\db.db"
js_file = r"D:\Owen\Lab\gemlogin-mcp\fb_review_script.js"

# ตรวจสอบการมีอยู่ของไฟล์ JavaScript
if not os.path.exists(js_file):
    print(f"Error: {js_file} not found")
    exit(1)

with open(js_file, 'r', encoding='utf-8') as f:
    js_code = f.read()

# ตั้งค่าชื่อสคริปต์และสร้าง ID แบบสุ่ม 21 ตัวอักษร
script_name = "Facebook Page Auto Review (Gemini AI)"
new_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(21))

# สร้างพารามิเตอร์สำหรับ UI
params = [
    {
        "id": "gemini_key",
        "name": "gemini_api_key",
        "label": "Gemini API Key",
        "type": "string",
        "description": "ระบุ API Key ของ Gemini สำหรับสร้างเนื้อหารีวิว",
        "defaultValue": "",
        "placeholder": "AIzaSy..."
    },
    {
        "id": "pages_file",
        "name": "fb_pages_file",
        "label": "Facebook Pages File (.txt)",
        "type": "filepath",
        "description": "ไฟล์ Text เก็บลิสต์ Facebook Page URL/Username (บรรทัดละ 1 เพจ)",
        "defaultValue": "",
        "placeholder": "C:\\Users\\Admin\\Downloads\\fb_pages.txt"
    },
    {
        "id": "instructions",
        "name": "review_instructions",
        "label": "Review Style / Instructions",
        "type": "string",
        "description": "ระบุทิศทาง คำอธิบายเพจ หรือสไตล์การเขียนของ AI",
        "defaultValue": "รีวิวชื่นชมร้านค้า บริการรวดเร็ว พนักงานดีเยี่ยม บรรยากาศเป็นกันเอง",
        "placeholder": "รีวิวเชิงบวก ให้ข้อมูลน่าสนใจและสุภาพ"
    },
    {
        "id": "temp_val",
        "name": "temperature",
        "label": "Creativity (Temperature 0.1 - 1.0)",
        "type": "string",
        "description": "ค่าความสร้างสรรค์ของ AI (ค่าเริ่มต้น 0.8)",
        "defaultValue": "0.8",
        "placeholder": "0.8"
    }
]

# สร้าง Flow Schema สำหรับ GemLogin
new_drawflow = {
    "nodes": [
        {
            "id": "trigger_node",
            "type": "BlockBasic",
            "initialized": False,
            "position": {"x": 50, "y": 100},
            "data": {
                "icon": "riPlayLine",
                "disableBlock": False,
                "description": "รันสคริปต์รีวิวเฟสบุ๊คแบบอัตโนมัติด้วย AI",
                "type": "manual",
                "parameters": params
            },
            "label": "trigger"
        },
        {
            "id": "js_code_block",
            "type": "BlockBasicWithFallback",
            "initialized": False,
            "position": {"x": 350, "y": 100},
            "data": {
                "icon": "riCodeSSlashLine",
                "disableBlock": False,
                "description": "รันรีวิวบน Facebook หน้าปัจจุบัน",
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
            "source": "trigger_node",
            "target": "js_code_block",
            "sourceHandle": "trigger_node-output-1",
            "targetHandle": "js_code_block-input-1",
            "type": "bezier",
            "markerEnd": "arrowclosed"
        }
    ],
    "viewport": {"x": 0, "y": 0, "zoom": 1}
}

script_json = {
    "id": new_id,
    "name": script_name,
    "icon": "riFacebookCircleLine",
    "drawflow": new_drawflow,
    "trigger": { "parameters": params },
    "version": "1.0.0"
}

# เชื่อมต่อ SQLite Database และบันทึกข้อมูล
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# ตรวจสอบว่าเคยมีชื่อสคริปต์ซ้ำกันไหม ถ้ามีให้ลบตัวเก่าก่อนเพื่อให้รันได้ลื่นไหล
cursor.execute("SELECT id FROM apps WHERE name = ?", (script_name,))
exists = cursor.fetchone()

if exists:
    cursor.execute("DELETE FROM apps WHERE name = ?", (script_name,))
    print(f"[DB] Old script removed.")

cursor.execute(
    "INSERT INTO apps (id, name, version, script, type, createdAt, updatedAt) VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'))",
    (new_id, script_name, "1.0.0", json.dumps(script_json, ensure_ascii=False), "local")
)

conn.commit()
conn.close()

print(f"[SUCCESS] Created script '{script_name}' in GemLogin Database!")
print(f"Script ID: {new_id}")
