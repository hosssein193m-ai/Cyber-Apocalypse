# =============================================================================
#  💀💀  CYBER APOCALYPSE — WINDOWS EDITION  💀💀
# -----------------------------------------------------------------------------
#  Author   : MohixCode / Mohammadreza Nouriyani
#  Adapted  : For Windows (fullscreen fixed)
# -----------------------------------------------------------------------------
#  ✅ TESTED ON:
#     - Windows 10 / 11
#     - Python 3.8+
# -----------------------------------------------------------------------------
#  🎯 FEATURES:
#     1.  Full-screen hacker prank (Tkinter)
#     2.  Matrix rain + glitch storm + fake progress + fake dump
#     3.  Emoji explosion + screamers
#     4.  🖱️  Mouse hijack (pyautogui)
#     5.  📝  Auto-typing in Notepad
#     6.  🖼️  Desktop wallpaper swap (Win32 API via ctypes)
#     7.  🎭  Interactive responses to clicks/keys
#     8.  ♻️  FULL ROLLBACK after 20s or on ESC/Ctrl+Shift+Q
# -----------------------------------------------------------------------------
#  📦 INSTALL (Windows):
#     pip install pyautogui pillow
#     (pywin32 اختیاری — کد از ctypes استفاده می‌کنه)
# -----------------------------------------------------------------------------
#  ▶️ RUN:
#     python cyber_apocalypse.py
# =============================================================================

import tkinter as tk
import random
import time
import os
import sys
import threading
import subprocess
import ctypes

# -----------------------------------------------------------------------------
#  OPTIONAL IMPORTS
# -----------------------------------------------------------------------------
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

try:
    from PIL import ImageGrab
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import pyautogui
    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0.02
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False

# -----------------------------------------------------------------------------
#  PATHS & CONFIG
# -----------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()
ASSETS_DIR = os.path.join(SCRIPT_DIR, "assets")
BACKUP_DIR = os.path.join(SCRIPT_DIR, ".backup")
SHOTS_DIR  = os.path.join(SCRIPT_DIR, "screenshots")
os.makedirs(BACKUP_DIR, exist_ok=True)

ENABLE_AUDIO     = True
ENABLE_MOUSE     = True
ENABLE_NOTEPAD   = True
ENABLE_WALLPAPER = True
ENABLE_SHOTS     = True
SHOT_INTERVAL    = 15
AUTO_ROLLBACK_MS = 20000

# -----------------------------------------------------------------------------
#  COLORS & TEXT
# -----------------------------------------------------------------------------
NEON_COLORS = ["#00ffff", "#ff00ff", "#ffff00", "#ff0040", "#00ff88", "#ffffff"]
MATRIX_CHARS = "アカサタナハマヤラワ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&*+=<>"
HACKER_EMOJIS = ["💀", "👾", "🎭", "😈", "🔥", "☠️", "🕶️", "💻", "🧨", "🚨"]

FONT_MONO  = ("Consolas", 14, "bold")
FONT_EMOJI = ("Segoe UI Emoji", 24)
FONT_BIG   = ("Consolas", 40, "bold")
FONT_LABEL = ("Consolas", 22, "bold")
FONT_SUB   = ("Consolas", 14)
FONT_DUMP  = ("Consolas", 12)

_photo_refs = []

def load_photo(path):
    try:
        img = tk.PhotoImage(file=path)
        _photo_refs.append(img)
        return img
    except Exception:
        return None


# =============================================================================
#  SOUND HELPER (Windows — winsound)
# =============================================================================
def beep(freq=800, dur=120):
    if not (ENABLE_AUDIO and HAS_WINSOUND):
        return
    try:
        threading.Thread(
            target=winsound.Beep,
            args=(freq, dur),
            daemon=True
        ).start()
    except Exception:
        pass


# =============================================================================
#  WALLPAPER MANAGER (Windows — ctypes / Win32 API)
# =============================================================================
class WallpaperManager:
    SPI_SETDESKWALLPAPER = 0x0014
    SPI_GETDESKWALLPAPER = 0x0073

    def __init__(self):
        self.original = None
        self.backup_path = os.path.join(BACKUP_DIR, "original_wallpaper.txt")

    def save_current(self):
        try:
            buf = ctypes.create_unicode_buffer(512)
            ctypes.windll.user32.SystemParametersInfoW(
                self.SPI_GETDESKWALLPAPER, 512, buf, 0
            )
            self.original = buf.value or ""
            with open(self.backup_path, "w", encoding="utf-8") as f:
                f.write(self.original)
        except Exception:
            self.original = ""

    def set_wallpaper(self, image_path):
        if not os.path.isfile(image_path):
            return False
        try:
            abs_path = os.path.abspath(image_path)
            ctypes.windll.user32.SystemParametersInfoW(
                self.SPI_SETDESKWALLPAPER, 0, abs_path, 3
            )
            return True
        except Exception:
            return False

    def restore(self):
        try:
            if self.original and os.path.isfile(self.original):
                ctypes.windll.user32.SystemParametersInfoW(
                    self.SPI_SETDESKWALLPAPER, 0, self.original, 3
                )
                return True
        except Exception:
            pass
        return False


# =============================================================================
#  NOTEPAD INJECTOR (Windows)
# =============================================================================
class NotepadInjector:
    def __init__(self):
        self.proc = None
        self.message = ""

    def open_and_type(self, username="user"):
        self.message = f"""========================================
        YOU HAVE BEEN HACKED  💀
========================================

Hello {username},

I have been watching you for a while.
Your files, your photos, your passwords...
Everything is now MINE.

Do NOT try to close this window.
Do NOT try to restart your computer.
It is already too late.

Just remember:
    WE OWN YOUR SYSTEM.

   😈  Have a nice day  😈
========================================
"""
        try:
            self.proc = subprocess.Popen(["notepad.exe"])
        except Exception:
            self.proc = None
            return
        threading.Thread(target=self._type_worker, daemon=True).start()

    def _type_worker(self):
        time.sleep(1.8)
        if not HAS_PYAUTOGUI:
            return
        try:
            for line in self.message.splitlines():
                pyautogui.typewrite(line, interval=0.02)
                pyautogui.press("enter")
                time.sleep(0.08)
        except Exception:
            pass

    def close(self):
        if self.proc is not None:
            try:
                self.proc.terminate()
            except Exception:
                try:
                    subprocess.run(
                        ["taskkill", "/F", "/IM", "notepad.exe"],
                        capture_output=True
                    )
                except Exception:
                    pass
        # اضافه: هر notepad دیگه‌ای هم بسته بشه
        try:
            subprocess.run(
                ["taskkill", "/F", "/IM", "notepad.exe"],
                capture_output=True
            )
        except Exception:
            pass


# =============================================================================
#  MOUSE HIJACKER
# =============================================================================
class MouseHijacker:
    def __init__(self):
        self._stop = threading.Event()
        self._thread = None

    def start(self):
        if not (ENABLE_MOUSE and HAS_PYAUTOGUI):
            return
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()

    def _worker(self):
        try:
            w, h = pyautogui.size()
            while not self._stop.is_set():
                x = random.randint(50, max(60, w - 50))
                y = random.randint(50, max(60, h - 50))
                try:
                    pyautogui.moveTo(x, y,
                                     duration=random.uniform(0.15, 0.5))
                    if random.random() < 0.25:
                        pyautogui.click()
                except Exception:
                    pass
                self._stop.wait(random.uniform(0.4, 1.2))
        except Exception:
            pass


# =============================================================================
#  SCREENSHOT WORKER
# =============================================================================
def _shot_loop(stop_event):
    if not (ENABLE_SHOTS and HAS_PIL):
        return
    os.makedirs(SHOTS_DIR, exist_ok=True)
    n = 0
    while not stop_event.is_set():
        try:
            img = ImageGrab.grab()
            img.save(os.path.join(SHOTS_DIR, f"shot_{n:03d}.png"))
            n += 1
        except Exception:
            pass
        for _ in range(SHOT_INTERVAL * 10):
            if stop_event.is_set():
                return
            time.sleep(0.1)


# =============================================================================
#  MAIN PRANK
# =============================================================================
class CyberApocalypse:
    def __init__(self):
        self.exit_now = False

        # ---- Sub-systems -----------------------------------------------
        self.wallpaper = WallpaperManager()
        self.notepad   = NotepadInjector()
        self.mouse     = MouseHijacker()

        # ---- Counters --------------------------------------------------
        self.click_count = 0
        self.key_count   = 0
        self._rollback_scheduled = False

        # =============================================================
        #  WINDOW SETUP — WINDOWS FULLSCREEN
        # =============================================================
        self.root = tk.Tk()
        self.root.title("Cyber Apocalypse")

        self.W = self.root.winfo_screenwidth()
        self.H = self.root.winfo_screenheight()

        # ۱. پس‌زمینه
        self.root.configure(bg="black")

        # ۲. topmost
        self.root.attributes("-topmost", True)

        # ۳. fullscreen
        try:
            self.root.attributes("-fullscreen", True)
        except Exception:
            pass

        # ۴. geometry دستی
        self.root.geometry(f"{self.W}x{self.H}+0+0")

        # ۵. حذف حاشیه
        try:
            self.root.overrideredirect(True)
        except Exception:
            pass

        # ۶. تأیید دوباره بعد از ۲۰۰ms
        def _confirm_fullscreen():
            try:
                self.root.attributes("-fullscreen", True)
            except Exception:
                pass
            try:
                self.root.geometry(f"{self.W}x{self.H}+0+0")
            except Exception:
                pass
            try:
                self.root.lift()
                self.root.focus_force()
            except Exception:
                pass

        self.root.after(200, _confirm_fullscreen)

        # =============================================================
        #  CANVAS + LABELS
        # =============================================================
        self.canvas = tk.Canvas(self.root, bg="black",
                                highlightthickness=0, cursor="none",
                                width=self.W, height=self.H)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.root, text="> initializing...",
                              font=FONT_LABEL, bg="black", fg="#00ff88")
        self.label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.sub_label = tk.Label(self.root, text="",
                                  font=FONT_SUB, bg="black", fg="#00ffff")
        self.sub_label.place(relx=0.5, rely=0.62, anchor=tk.CENTER)

        # ---- State -----------------------------------------------------
        self.matrix_columns = []
        self._scan_y = 0
        self._progress_value = 0
        self._dump_index = 0

        # ---- Bindings --------------------------------------------------
        self.root.bind("<Escape>", self.close)
        self.root.bind("<Control-Shift-Q>", self.close)
        self.root.bind("<Button-1>", self._on_click)
        self.root.bind("<Key>", self._on_key)

        # ---- Save wallpaper BEFORE anything changes --------------------
        try:
            self.wallpaper.save_current()
        except Exception:
            pass

        # ---- Screenshot thread -----------------------------------------
        self._stop_shots = threading.Event()
        if ENABLE_SHOTS and HAS_PIL:
            threading.Thread(target=_shot_loop,
                             args=(self._stop_shots,),
                             daemon=True).start()

        # ---- Kick off --------------------------------------------------
        beep(900, 150)
        self.root.after(200, self.phase_boot_log)

    # -------------------------------------------------------------------------
    def safe_after(self, ms, func, *args):
        if not self.exit_now:
            self.root.after(ms, func, *args)

    # -------------------------------------------------------------------------
    #  INTERACTION
    # -------------------------------------------------------------------------
    def _on_click(self, _event):
        self.click_count += 1
        msg = random.choice([
            f"You clicked {self.click_count} times. Useless. 😈",
            f"Click #{self.click_count} registered. Keep trying...",
            "You can't click your way out of this.",
        ])
        self.sub_label.config(text=msg, fg="#ff0040")

    def _on_key(self, event):
        self.key_count += 1
        if event.char and event.char.isprintable():
            self.sub_label.config(
                text=f"You typed: '{event.char}'   ({self.key_count} keys)  "
                     f"— Nobody is listening. 😈",
                fg=random.choice(NEON_COLORS)
            )
        return "break"

    # -------------------------------------------------------------------------
    #  PHASE 0 — BOOT LOG
    # -------------------------------------------------------------------------
    def phase_boot_log(self):
        lines = [
            "> Initializing kernel modules ............... [OK]",
            "> Loading encrypted payload ................. [OK]",
            "> Bypassing firewall rules .................. [OK]",
            "> Spoofing MAC address ...................... [OK]",
            "> Hijacking DNS requests .................... [OK]",
            "> Injecting remote shell .................... [OK]",
            "> Disabling logging ......................... [OK]",
            "> Erasing traces ............................ [OK]",
        ]
        self._boot_y = 40
        for i, line in enumerate(lines):
            self.safe_after(i * 200, self._print_boot_line, line)
        self.safe_after(len(lines) * 200 + 400, self.phase_matrix)

    def _print_boot_line(self, text):
        beep(1200, 30)
        self.canvas.create_text(40, self._boot_y, anchor="w",
                                text=text, font=FONT_DUMP,
                                fill="#00ff88", tags="boot")
        self._boot_y += 30

    # -------------------------------------------------------------------------
    #  PHASE 1 — MATRIX RAIN
    # -------------------------------------------------------------------------
    def phase_matrix(self):
        self.canvas.delete("boot")
        self.label.config(text="> MATRIX LINK ESTABLISHED", fg="#00ff88")
        col_w = 20
        n = self.W // col_w
        self.matrix_columns = [
            {"x": i * col_w,
             "y": random.randint(-self.H, 0),
             "speed": random.randint(8, 22)}
            for i in range(n)
        ]
        self._matrix_tick()
        self.safe_after(4000, self.phase_glitch)

    def _matrix_tick(self):
        if self.exit_now:
            return
        for col in self.matrix_columns:
            ch = random.choice(MATRIX_CHARS)
            color = random.choice(["#00ff88", "#00cc66", "#88ffbb", "#ffffff"])
            self.canvas.create_text(col["x"], col["y"], text=ch,
                                    font=FONT_MONO,
                                    fill=color, tags="matrix")
            col["y"] += col["speed"]
            if col["y"] > self.H:
                col["y"] = random.randint(-300, 0)
                col["speed"] = random.randint(8, 22)
        items = self.canvas.find_withtag("matrix")
        if len(items) > 900:
            for it in items[:300]:
                self.canvas.delete(it)
        self.safe_after(60, self._matrix_tick)

    # -------------------------------------------------------------------------
    #  PHASE 2 — GLITCH STORM
    # -------------------------------------------------------------------------
    def phase_glitch(self):
        self.canvas.delete("matrix")
        self.label.config(text="> SYSTEM FAILURE DETECTED", fg="#ff0040")
        self._glitch_tick()
        self._scanline_tick()
        self.safe_after(3000, self.phase_progress)

    def _glitch_tick(self):
        if self.exit_now:
            return
        self.canvas.delete("glitch")
        for _ in range(random.randint(12, 28)):
            y = random.randint(0, self.H)
            h = random.randint(2, 50)
            x = random.randint(-100, self.W)
            w = random.randint(200, self.W + 200)
            c = random.choice(NEON_COLORS)
            self.canvas.create_rectangle(x, y, x + w, y + h,
                                         fill=c, outline=c, tags="glitch")
        for _ in range(random.randint(5, 15)):
            x = random.randint(0, self.W)
            y = random.randint(0, self.H)
            s = random.randint(20, 160)
            c = random.choice(NEON_COLORS)
            self.canvas.create_rectangle(x, y, x + s, y + s,
                                         fill=c, outline=c, tags="glitch")
        if random.random() < 0.1:
            beep(random.randint(200, 1500), 25)
        self.safe_after(random.randint(50, 140), self._glitch_tick)

    def _scanline_tick(self):
        if self.exit_now:
            return
        self.canvas.delete("scan")
        y = self._scan_y
        self.canvas.create_rectangle(0, y, self.W, y + 4,
                                     fill="#00ff88", outline="", tags="scan")
        self._scan_y = (y + 8) % self.H
        self.safe_after(30, self._scanline_tick)

    # -------------------------------------------------------------------------
    #  PHASE 3 — PROGRESS
    # -------------------------------------------------------------------------
    def phase_progress(self):
        self.canvas.delete("glitch")
        self.canvas.delete("scan")
        self.label.config(text="> BYPASSING SECURITY...", fg="#00ffff")
        self._progress_value = 0
        self._progress_tick()

    def _progress_tick(self):
        if self.exit_now:
            return
        if self._progress_value >= 100:
            self.safe_after(300, self.phase_dump)
            return
        self._progress_value += random.randint(2, 7)
        if self._progress_value > 100:
            self._progress_value = 100
        filled = self._progress_value // 5
        bar = "█" * filled + "░" * (20 - filled)
        self.sub_label.config(
            text=f"[{bar}]  {self._progress_value}%   "
                 f"Target: 10.13.37.{random.randint(1,254)}",
            fg="#00ffff"
        )
        beep(1800, 20)
        self.safe_after(random.randint(60, 140), self._progress_tick)

    # -------------------------------------------------------------------------
    #  PHASE 4 — DUMP
    # -------------------------------------------------------------------------
    def phase_dump(self):
        self.label.config(text="> EXFILTRATING DATA...", fg="#ff0040")
        self.sub_label.config(text="")
        self._dump_lines = [
            "root@cyber:~# nmap -sS 192.168.1.0/24",
            "[+] Host 192.168.1.1    UP    (ports 22,80,443)",
            "[!] Exploiting CVE-2024-3094 ... OK",
            "[!] Privilege escalation ... root shell",
            "root@cyber:~# sqlmap -u target.com --dbs",
            "    admin : $2y$10$Xk9...",
            "    user1 : $2y$10$aB3...",
            "[!] Backdoor installed.",
            "[!] All your data belongs to US. 😈",
        ]
        self._dump_index = 0
        self._dump_tick()

    def _dump_tick(self):
        if self.exit_now:
            return
        if self._dump_index >= len(self._dump_lines):
            self.safe_after(400, self.phase_images)
            return
        y = 40 + (self._dump_index % 40) * 24
        if self._dump_index >= 40:
            self.canvas.delete("dump")
        line = self._dump_lines[self._dump_index]
        color = "#ff0040" if "!" in line else "#00ff88"
        self.canvas.create_text(40, y, anchor="w", text=line,
                                font=FONT_DUMP,
                                fill=color, tags="dump")
        beep(2000, 15)
        self._dump_index += 1
        self.safe_after(120, self._dump_tick)

    # -------------------------------------------------------------------------
    #  PHASE 5 — IMAGES + SIDE EFFECTS
    # -------------------------------------------------------------------------
    def phase_images(self):
        self.canvas.delete("dump")
        self.label.config(text="⚠  IDENTITY REVEALED  ⚠",
                          fg="#ff0040", font=("Consolas", 30, "bold"))

        if ENABLE_WALLPAPER:
            self._try_set_hacker_wallpaper()

        if ENABLE_NOTEPAD:
            try:
                user = os.getlogin()
            except Exception:
                user = os.environ.get("USERNAME", "friend")
            self.notepad.open_and_type(user)

        if ENABLE_MOUSE:
            self.mouse.start()

        if os.path.isdir(ASSETS_DIR):
            files = sorted([
                os.path.join(ASSETS_DIR, f)
                for f in os.listdir(ASSETS_DIR)
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
            ])
            flag = next((p for p in files if "images_1" in p), None)
            others = [p for p in files if p != flag]
            hoodie = others[0] if len(others) >= 1 else None
            mask   = others[1] if len(others) >= 2 else None

            for path, (rx, ry) in [(hoodie, (0.20, 0.55)),
                                   (mask,   (0.50, 0.55)),
                                   (flag,   (0.80, 0.55))]:
                if not path or not os.path.isfile(path):
                    continue
                img = load_photo(path)
                if img is None:
                    continue
                self.canvas.create_image(self.W * rx, self.H * ry,
                                         image=img, tags="photo")

        self.safe_after(3000, self.phase_emoji_explosion)

    def _try_set_hacker_wallpaper(self):
        candidates = []
        if os.path.isdir(ASSETS_DIR):
            candidates = [
                os.path.join(ASSETS_DIR, f)
                for f in os.listdir(ASSETS_DIR)
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp"))
                   and "images_1" not in f.lower()
            ]
        if not candidates:
            for ext in (".png", ".jpg", ".jpeg", ".bmp"):
                p = os.path.join(SCRIPT_DIR, f"wallpaper{ext}")
                if os.path.isfile(p):
                    candidates.append(p)
        if candidates:
            self.wallpaper.set_wallpaper(candidates[0])

    # -------------------------------------------------------------------------
    #  PHASE 6 — EMOJIS + SCREAMER
    # -------------------------------------------------------------------------
    def phase_emoji_explosion(self):
        self._emoji_wave()
        self.safe_after(2000, self.phase_slogan)
        for _ in range(3):
            self.safe_after(random.randint(500, 4000), self._screamer)

    def _emoji_wave(self):
        if self.exit_now:
            return
        for _ in range(25):
            x = random.randint(60, self.W - 60)
            y = random.randint(60, self.H - 60)
            emoji = random.choice(HACKER_EMOJIS)
            size = random.randint(24, 90)
            self.canvas.create_text(x, y, text=emoji,
                                    font=("Segoe UI Emoji", size),
                                    fill=random.choice(NEON_COLORS),
                                    tags="emoji")
        beep(1000, 30)
        self.safe_after(2000, self._emoji_wave)

    def _screamer(self):
        if self.exit_now:
            return
        emoji = random.choice(HACKER_EMOJIS)
        item = self.canvas.create_text(
            self.W / 2, self.H / 2, text=emoji,
            font=("Segoe UI Emoji", 320),
            fill="#ff0040", tags="scream"
        )
        beep(300, 400)
        self.safe_after(120, lambda: self.canvas.delete(item))

    # -------------------------------------------------------------------------
    #  PHASE 7 — SLOGAN + AUTO ROLLBACK
    # -------------------------------------------------------------------------
    def phase_slogan(self):
        self.label.config(text="WE  OWN  YOUR  SYSTEM",
                          fg="#ff0040",
                          font=("Consolas", 40, "bold"))
        self.sub_label.config(
            text="😈  Press ESC or Ctrl+Shift+Q to end  😈\n"
                 f"(auto-restore in {AUTO_ROLLBACK_MS//1000} seconds)",
            fg="#ffffff", font=("Consolas", 16, "bold")
        )
        self._glow_tick(0)

        if not self._rollback_scheduled:
            self._rollback_scheduled = True
            self.safe_after(AUTO_ROLLBACK_MS, self.close)

    def _glow_tick(self, i):
        if self.exit_now:
            return
        palette = ["#ff0040", "#ff3366", "#ff00ff", "#00ffff", "#ffffff"]
        self.label.config(fg=palette[i % len(palette)])
        self.safe_after(180, self._glow_tick, i + 1)

    # -------------------------------------------------------------------------
    #  CLEANUP / ROLLBACK
    # -------------------------------------------------------------------------
    def close(self, _event=None):
        if self.exit_now:
            return
        self.exit_now = True

        try:
            self.mouse.stop()
        except Exception:
            pass
        try:
            self.notepad.close()
        except Exception:
            pass
        try:
            self.wallpaper.restore()
        except Exception:
            pass
        try:
            self._stop_shots.set()
        except Exception:
            pass

        beep(500, 250)

        try:
            self.root.destroy()
        except Exception:
            pass

    # -------------------------------------------------------------------------
    def run(self):
        self.root.update_idletasks()
        self.root.after(150, self.root.focus_force)
        self.root.mainloop()


# =============================================================================
#  ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    print("=" * 65)
    print("  💀  CYBER APOCALYPSE — WINDOWS EDITION  💀")
    print("=" * 65)
    print(f"  Platform : {sys.platform}")
    print(f"  pyautogui: {'✅ OK' if HAS_PYAUTOGUI else '❌ missing  → pip install pyautogui'}")
    print(f"  Pillow   : {'✅ OK' if HAS_PIL else '❌ missing  → pip install pillow'}")
    print(f"  winsound : {'✅ OK' if HAS_WINSOUND else '❌ missing (غیر ویندوز؟)'}")
    print("=" * 65)
    print("  Starting in 3 seconds...  (press ESC to end early)")
    print("=" * 65)

    time.sleep(3)
    CyberApocalypse().run()

    print("\n[+] Prank ended. All systems restored to normal. 😇")
    print("    Wallpaper: restored")
    print("    Notepad  : closed")
    print("    Mouse    : released")