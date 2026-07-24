#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChangNameVideo - โปรแกรมเปลี่ยนชื่อวิดีโอแบบสุ่ม
Random Video Renamer with hashtag support
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import random
import threading

class ChangNameVideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ChangNameVideo - เปลี่ยนชื่อวิดีโอแบบสุ่ม")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)

        # ตัวแปรเก็บข้อมูล
        self.video_files = []       # list of (full_path, ext)
        self.preview_names = []     # ชื่อตัวอย่างที่แสดงก่อนกดเริ่ม

        # === Style ===
        style = ttk.Style()
        style.theme_use('clam')

        # === Main Frame ===
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ========== ROW 0: เลือกโฟลเดอร์วิดีโอ ==========
        row0 = ttk.Frame(main_frame)
        row0.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(row0, text="📁 วิดีโอที่ต้องการเปลี่ยนชื่อ:", font=("", 10, "bold")).pack(anchor=tk.W)

        btn_frame = ttk.Frame(row0)
        btn_frame.pack(fill=tk.X, pady=5)

        self.btn_select = ttk.Button(btn_frame, text="📂 เลือกไฟล์วิดีโอ", command=self.select_videos)
        self.btn_select.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_select_folder = ttk.Button(btn_frame, text="📁 เลือกทั้งโฟลเดอร์", command=self.select_folder)
        self.btn_select_folder.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_clear_files = ttk.Button(btn_frame, text="🗑️ ล้างรายการ", command=self.clear_videos)
        self.btn_clear_files.pack(side=tk.LEFT)

        # รายการไฟล์วิดีโอ
        self.file_listbox = tk.Listbox(main_frame, height=5, selectmode=tk.EXTENDED)
        self.file_listbox.pack(fill=tk.X, pady=(0, 10))

        self.lbl_file_count = ttk.Label(main_frame, text="จำนวน: 0 ไฟล์")
        self.lbl_file_count.pack(anchor=tk.W, pady=(0, 10))

        # ========== ROW 1: ชื่อวิดีโอ + แฮชแท็ก ==========
        panel = ttk.Frame(main_frame)
        panel.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # --- คอลัมน์ซ้าย: ชื่อวิดีโอ ---
        left_col = ttk.LabelFrame(panel, text="🎬 ชื่อวิดีโอ (1 ชื่อต่อ 1 บรรทัด)", padding="5")
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.name_text = scrolledtext.ScrolledText(left_col, height=8, font=("", 10))
        self.name_text.pack(fill=tk.BOTH, expand=True)
        # ใส่ตัวอย่าง
        self.name_text.insert(tk.END, "คลิปตลก\nเต้น cover\nรีวิวอาหาร\nสอนแต่งหน้า\n")

        # --- คอลัมน์ขวา: แฮชแท็ก ---
        right_col = ttk.LabelFrame(panel, text="🏷️ แฮชแท็ก (1 แฮชแท็กต่อ 1 บรรทัด, ใส่หรือไม่ใส่ # ก็ได้)", padding="5")
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.hashtag_text = scrolledtext.ScrolledText(right_col, height=8, font=("", 10))
        self.hashtag_text.pack(fill=tk.BOTH, expand=True)
        # ใส่ตัวอย่าง
        self.hashtag_text.insert(tk.END, "#ตลก\n#coverdance\n#รีวิว\n#beauty\n#ไวรัล\n#มาแรง\n#tiktok\n#youtube\n")

        # ========== ROW 2: ตัวเลือก ==========
        option_frame = ttk.LabelFrame(main_frame, text="⚙️ ตัวเลือก", padding="5")
        option_frame.pack(fill=tk.X, pady=(0, 10))

        opt_row1 = ttk.Frame(option_frame)
        opt_row1.pack(fill=tk.X, pady=2)

        ttk.Label(opt_row1, text="จำนวนแฮชแท็กต่อวิดีโอ:").pack(side=tk.LEFT)
        self.hashtag_count = tk.IntVar(value=3)
        self.spin_hashtag = ttk.Spinbox(opt_row1, from_=1, to=5, textvariable=self.hashtag_count, width=5)
        self.spin_hashtag.pack(side=tk.LEFT, padx=5)

        ttk.Label(opt_row1, text="คั่นด้วย:").pack(side=tk.LEFT, padx=(20, 0))
        self.separator = tk.StringVar(value=" ")
        self.combo_sep = ttk.Combobox(opt_row1, textvariable=self.separator,
                                       values=[" ", "_", "-", " | ", " · "], width=5)
        self.combo_sep.pack(side=tk.LEFT, padx=5)

        ttk.Label(opt_row1, text="ตำแหน่งแฮชแท็ก:").pack(side=tk.LEFT, padx=(20, 0))
        self.tag_position = tk.StringVar(value="ท้ายชื่อ")
        self.combo_pos = ttk.Combobox(opt_row1, textvariable=self.tag_position,
                                       values=["ท้ายชื่อ", "หน้าชื่อ"], width=10)
        self.combo_pos.pack(side=tk.LEFT, padx=5)

        opt_row2 = ttk.Frame(option_frame)
        opt_row2.pack(fill=tk.X, pady=2)

        self.shuffle_names = tk.BooleanVar(value=True)
        ttk.Checkbutton(opt_row2, text="สุ่มลำดับชื่อวิดีโอ", variable=self.shuffle_names).pack(side=tk.LEFT, padx=(0, 15))

        self.shuffle_tags = tk.BooleanVar(value=True)
        ttk.Checkbutton(opt_row2, text="สุ่มแฮชแท็ก", variable=self.shuffle_tags).pack(side=tk.LEFT, padx=(0, 15))

        self.keep_ext = tk.BooleanVar(value=True)
        ttk.Checkbutton(opt_row2, text="คงนามสกุลไฟล์เดิม", variable=self.keep_ext).pack(side=tk.LEFT)

        # ========== ROW 3: ปุ่มพรีวิว + เริ่ม ==========
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(0, 10))

        self.btn_preview = ttk.Button(action_frame, text="👁️ พรีวิวชื่อใหม่", command=self.preview_names_fn)
        self.btn_preview.pack(side=tk.LEFT, padx=(0, 10))

        self.btn_rename = ttk.Button(action_frame, text="🚀 เริ่มเปลี่ยนชื่อ!", command=self.start_rename)
        self.btn_rename.pack(side=tk.LEFT, padx=(0, 10))

        # Progress bar
        self.progress = ttk.Progressbar(action_frame, mode='determinate', length=200)
        self.progress.pack(side=tk.LEFT, padx=10)

        # ========== ROW 4: พื้นที่พรีวิว ==========
        preview_frame = ttk.LabelFrame(main_frame, text="📋 ผลลัพธ์", padding="5")
        preview_frame.pack(fill=tk.BOTH, expand=True)

        self.preview_text = scrolledtext.ScrolledText(preview_frame, height=8, font=("Consolas", 9))
        self.preview_text.pack(fill=tk.BOTH, expand=True)

        # ========== Status Bar ==========
        self.status_var = tk.StringVar(value="พร้อมทำงาน ► เลือกไฟล์วิดีโอ + ใส่ชื่อ + ใส่แฮชแท็ก → กดเริ่ม")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding=5)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    # ============================================================
    #  METHODS
    # ============================================================

    def select_videos(self):
        """เลือกไฟล์วิดีโอหลายไฟล์"""
        files = filedialog.askopenfilenames(
            title="เลือกไฟล์วิดีโอ",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.m4v *.mpg *.mpeg *.3gp"),
                ("All files", "*.*")
            ]
        )
        if files:
            self.video_files = [(f, os.path.splitext(f)[1]) for f in files]
            self.refresh_file_list()
            self.status_var.set(f"เลือกแล้ว {len(self.video_files)} ไฟล์")

    def select_folder(self):
        """เลือกทั้งโฟลเดอร์"""
        folder = filedialog.askdirectory(title="เลือกโฟลเดอร์ที่มีวิดีโอ")
        if folder:
            video_exts = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', '.3gp'}
            files = []
            for f in os.listdir(folder):
                full = os.path.join(folder, f)
                if os.path.isfile(full) and os.path.splitext(f)[1].lower() in video_exts:
                    files.append((full, os.path.splitext(f)[1]))
            if files:
                self.video_files = files
                self.refresh_file_list()
                self.status_var.set(f"เลือกแล้ว {len(self.video_files)} ไฟล์ จาก {folder}")
            else:
                messagebox.showwarning("ไม่พบไฟล์", "ไม่พบไฟล์วิดีโอในโฟลเดอร์นี้")

    def clear_videos(self):
        """ล้างรายการวิดีโอ"""
        self.video_files.clear()
        self.file_listbox.delete(0, tk.END)
        self.lbl_file_count.config(text="จำนวน: 0 ไฟล์")
        self.preview_text.delete(1.0, tk.END)
        self.status_var.set("ล้างรายการแล้ว ► เลือกไฟล์วิดีโอใหม่")

    def refresh_file_list(self):
        """อัปเดตรายการไฟล์ใน listbox"""
        self.file_listbox.delete(0, tk.END)
        for fpath, ext in self.video_files:
            self.file_listbox.insert(tk.END, f"  {os.path.basename(fpath)}")
        self.lbl_file_count.config(text=f"จำนวน: {len(self.video_files)} ไฟล์")

    def get_names(self):
        """อ่านชื่อจาก text area"""
        raw = self.name_text.get(1.0, tk.END).strip()
        return [n.strip() for n in raw.splitlines() if n.strip()]

    def get_hashtags(self):
        """อ่านแฮชแท็กจาก text area (ใส่ # ให้อัตโนมัติถ้ายังไม่มี)"""
        raw = self.hashtag_text.get(1.0, tk.END).strip()
        tags = [t.strip() for t in raw.splitlines() if t.strip()]
        # เติม # ถ้ายังไม่มี
        return [t if t.startswith("#") else f"#{t}" for t in tags]

    def generate_new_names(self):
        """สร้างชื่อใหม่จาก names + hashtags (ยังไม่ลงไฟล์)"""
        names = self.get_names()
        tags = self.get_hashtags()

        if not names:
            return [], "❌ กรุณาใส่ชื่อวิดีโออย่างน้อย 1 ชื่อ"
        if not tags:
            return [], "❌ กรุณาใส่แฮชแท็กอย่างน้อย 1 อัน"
        if not self.video_files:
            return [], "❌ กรุณาเลือกไฟล์วิดีโอก่อน"

        num_tags = self.hashtag_count.get()
        sep = self.separator.get()
        tag_pos = self.tag_position.get()

        # เตรียมชื่อให้พอ
        working_names = names.copy()
        if self.shuffle_names.get():
            random.shuffle(working_names)

        # วนชื่อถ้าไม่พอ
        while len(working_names) < len(self.video_files):
            extra = names.copy()
            if self.shuffle_names.get():
                random.shuffle(extra)
            working_names.extend(extra)
        working_names = working_names[:len(self.video_files)]

        results = []
        for i, (fpath, ext) in enumerate(self.video_files):
            name = working_names[i]
            chosen_tags = self._pick_tags(tags, num_tags)

            if tag_pos == "หน้าชื่อ":
                tag_str = sep.join(chosen_tags)
                new_base = f"{tag_str}{sep}{name}"
            else:
                tag_str = sep.join(chosen_tags)
                new_base = f"{name}{sep}{tag_str}"

            # ลบอักขระที่ใช้เป็นชื่อไฟล์ไม่ได้
            new_base = self._sanitize_filename(new_base)

            final_ext = ext if self.keep_ext.get() else ".mp4"
            new_fullname = new_base + final_ext
            new_path = os.path.join(os.path.dirname(fpath), new_fullname)
            results.append((fpath, new_path, new_fullname))

        return results, None

    def _pick_tags(self, tags, count):
        """เลือกแฮชแท็กแบบสุ่ม"""
        available = tags.copy()
        if self.shuffle_tags.get():
            random.shuffle(available)

        # ถ้ามีไม่พอ ให้วน
        while len(available) < count:
            extra = tags.copy()
            if self.shuffle_tags.get():
                random.shuffle(extra)
            available.extend(extra)
        return available[:count]

    def _sanitize_filename(self, name):
        """ลบอักขระที่ไม่สามารถใช้ในชื่อไฟล์ได้"""
        invalid = '<>:"/\\|?*'
        for ch in invalid:
            name = name.replace(ch, "")
        # ตัดช่องว่างหัวท้าย
        name = name.strip()
        # จำกัดความยาว (เผื่อ ext)
        if len(name) > 200:
            name = name[:200]
        return name

    def preview_names_fn(self):
        """แสดงตัวอย่างชื่อใหม่ใน preview area"""
        results, error = self.generate_new_names()
        self.preview_text.delete(1.0, tk.END)

        if error:
            self.preview_text.insert(tk.END, f"{error}\n")
            self.status_var.set(error)
            return

        self.preview_names = results
        self.preview_text.insert(tk.END, f"📋 ตัวอย่างชื่อใหม่ ({len(results)} ไฟล์):\n")
        self.preview_text.insert(tk.END, "─" * 60 + "\n")
        for _, _, new_name in results:
            self.preview_text.insert(tk.END, f"  → {new_name}\n")
        self.preview_text.insert(tk.END, "─" * 60 + "\n")
        self.preview_text.insert(tk.END, "💡 กด 'เริ่มเปลี่ยนชื่อ!' เพื่อดำเนินการจริง\n")

        self.status_var.set(f"พรีวิวพร้อม ({len(results)} ไฟล์) ► กดเริ่มเพื่อเปลี่ยนชื่อจริง")

    def start_rename(self):
        """เริ่มเปลี่ยนชื่อ (มี dialog ยืนยัน)"""
        if not self.video_files:
            messagebox.showwarning("ไม่มีไฟล์", "กรุณาเลือกไฟล์วิดีโอก่อน")
            return

        # สร้างชื่อใหม่ก่อน (หรือใช้จาก preview)
        if not self.preview_names:
            results, error = self.generate_new_names()
            if error:
                messagebox.showerror("ข้อผิดพลาด", error)
                return
        else:
            # regenerate เสมอ เพื่อให้ random ใหม่ทุกครั้งที่กด
            results, error = self.generate_new_names()
            if error:
                messagebox.showerror("ข้อผิดพลาด", error)
                return

        # ยืนยัน
        ok = messagebox.askokcancel(
            "ยืนยันการเปลี่ยนชื่อ",
            f"กำลังจะเปลี่ยนชื่อ {len(results)} ไฟล์\n\n"
            "ตัวอย่าง 3 รายการแรก:\n" +
            "\n".join(f"  → {r[2]}" for r in results[:3]) +
            "\n\nดำเนินการต่อ?"
        )
        if not ok:
            return

        # รันใน thread เพื่อไม่ให้ GUI ค้าง
        self.btn_rename.config(state=tk.DISABLED)
        self.progress["maximum"] = len(results)
        self.progress["value"] = 0

        thread = threading.Thread(target=self._do_rename, args=(results,), daemon=True)
        thread.start()

    def _do_rename(self, results):
        """เปลี่ยนชื่อไฟล์จริง (รันใน background thread)"""
        success = 0
        errors = []

        for i, (old_path, new_path, new_name) in enumerate(results):
            try:
                # ตรวจสอบว่าชื่อซ้ำหรือไม่
                if os.path.exists(new_path) and old_path != new_path:
                    # เติมเลขกันชน
                    base, ext = os.path.splitext(new_path)
                    counter = 1
                    while os.path.exists(f"{base}_{counter}{ext}"):
                        counter += 1
                    new_path = f"{base}_{counter}{ext}"

                os.rename(old_path, new_path)
                success += 1
            except Exception as e:
                errors.append(f"❌ {os.path.basename(old_path)} → {e}")

            # อัปเดต progress
            self.root.after(0, lambda v=i+1: self.progress.configure(value=v))

        # แสดงผล
        msg = f"✅ เปลี่ยนชื่อสำเร็จ: {success} ไฟล์"
        if errors:
            msg += f"\n❌ ล้มเหลว: {len(errors)} ไฟล์\n" + "\n".join(errors[:5])
            if len(errors) > 5:
                msg += f"\n... และอีก {len(errors)-5} รายการ"

        self.root.after(0, lambda: self._rename_done(msg, success))

    def _rename_done(self, msg, success):
        """callback หลังเปลี่ยนชื่อเสร็จ"""
        self.btn_rename.config(state=tk.NORMAL)
        self.progress["value"] = 0

        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, msg)

        if success > 0:
            # เคลียร์รายการเก่า
            self.video_files.clear()
            self.file_listbox.delete(0, tk.END)
            self.lbl_file_count.config(text="จำนวน: 0 ไฟล์")
            self.preview_names.clear()

        self.status_var.set(msg.replace("\n", " | "))

        messagebox.showinfo("เสร็จสิ้น", msg)


# ============================================================
#  ENTRY POINT
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()

    # ไอคอน (ถ้ามี)
    # try:
    #     root.iconbitmap("icon.ico")
    # except:
    #     pass

    app = ChangNameVideoApp(root)
    root.mainloop()
