#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║  YumClip (ยำรวมคลิป) — Video Clip Mixer             ║
║  สุ่มคลิปวิดีโอจากโฟลเดอร์ มารวมกันเป็นคลิปใหม่      ║
╚══════════════════════════════════════════════════════╝

Requires: ffmpeg + ffprobe (in PATH)
"""

import os
import sys
import random
import re
import subprocess
import argparse
import shutil
from pathlib import Path
from typing import Callable

# ── Supported video extensions ──
VIDEO_EXTENSIONS = {
    ".mp4", ".avi", ".mov", ".mkv", ".webm",
    ".flv", ".wmv", ".m4v", ".mpg", ".mpeg", ".3gp", ".ts"
}


def get_video_files(folder: Path, recursive: bool = False) -> list[Path]:
    """Return all video files in folder.  Set recursive=True to scan subfolders."""
    files = []
    iterator = folder.rglob("*") if recursive else folder.iterdir()
    for f in iterator:
        if f.is_file() and f.suffix.lower() in VIDEO_EXTENSIONS:
            files.append(f)
    return files


def get_duration(filepath: Path) -> float:
    """Get video duration in seconds via ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(filepath)
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return float(r.stdout.strip())
    except (ValueError, subprocess.TimeoutExpired):
        return 0.0


def _load_used_names(used_folder: Path) -> set[str]:
    """Return set of filenames that have already been used (tracked in used_folder)."""
    if not used_folder.is_dir():
        return set()
    return {f.name for f in used_folder.iterdir() if f.is_file()}


def _save_used_snapshot(used_folder: Path, snapshot_file: Path):
    """Write a snapshot text file listing what was used in this batch."""
    used_folder.mkdir(parents=True, exist_ok=True)
    existing = {f.name for f in used_folder.iterdir() if f.is_file()}
    snapshot_file.write_text("\n".join(sorted(existing)) + "\n", encoding="utf-8")


def _tokenize_stem(stem: str) -> list[str]:
    """Split a filename stem into meaningful tokens."""
    s = stem.replace("_", " ").replace("-", " ").replace(".", " ")
    return [t.strip() for t in s.split() if t.strip()]


def _build_output_name(selected_videos: list[Path]) -> str:
    """
    Pick 2 random source filenames, merge their unique tokens,
    remove duplicates, keep the length reasonable.
    """
    sources = random.sample(selected_videos, min(2, len(selected_videos)))

    all_tokens: list[str] = []
    seen: set[str] = set()
    for src in sources:
        for token in _tokenize_stem(src.stem):
            key = token.lower()
            if key not in seen:
                all_tokens.append(token)
                seen.add(key)

    name = " ".join(all_tokens)

    MAX_LEN = 80
    if len(name) > MAX_LEN:
        name = name[:MAX_LEN].rsplit(" ", 1)[0]

    return name if name else sources[0].stem


def _write_concat_file(video_list: list[Path], concat_path: str):
    """Write ffmpeg concat demuxer file."""
    with open(concat_path, "w", encoding="utf-8") as f:
        for v in video_list:
            safe = str(v.absolute()).replace("\\", "/")
            f.write(f"file '{safe}'\n")


def _parse_resolution(res: str) -> tuple[int, int] | None:
    """
    Parse resolution string.  Returns (w, h) or None.
    Accepts:  "1920x1080",  "1280:720",  "1080" (scales height, keeps AR).
    """
    if not res:
        return None
    res = res.strip()
    # "1920x1080" or "1920:1080"
    m = re.match(r"^(\d+)[x:](\d+)$", res, re.IGNORECASE)
    if m:
        return int(m.group(1)), int(m.group(2))
    # "1080" → scale to height 1080, width auto
    m = re.match(r"^(\d+)$", res)
    if m:
        val = int(m.group(1))
        if val <= 2160:
            return (-2, val)  # -2 = auto width (ffmpeg scale flag)
        return None
    return None


def combine_videos(
    video_list: list[Path],
    output_path: str,
    threads: int = 0,
    resolution: str | None = None,
    no_audio: bool = False,
    audio_only: bool = False,
) -> bool:
    """
    Concatenate videos using ffmpeg concat demuxer (stream copy — fast).
    Falls back to re-encode if codecs differ.

    Parameters
    ----------
    threads : int
        CPU threads. 0 = auto.  Set 2-4 on weak PCs.
    resolution : str or None
        Force output resolution, e.g. "1920x1080" or "1080".
    no_audio : bool
        Strip audio track.
    audio_only : bool
        Strip video, keep audio only.
    """
    concat_file = output_path + ".txt"
    _write_concat_file(video_list, concat_file)

    thread_args = ["-threads", str(threads)] if threads > 0 else []
    needs_filter = bool(resolution or no_audio or audio_only)

    # ── Attempt 1: stream copy (fast) — only if no filters ──
    if not needs_filter:
        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_file, "-c", "copy", *thread_args, output_path
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0:
            os.remove(concat_file)
            return True
        print("   (stream-copy failed, retrying with re-encode…)")

    # ── Attempt 2: re-encode ──
    cmd2 = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_file,
    ]

    # Video codec
    if audio_only:
        cmd2 += ["-vn"]
    else:
        cmd2 += ["-c:v", "libx264", "-preset", "fast", "-crf", "23"]

    # Audio codec
    if no_audio:
        cmd2 += ["-an"]
    else:
        cmd2 += ["-c:a", "aac"]

    # Resolution filter
    if resolution:
        parsed = _parse_resolution(resolution)
        if parsed:
            w, h = parsed
            # -2 means "auto" in ffmpeg scale
            scale_w = f"{w}" if w > 0 else "-2"
            scale_h = f"{h}" if h > 0 else "-2"
            cmd2 += ["-vf", f"scale={scale_w}:{scale_h}"]

    cmd2 += thread_args + [output_path]

    r2 = subprocess.run(cmd2, capture_output=True, text=True)

    if os.path.exists(concat_file):
        os.remove(concat_file)
    return r2.returncode == 0


def yum_clip(
    folder: str,
    min_duration: float = 20.0,
    num_outputs: int = 5,
    output_folder: str | None = None,
    max_overage: float | None = None,
    used_folder: str | None = None,
    move_used: bool = False,
    threads: int = 0,
    recursive: bool = False,
    resolution: str | None = None,
    no_audio: bool = False,
    audio_only: bool = False,
    progress_callback: Callable[[int, int, str], None] | None = None,
):
    """
    Main mixer logic.

    Parameters
    ----------
    folder : str
        Path to folder containing source videos.
    min_duration : float
        Minimum total duration (seconds) for each output clip.
    num_outputs : int
        Number of output clips to produce.
    output_folder : str or None
        Where to save results.  Defaults to ``<folder>/YumClip_Output``.
    max_overage : float or None
        Each group's total will not exceed min_duration + max_overage.
    used_folder : str or None
        Folder tracking already-used clips.  Defaults to ``<folder>/YumClip_Used``.
    move_used : bool
        MOVE source files into used_folder instead of copying.
    threads : int
        ffmpeg CPU threads. 0 = auto.
    recursive : bool
        Scan subfolders recursively.
    resolution : str or None
        Force output resolution, e.g. "1920x1080" or "1080".
    no_audio : bool
        Strip audio from output.
    audio_only : bool
        Keep audio only, drop video.
    progress_callback : callable or None
        Called as progress_callback(current, total, status_text) for GUI updates.
    """
    folder = Path(folder).expanduser().resolve()
    if not folder.is_dir():
        print(f"❌ Folder not found: {folder}")
        return

    # ── Used folder ──
    if used_folder is None:
        used_folder = folder / "YumClip_Used"
    else:
        used_folder = Path(used_folder).expanduser().resolve()
    used_folder.mkdir(parents=True, exist_ok=True)

    used_names = _load_used_names(used_folder)

    # ── Gather videos ──
    all_videos = get_video_files(folder, recursive=recursive)
    videos = [v for v in all_videos if v.name not in used_names]

    skipped = len(all_videos) - len(videos)
    if skipped > 0:
        print(f"⏭  Skipping {skipped} already-used clip(s) (tracked in {used_folder})")

    if len(videos) < 2:
        print(f"❌ Need ≥ 2 fresh video files, found {len(videos)} "
              f"(+{skipped} used) in {folder}")
        if progress_callback:
            progress_callback(0, num_outputs, "❌ Not enough videos")
        return

    scan_mode = "recursive" if recursive else "flat"
    print(f"\n📁 {folder}  ({scan_mode})")
    print(f"🎬 {len(videos)} fresh video(s)  +  {skipped} already used\n")

    # ── Scan durations ──
    print("⏱  Scanning durations…")
    dur: dict[Path, float] = {}
    for v in videos:
        d = get_duration(v)
        dur[v] = d

    # ── Filter out videos that already exceed min_duration ──
    too_long = [v for v, d in dur.items() if d >= min_duration]
    if too_long:
        print(f"\n⏭  Filtering out {len(too_long)} clip(s) already ≥ {min_duration}s:")
        for v in too_long:
            print(f"      • {v.name} ({dur[v]:.1f}s)")
            del dur[v]
            videos.remove(v)

    # Show remaining videos
    print(f"\n   Remaining for mixing: {len(videos)} clip(s)")
    for v in videos:
        print(f"   {v.name:<50s} {dur[v]:>8.1f}s")
    print()

    # Check again after filtering
    if len(videos) < 2:
        print(f"❌ After filtering, only {len(videos)} clip(s) remain — need ≥ 2 to mix")
        if progress_callback:
            progress_callback(0, num_outputs, "❌ Not enough short clips")
        return

    # ── Output folder ──
    if output_folder is None:
        output_folder = folder / "YumClip_Output"
    else:
        output_folder = Path(output_folder).expanduser().resolve()
    output_folder.mkdir(parents=True, exist_ok=True)

    # ── Overage cap ──
    if max_overage is None:
        max_overage = max(min_duration * 0.2, 2.0)

    pool = list(videos)
    random.shuffle(pool)

    used_this_run: list[Path] = []
    actual_count = 0  # how many we actually produced

    for i in range(1, num_outputs + 1):
        if not pool:
            print(f"⚠  No fresh videos left — stopping after {i - 1} output(s)")
            break

        # ── Progress callback ──
        if progress_callback:
            progress_callback(i - 1, num_outputs, f"กำลังยำคลิปที่ {i}/{num_outputs}…")

        # Build one group
        selected: list[Path] = []
        total = 0.0
        target_ceiling = min_duration + max_overage

        round_pool = pool.copy()
        random.shuffle(round_pool)

        for v in round_pool:
            d = dur[v]
            if total >= min_duration and total + d > target_ceiling:
                continue
            selected.append(v)
            total += d
            pool.remove(v)
            if total >= min_duration:
                break

        if total < min_duration:
            print(f"⚠  Output #{i}: only reached {total:.1f}s (target ≥ {min_duration}s)")

        # ── Name output ──
        base_name = _build_output_name(selected)
        out_path = output_folder / f"{base_name}.mp4"
        if out_path.exists():
            for dup_n in range(1, 100):
                out_path = output_folder / f"{base_name}_{dup_n}.mp4"
                if not out_path.exists():
                    break
        out_name = out_path.name

        print(f"🍜 Output #{i}  →  {out_name}")
        print(f"   Clips: {len(selected)}  |  Total: {total:.1f}s  |  Target ≥ {min_duration}s")
        for v in selected:
            print(f"      • {v.name} ({dur[v]:.1f}s)")

        ok = combine_videos(
            selected, str(out_path),
            threads=threads, resolution=resolution,
            no_audio=no_audio, audio_only=audio_only,
        )
        if ok:
            print(f"   ✅ Saved")
            used_this_run.extend(selected)
            actual_count = i
        else:
            print(f"   ❌ Failed")
        print()

    # ── Progress done ──
    if progress_callback:
        progress_callback(actual_count, num_outputs, "✅ เสร็จแล้ว!")

    # ── Register used clips ──
    if used_this_run:
        action = "Moving" if move_used else "Copying"
        print(f"📦 {action} {len(used_this_run)} used clip(s) to {used_folder} …")
        for v in used_this_run:
            dest = used_folder / v.name
            try:
                if move_used:
                    shutil.move(str(v), str(dest))
                else:
                    shutil.copy2(str(v), str(dest))
                print(f"   {'→' if move_used else '📋'} {v.name}")
            except OSError as e:
                print(f"   ⚠  Could not {action.lower()} {v.name}: {e}")

    snapshot = output_folder / "YumClip_used_snapshot.txt"
    _save_used_snapshot(used_folder, snapshot)

    print(f"\n📂 Done!  Output → {output_folder}")
    print(f"📂 Used   → {used_folder}  ({len(used_this_run)} new + {skipped} prior)")

    return actual_count, str(output_folder), str(used_folder)


# ── CLI entry point ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        prog="yumclip",
        description="YumClip (ยำรวมคลิป) — Random video clip mixer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  yumclip "D:\\My Videos"
  yumclip "D:\\My Videos" -d 30 -n 3 -r
  yumclip "D:\\My Videos" --min-duration 25 --num-outputs 5 -o "D:\\Output"
  yumclip "D:\\My Videos" -r --res 1920x1080 --no-audio
  yumclip "D:\\My Videos" --used-folder "D:\\UsedClips" --move-used
  yumclip "D:\\My Videos" -t 2 --gui
        """,
    )
    parser.add_argument(
        "folder", nargs="?", default=None,
        help="Folder containing video files"
    )
    parser.add_argument(
        "-d", "--min-duration", type=float, default=20.0,
        help="Minimum total duration per output clip in seconds (default: 20)"
    )
    parser.add_argument(
        "-n", "--num-outputs", type=int, default=5,
        help="Number of output clips to create (default: 5)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output folder (default: <source>/YumClip_Output)"
    )
    parser.add_argument(
        "--max-overage", type=float, default=None,
        help="Max seconds over min_duration per group (default: 20%% of min_duration)"
    )
    parser.add_argument(
        "-u", "--used-folder",
        help="Folder to track used clips (default: <source>/YumClip_Used)"
    )
    parser.add_argument(
        "--move-used", action="store_true",
        help="MOVE source files to used folder (default: COPY)"
    )
    parser.add_argument(
        "-t", "--threads", type=int, default=0,
        help="ffmpeg CPU threads (0=auto, use 2-4 on weak PCs)"
    )
    parser.add_argument(
        "-r", "--recursive", action="store_true",
        help="Scan subfolders recursively"
    )
    parser.add_argument(
        "--res", "--resolution", type=str, default=None, metavar="WxH",
        help="Force output resolution, e.g. 1920x1080 or 1080"
    )
    parser.add_argument(
        "--no-audio", action="store_true",
        help="Strip audio from output"
    )
    parser.add_argument(
        "--audio-only", action="store_true",
        help="Keep audio only (drop video)"
    )
    parser.add_argument(
        "--gui", action="store_true",
        help="Launch simple tkinter GUI"
    )

    args = parser.parse_args()

    if args.gui or args.folder is None:
        launch_gui(
            folder=args.folder if args.folder else "",
            min_dur=args.min_duration,
            num_out=args.num_outputs,
            output=args.output if args.output else "",
            threads=args.threads,
            recursive=args.recursive,
            resolution=args.res or "",
            no_audio=args.no_audio,
            audio_only=args.audio_only,
        )
    else:
        yum_clip(
            folder=args.folder,
            min_duration=args.min_duration,
            num_outputs=args.num_outputs,
            output_folder=args.output,
            max_overage=args.max_overage,
            used_folder=args.used_folder,
            move_used=args.move_used,
            threads=args.threads,
            recursive=args.recursive,
            resolution=args.res,
            no_audio=args.no_audio,
            audio_only=args.audio_only,
        )


# ── GUI (tkinter) ────────────────────────────────────────────────
def launch_gui(
    folder: str = "",
    min_dur: float = 20.0,
    num_out: int = 5,
    output: str = "",
    threads: int = 0,
    recursive: bool = False,
    resolution: str = "",
    no_audio: bool = False,
    audio_only: bool = False,
):
    """Simple cross-platform GUI."""
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox, ttk
    except ImportError:
        print("tkinter not available — use CLI mode instead.")
        sys.exit(1)

    root = tk.Tk()
    root.title("YumClip (ยำรวมคลิป)")
    root.geometry("580x740")
    root.resizable(False, False)

    bg = "#1e1e2e"
    fg = "#cdd6f4"
    accent = "#f38ba8"
    sub_color = "#a6adc8"
    entry_bg = "#313244"
    btn_bg = "#585b70"
    root.configure(bg=bg)

    # ── Header ──
    tk.Label(
        root, text="🍜 YumClip — ยำรวมคลิป",
        font=("Segoe UI", 18, "bold"), fg=accent, bg=bg
    ).pack(pady=(18, 6))

    # ── Helper: labelled entry row ──
    def _labeled_entry(parent, label, var, browse=False, width=None):
        frm = tk.Frame(parent, bg=bg)
        frm.pack(fill="x", padx=28, pady=3)
        tk.Label(frm, text=label, fg=fg, bg=bg, font=("Segoe UI", 10)).pack(anchor="w")
        row = tk.Frame(frm, bg=bg)
        row.pack(fill="x", pady=(2, 0))
        kw = {"font": ("Segoe UI", 9), "bg": entry_bg, "fg": fg,
              "insertbackground": fg, "relief": "flat"}
        if width:
            kw["width"] = width
        tk.Entry(row, textvariable=var, **kw).pack(
            side="left", fill="x", expand=not width, ipady=3)
        if browse:
            tk.Button(row, text="Browse…", font=("Segoe UI", 8),
                      bg=btn_bg, fg=fg, relief="flat", padx=10,
                      command=lambda: var.set(filedialog.askdirectory())
                      ).pack(side="left", padx=(6, 0))

    # ── Helper: single-line field (label + small entry) ──
    def _small_field(parent, label, var, width=8):
        frm = tk.Frame(parent, bg=bg)
        frm.pack(fill="x", padx=28, pady=3)
        tk.Label(frm, text=label, fg=fg, bg=bg, font=("Segoe UI", 10)).pack(anchor="w")
        tk.Entry(frm, textvariable=var, font=("Segoe UI", 10), width=width,
                 bg=entry_bg, fg=fg, insertbackground=fg, relief="flat",
                 justify="center").pack(anchor="w", ipady=3)

    # ── Fields ────────────────────────────────────────────────

    folder_var = tk.StringVar(value=folder)
    _labeled_entry(root, "📁 โฟลเดอร์ต้นทาง", folder_var, browse=True)

    out_var = tk.StringVar(value=output)
    _labeled_entry(root, "📂 โฟลเดอร์ปลายทาง (คลิปที่ยำเสร็จ)", out_var, browse=True)

    dur_var = tk.DoubleVar(value=min_dur)
    _small_field(root, "⏱  ความยาวขั้นต่ำต่อคลิปผลลัพธ์ (วินาที)", dur_var)

    num_var = tk.IntVar(value=num_out)
    _small_field(root, "🎬 จำนวนคลิปที่ต้องการ", num_var)

    thread_var = tk.IntVar(value=threads)
    _small_field(root, "🧵 Threads (0=auto, 2-4 สำหรับคอมไม่แรง)", thread_var)

    res_var = tk.StringVar(value=resolution)
    _small_field(root, "📐 ความละเอียด (ว่าง=เดิม / 1920x1080 / 1080)", res_var, width=16)

    used_var = tk.StringVar(value="")
    _labeled_entry(root, "🗂  โฟลเดอร์เก็บคลิปที่ใช้แล้ว (กันซ้ำ)", used_var, browse=True)

    # ── Checkboxes ──
    def _checkbox(parent, var, text):
        frm = tk.Frame(parent, bg=bg)
        frm.pack(fill="x", padx=28, pady=1)
        tk.Checkbutton(
            frm, variable=var, text=text,
            fg=sub_color, bg=bg, selectcolor=entry_bg,
            activebackground=bg, activeforeground=fg,
            font=("Segoe UI", 9)
        ).pack(anchor="w")

    recurse_var = tk.BooleanVar(value=recursive)
    _checkbox(root, recurse_var, "📁 สแกนโฟลเดอร์ย่อยด้วย (-r)")

    move_var = tk.BooleanVar(value=False)
    _checkbox(root, move_var, "📦 ย้ายคลิปไปโฟลเดอร์ใช้แล้ว (แทน copy)")

    no_audio_var = tk.BooleanVar(value=no_audio)
    _checkbox(root, no_audio_var, "🔇 ไม่มีเสียง (--no-audio)")

    audio_only_var = tk.BooleanVar(value=audio_only)
    _checkbox(root, audio_only_var, "🎵 เอาแต่เสียง (--audio-only)")

    # ── Progress bar ──
    progress_var = tk.DoubleVar(value=0)
    progress_bar = ttk.Progressbar(
        root, variable=progress_var, maximum=num_var.get(), length=480
    )
    progress_bar.pack(pady=(12, 4))

    status_var = tk.StringVar(value="Ready")
    tk.Label(root, textvariable=status_var, fg=sub_color, bg=bg,
             font=("Segoe UI", 9)).pack(pady=(0, 6))

    # ── Progress callback (called by yum_clip) ──
    def on_progress(current: int, total: int, text: str):
        progress_var.set(current)
        status_var.set(text)
        root.update_idletasks()

    # ── Go button ──
    def on_mix():
        f = folder_var.get().strip()
        if not f:
            messagebox.showerror("Error", "กรุณาเลือกโฟลเดอร์ต้นทางก่อน")
            return
        if not Path(f).is_dir():
            messagebox.showerror("Error", f"ไม่พบโฟลเดอร์:\n{f}")
            return

        used = used_var.get().strip() or None
        out = out_var.get().strip() or None
        res = res_var.get().strip() or None

        progress_var.set(0)
        progress_bar["maximum"] = num_var.get()
        status_var.set("⏳ กำลังสแกนวิดีโอ…")
        root.update_idletasks()

        try:
            result = yum_clip(
                folder=f,
                min_duration=dur_var.get(),
                num_outputs=num_var.get(),
                output_folder=out,
                used_folder=used,
                move_used=move_var.get(),
                threads=thread_var.get(),
                recursive=recurse_var.get(),
                resolution=res,
                no_audio=no_audio_var.get(),
                audio_only=audio_only_var.get(),
                progress_callback=on_progress,
            )
            progress_var.set(num_var.get())
            status_var.set("✅ เสร็จแล้ว!")
            if result:
                cnt, out_d, used_d = result
                messagebox.showinfo("Done",
                    f"ยำคลิปเสร็จแล้ว 🍜\n\n"
                    f"🎬 สร้าง {cnt} คลิป\n"
                    f"📂 ผลลัพธ์ → {out_d}\n"
                    f"🗂  คลิปที่ใช้แล้ว → {used_d}")
        except Exception as e:
            status_var.set("❌ Error")
            messagebox.showerror("Error", str(e))

    tk.Button(
        root, text="🍜 เริ่มยำคลิป!",
        command=on_mix,
        font=("Segoe UI", 14, "bold"),
        bg=accent, fg="#1e1e2e",
        activebackground="#eba0ac", activeforeground="#1e1e2e",
        relief="flat", padx=30, pady=8, cursor="hand2"
    ).pack(pady=(8, 0))

    tk.Label(
        root, text="ต้องมี ffmpeg ใน PATH | สร้างโดย Kvasir",
        font=("Segoe UI", 7), fg="#585b70", bg=bg
    ).pack(side="bottom", pady=6)

    root.mainloop()


if __name__ == "__main__":
    main()
