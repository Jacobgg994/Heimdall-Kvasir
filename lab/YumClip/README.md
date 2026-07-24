# 🍜 YumClip — ยำรวมคลิป

สุ่มคลิปวิดีโอจากโฟลเดอร์ มายำรวมกันเป็นคลิปใหม่ตามจำนวนและความยาวที่ต้องการ

## 🔧 Requirements

- **Python 3.10+** → [python.org](https://www.python.org/downloads/)
- **ffmpeg + ffprobe** → [ffmpeg.org](https://ffmpeg.org/download.html)
  - หรือ `winget install ffmpeg` (Windows)

## 🚀 วิธีใช้

### แบบ GUI

ดับเบิลคลิก `run.bat` หรือรัน:

```cmd
python yumclip.py --gui
```

### แบบ CLI

```cmd
python yumclip.py "D:\My Videos" -d 30 -n 5 -r -t 2 --res 1920x1080
```

## 📋 ตัวเลือกทั้งหมด

| Flag | คำอธิบาย | Default |
|---|---|---|
| `folder` | โฟลเดอร์ต้นทาง | — |
| `-d, --min-duration` | ความยาวขั้นต่ำต่อคลิปผลลัพธ์ (วินาที) | `20` |
| `-n, --num-outputs` | จำนวนคลิปที่ต้องการ | `5` |
| `-o, --output` | โฟลเดอร์ปลายทาง | `<source>/YumClip_Output` |
| `-u, --used-folder` | โฟลเดอร์เก็บคลิปที่ใช้แล้ว (กันซ้ำ) | `<source>/YumClip_Used` |
| `--max-overage` | จำกัดไม่ให้ยาวเกินไป (วินาที) | `20% ของ min_duration` |
| `--move-used` | **ย้าย** แทน copy ไป used folder | `False` (copy) |
| `-t, --threads` | จำนวน CPU threads (`2-4` สำหรับคอมไม่แรง) | `0` (auto) |
| `-r, --recursive` | สแกนโฟลเดอร์ย่อยด้วย | `False` |
| `--res` | บังคับความละเอียด เช่น `1920x1080` หรือ `1080` | ไม่บังคับ |
| `--no-audio` | ตัดเสียงออก | `False` |
| `--audio-only` | เอาแต่เสียง ตัดวิดีโอ | `False` |
| `--gui` | เปิด GUI | — |

## 📂 ตัวอย่าง

```
D:\My Videos\
├── cat01.mp4         (12s)
├── cat02.mp4         (8s)
├── dog01.mp4         (15s)
├── meme01.mp4        (5s)
├── meme02.mp4        (7s)
├── subfolder\
│   └── hidden.mp4    (10s)
```

```cmd
# ปกติ
python yumclip.py "D:\My Videos" -d 20 -n 3

# สแกนโฟลเดอร์ย่อย + จำกัด threads + บังคับ 1080p
python yumclip.py "D:\My Videos" -r -t 2 --res 1920x1080

# ตัดเสียง + ย้ายคลิปต้นทางไป used folder
python yumclip.py "D:\My Videos" --no-audio --move-used
```

ผลลัพธ์:
```
D:\My Videos\YumClip_Output\
├── cat playing toys fun dog.mp4     ← รวม 3 คลิป 25s
├── meme funny moment out.mp4        ← รวม 4 คลิป 23s
└── dog outdoor running.mp4          ← รวม 2 คลิป 21s

D:\My Videos\YumClip_Used\
├── cat01.mp4    ← copy คลิปที่ใช้แล้ว
├── dog01.mp4
└── ...
```

## 🖥 GUI

```
┌────────────────────────────────────────┐
│  🍜 YumClip — ยำรวมคลิป               │
│                                        │
│  📁 โฟลเดอร์ต้นทาง             [Browse…]│
│  📂 โฟลเดอร์ปลายทาง            [Browse…]│
│  ⏱  ความยาวขั้นต่ำต่อคลิป               │
│  🎬 จำนวนคลิปที่ต้องการ                │
│  🧵 Threads                            │
│  📐 ความละเอียด                        │
│  🗂  โฟลเดอร์เก็บคลิปที่ใช้แล้ว  [Browse…]│
│  📁 สแกนโฟลเดอร์ย่อยด้วย ☐             │
│  📦 ย้ายคลิปไปโฟลเดอร์ใช้แล้ว ☐         │
│  🔇 ไม่มีเสียง ☐                        │
│  🎵 เอาแต่เสียง ☐                       │
│  ═══════════█░░░░═══════ 2/5           │
│  กำลังยำคลิปที่ 2/5…                   │
│  [      🍜 เริ่มยำคลิป!      ]         │
└────────────────────────────────────────┘
```

## ⚠️ Note

- ไฟล์ต้นฉบับ **ไม่ถูกแก้ไขหรือลบ** (ยกเว้นใช้ `--move-used`)
- stream-copy เร็วมากเพราะไม่ encode ใหม่ — แต่ทุกคลิปต้อง codec เดียวกัน
- ถ้า codec ไม่ตรงกัน จะ fallback ไป re-encode H.264
- `--res` / `--no-audio` / `--audio-only` จะบังคับ re-encode ทันที
