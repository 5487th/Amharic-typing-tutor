import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import customtkinter as ctk
from PIL import Image, ImageDraw
from tkinter import filedialog
from blinker import signal
from scripts.user_manager import UserManager, User
from scripts.language_manager import LanguageManager
from scripts.custom_widgets import *
import json
import time
import threading
import random
import math
import tkinter as tk
import sqlite3
import datetime

try:
    import winsound as _winsound

    _HAS_WINSOUND = True
except ImportError:
    _HAS_WINSOUND = False
from scripts.menus import Menu


# claude aided
class AmharicRainMenu(Menu):

    # ── Content ───────────────────────────────────────────────────────────────
    _LETTERS = list(
        "ሀሁሂሃሄህሆለሉሊላሌልሎሐሑሒሓሔሕሖመሙሚማሜምሞሠሡሢሣሤሥሦረሩሪራሬርሮሰሱሲሳሴስሶሸሹሺሻሼሽሾቀቁቂቃቄቅቆበቡቢባቤብቦቨቩቪቫቬቭቮተቱቲታቴትቶቸቹቺቻቼችቾኀኁኂኃኄኅኆነኑኒናኔንኖኘኙኚኛኜኝኞአኡኢኣኤእኦከኩኪካኬክኮኸኹኺኻኼኽኾወዉዊዋዌውዎዐዑዒዓዔዕዖዘዙዚዛዜዝዞዠዡዢዣዤዥዦየዩዪያዬይዮደዱዲዳዴድዶጀጁጂጃጄጅጆገጉጊጋጌግጎጠጡጢጣጤጥጦጨጩጪጫጬጭጮጰጱጲጳጴጵጶጸጹጺጻጼጽጾፀፁፂፃፄፅፆፈፉፊፋፌፍፎፐፑፒፓፔፕፖ"
    )
    _WORDS_DEFAULT = [
        "ሰላም",
        "ፍቅር",
        "ደስታ",
        "ሀገር",
        "ቤተሰብ",
        "ትምህርት",
        "ጸሐፊ",
        "ሙዚቃ",
        "ወርቅ",
        "ብርሃን",
        "ሰማይ",
        "ምድር",
        "ውሃ",
        "እሳት",
        "አየር",
        "አበባ",
        "ዛፍ",
        "ወንዝ",
        "ተራራ",
        "ሜዳ",
        "ቤት",
        "መንገድ",
        "ሰው",
        "ልጅ",
        "አባት",
        "እናት",
        "ወንድም",
        "እህት",
        "ጓደኛ",
        "አስተማሪ",
        "ተማሪ",
        "ዶክተር",
        "ቀን",
        "ሌሊት",
        "ጠዋት",
        "ምሽት",
        "ዓመት",
        "ወር",
        "ሳምንት",
        "ሰዓት",
        "ፀሐይ",
        "ጨረቃ",
        "ኮከብ",
        "ደመና",
        "ዝናብ",
        "ነፋስ",
        "በረዶ",
        "ሙቀት",
        "ስጋ",
        "ዳቦ",
        "ቡና",
        "ሻይ",
        "ወተት",
        "ፍሬ",
        "አትክልት",
        "ምግብ",
        "መጽሐፍ",
        "ብዕር",
        "ወረቀት",
        "ፊደል",
        "ቋንቋ",
        "ቃል",
    ]

    # ── Translations ──────────────────────────────────────────────────────────
    _T = {
        "en": {
            "title": "Amharic Rain",
            "subtitle": "Type the falling words before they hit the ground",
            "play": "Play",
            "settings": "Settings",
            "back_to_app": "Back",
            "mode_label": "Game Mode",
            "mode_letters": "Letters",
            "mode_words": "Words",
            "mode_both": "Both",
            "difficulty": "Difficulty",
            "diff_easy": "Easy",
            "diff_medium": "Medium",
            "diff_hard": "Hard",
            "volume": "Volume",
            "language": "Language",
            "lang_en": "English",
            "lang_am": "አማረኛ",
            "back": "Back",
            "score": "Score",
            "paused": "PAUSED",
            "resume": "Resume",
            "main_menu": "Main Menu",
            "game_over": "Game Over",
            "final_score": "Final Score",
            "play_again": "Play Again",
            "type_here": "Type here…",
            "pause": "Pause",
            "level": "Level",
            "lives": "Lives",
        },
        "am": {
            "title": "አማረኛ ዝናብ",
            "subtitle": "ቃላቱ ሳይወድቁ ጻፏቸው",
            "play": "ጀምር",
            "settings": "ቅንብሮች",
            "back_to_app": "ወደኋላ",
            "mode_label": "የጨዋታ ዓይነት",
            "mode_letters": "ፊደሎች",
            "mode_words": "ቃላት",
            "mode_both": "ሁለቱም",
            "difficulty": "ደረጃ",
            "diff_easy": "ቀላል",
            "diff_medium": "መካከለኛ",
            "diff_hard": "ከባድ",
            "volume": "ድምፅ",
            "language": "ቋንቋ",
            "lang_en": "English",
            "lang_am": "አማርኛ",
            "back": "ወደኋላ",
            "score": "ነጥብ",
            "paused": "ቆሟል",
            "resume": "ቀጥል",
            "main_menu": "ዋና ሜኒዩ",
            "game_over": "ጨዋታ አበቃ",
            "final_score": "የመጨረሻ ነጥብ",
            "play_again": "እንደገና ተጫወት",
            "type_here": "እዚህ ይጻፉ…",
            "pause": "አቁም",
            "level": "ደረጃ",
            "lives": "ህይወት",
        },
    }

    # ── Difficulty presets ────────────────────────────────────────────────────
    _DIFFICULTY = {
        "easy": {
            "start_speed": 0.55,
            "speed_inc": 0.015,
            "spawn_rate": 2.8,
            "spawn_dec": 0.08,
            "min_spawn": 1.2,
            "lives": 7,
        },
        "medium": {
            "start_speed": 0.85,
            "speed_inc": 0.025,
            "spawn_rate": 2.2,
            "spawn_dec": 0.12,
            "min_spawn": 0.8,
            "lives": 5,
        },
        "hard": {
            "start_speed": 1.20,
            "speed_inc": 0.040,
            "spawn_rate": 1.6,
            "spawn_dec": 0.18,
            "min_spawn": 0.5,
            "lives": 3,
        },
    }

    _INITIAL_SCORE = 25
    _SCORE_GAIN = 5
    _SCORE_LOSS = 4

    # ── Boss word constants ───────────────────────────────────────────────────
    _BOSS_COLOR = "#FFD700"  # gold
    _BOSS_OUTLINE = "#FF8C00"  # dark-orange glow shadow
    _BOSS_HIT_COLOR = "#FFF176"  # bright flash per hit
    _BOSS_FONT = ("Ebrima", 24, "bold")
    _BOSS_CHANCE = 0.15  # 15 % per spawn cycle
    _BOSS_SPEED_MULT = 0.90  # falls at 90 % of normal speed
    _BOSS_HITS = 3
    _HIT_DIGITS = ["❶", "❷", "❸", "❹", "❺"]

    # ── Palette ───────────────────────────────────────────────────────────────
    _BG_DARK = "#0a0d18"
    _BG_MID = "#131929"
    _BG_CARD = "#1c2240"
    _ACCENT = "#7c8cff"
    _ACCENT2 = "#a78bfa"
    _GREEN = "#4ade80"
    _RED = "#f87171"
    _TEXT_MAIN = "#e8eaf6"
    _TEXT_DIM = "#7b7fa8"
    _INPUT_BG = "#111827"
    _WORD_COLORS = [
        "#7c8cff",
        "#a78bfa",
        "#67e8f9",
        "#4ade80",
        "#fbbf24",
        "#fb7185",
        "#38bdf8",
        "#c084fc",
    ]

    # ── Fonts ─────────────────────────────────────────────────────────────────
    _F_TITLE = ("Segoe UI", 42, "bold")
    _F_SUBTITLE = ("Segoe UI", 15)
    _F_BTN = ("Segoe UI", 16, "bold")
    _F_LABEL = ("Segoe UI", 14)
    _F_WORD = ("Ebrima", 26, "bold")
    _F_WORD_SM = ("Ebrima", 20, "bold")
    _F_HUD = ("Segoe UI", 16, "bold")
    _F_INPUT = ("Ebrima", 22)
    _F_BIG = ("Segoe UI", 64, "bold")

    _STARS: list = []

    # ─────────────────────────────────────────────────────────────────────────

    def __init__(self, language_manager=None):
        self.language_manager = language_manager
        self.on_back_button_pressed = signal(f"amharic_rain_back_{id(self)}")

        self.lang = (
            "am" if getattr(language_manager, "current_lang", "en") == "am" else "en"
        )
        self.mode = "both"
        self.difficulty = "medium"
        self.volume = 0.7

        # Per-difficulty word banks; fall back to _WORDS_DEFAULT for any missing key
        self._word_bank: dict = {"easy": [], "medium": [], "hard": []}

        self.root = None  # set in open_menu(root)
        self.score = self._INITIAL_SCORE
        self.lives = 5
        self.level = 1
        self._paused = False
        self._running = False
        self._items: list = []
        self._boss: dict | None = None
        self._spawn_timer = 0.0
        self._level_timer = 0.0
        self._current_speed = 1.0
        self._spawn_interval = 2.0
        self._last_tick = 0.0
        self._tag_counter = 0
        self._pause_overlay_shown = False
        self._pause_frame = None
        self._pause_dim = None
        self._game_area = None
        self._sounds: dict = {}
        self._snd_ready = False

        self.main_frame = None
        self._canvas = None
        self._input_var = None
        self._input_entry = None
        self._score_label = None
        self._level_label = None
        self._lives_label = None
        self._pause_btn = None

    # ── Word bank API ─────────────────────────────────────────────────────────

    def load_word_bank(self, path: str) -> bool:
        """
        Load words from a JSON file.
        Expected format: {"easy": [...], "medium": [...], "hard": [...]}
        Any missing difficulty key falls back to _WORDS_DEFAULT at runtime.
        Returns True on success, False on failure.
        """
        import json

        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if isinstance(data, dict):
                for diff in ("easy", "medium", "hard"):
                    words = data.get(diff, [])
                    self._word_bank[diff] = [str(w) for w in words if str(w).strip()]
                return True
        except Exception as exc:
            print(f"[AmharicRain] load_word_bank failed: {exc}")
        self._word_bank = {"easy": [], "medium": [], "hard": []}
        return False

    def set_word_bank(self, bank: dict) -> None:
        """
        Directly set the word bank from a dict.
        Expected: {"easy": [...], "medium": [...], "hard": [...]}
        """
        for diff in ("easy", "medium", "hard"):
            words = bank.get(diff, []) if isinstance(bank, dict) else []
            self._word_bank[diff] = [str(w) for w in words if str(w).strip()]

    def _words_for_difficulty(self) -> list:
        """Return the word list for the current difficulty, falling back to the built-in default."""
        return self._word_bank.get(self.difficulty) or list(self._WORDS_DEFAULT)

    # ── Menu protocol (overrides Menu base) ──────────────────────────────────

    def open_menu(self, root):
        self.root = root
        if not self.main_frame:
            self.main_frame = ctk.CTkFrame(
                self.root, fg_color=self._BG_DARK, corner_radius=0
            )
        self.main_frame.place(
            relwidth=1, relheight=1, relx=0.5, rely=0.5, anchor="center"
        )
        self._show_game_menu()
        self.root.update_idletasks()

    def close_menu(self):
        self._running = False
        if self.main_frame:
            self.main_frame.place_forget()
        if self.root:
            self.root.update_idletasks()

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _t(self, key: str) -> str:
        return self._T[self.lang].get(key, key)

    def _clear(self):
        self._running = False
        for attr in ("_pause_frame", "_pause_dim"):
            w = getattr(self, attr, None)
            if w and w.winfo_exists():
                w.destroy()
            setattr(self, attr, None)
        self._game_area = None
        if self.main_frame:
            for w in self.main_frame.winfo_children():
                w.destroy()
        self._canvas = self._input_var = self._input_entry = None
        self._score_label = self._level_label = self._lives_label = self._pause_btn = (
            None
        )
        self._pause_overlay_shown = False

    def _exit_to_app(self):
        self.on_back_button_pressed.send(self)

    # ── Night-sky star field ──────────────────────────────────────────────────

    def _build_stars(self, w: int, h: int):
        import random as _r

        rng = _r.Random(42)
        self._STARS = []
        for _ in range(200):
            self._STARS.append(
                (rng.randint(0, w), rng.randint(0, h), 1, rng.uniform(0.3, 1.0))
            )
        for _ in range(30):
            self._STARS.append(
                (rng.randint(0, w), rng.randint(0, h), 2, rng.uniform(0.5, 1.0))
            )
        for _ in range(5):
            self._STARS.append((rng.randint(0, w), rng.randint(0, h), 3, 1.0))

    def _draw_stars(self, canvas):
        canvas.delete("stars")
        w = canvas.winfo_width() or 800
        h = canvas.winfo_height() or 600
        if not self._STARS:
            self._build_stars(w, h)
        for sx, sy, sz, alpha in self._STARS:
            v = int(alpha * 220) + 35
            color = f"#{v:02x}{v:02x}{min(255, v + 30):02x}"
            r = sz
            canvas.create_oval(
                sx - r, sy - r, sx + r, sy + r, fill=color, outline="", tags="stars"
            )

    # ══════════════════════════════════════════════════════════
    #  SOUND ENGINE
    # ══════════════════════════════════════════════════════════

    def _init_sound(self):
        if self._snd_ready:
            return
        try:
            import pygame
            import numpy as np

            if not pygame.mixer.get_init():
                pygame.mixer.pre_init(
                    frequency=44100, size=-16, channels=2, buffer=2048
                )
                pygame.mixer.init()
            if not pygame.mixer.get_init():
                return
            self._pg_mixer = pygame.mixer
            self._np = np
            self._sounds = {
                # gameplay
                "key": self._make_tone(880, 0.055, "sine", decay=0.5),
                "match": self._make_chord([523, 659, 784], 0.35, decay=0.45),
                "wrong": self._make_tone(180, 0.22, "square", decay=0.6),
                "miss": self._make_tone(220, 0.28, "sine", decay=0.7),
                "levelup": self._make_arp([523, 659, 784, 1047], 0.12),
                "gameover": self._make_arp([523, 440, 392, 294], 0.22, descend=True),
                # UI
                "btn": self._make_tone(660, 0.07, "sine", decay=0.8),
                "back": self._make_tone(440, 0.09, "sine", decay=0.7),
                "seg": self._make_tone(740, 0.06, "sine", decay=0.9),
                "slider": self._make_tone(1100, 0.035, "sine", decay=1.2),
            }
            pygame.mixer.set_num_channels(16)
            self._snd_ready = True
        except Exception:
            import traceback

            traceback.print_exc()
            self._snd_ready = False

    def _make_tone(self, freq, duration, shape="sine", decay=0.5, volume=0.6):
        try:
            import numpy as np, pygame

            sr = 44100
            n = int(sr * duration)
            t = np.linspace(0, duration, n, endpoint=False)
            if shape == "sine":
                wave = np.sin(2 * np.pi * freq * t)
            elif shape == "square":
                wave = np.sign(np.sin(2 * np.pi * freq * t)) * 0.5
            elif shape == "saw":
                wave = 2 * (t * freq - np.floor(t * freq + 0.5))
            else:
                wave = np.sin(2 * np.pi * freq * t)
            env = np.exp(-decay * t / max(duration, 1e-9) * 6)
            mono = (wave * env * volume * 32767).astype(np.int16)
            stereo = np.ascontiguousarray(np.column_stack([mono, mono]))
            return pygame.sndarray.make_sound(stereo)
        except Exception:
            return None

    def _make_chord(self, freqs, duration, decay=0.5, volume=0.45):
        try:
            import numpy as np, pygame

            sr = 44100
            t = np.linspace(0, duration, int(sr * duration), endpoint=False)
            wave = sum(np.sin(2 * np.pi * f * t) for f in freqs) / len(freqs)
            env = np.exp(-decay * t / max(duration, 1e-9) * 6)
            mono = (wave * env * volume * 32767).astype(np.int16)
            stereo = np.ascontiguousarray(np.column_stack([mono, mono]))
            return pygame.sndarray.make_sound(stereo)
        except Exception:
            return None

    def _make_arp(self, freqs, note_dur, descend=False, volume=0.55):
        try:
            import numpy as np, pygame

            sr = 44100
            samples = []
            for freq in freqs:
                t = np.linspace(0, note_dur, int(sr * note_dur), endpoint=False)
                wave = np.sin(2 * np.pi * freq * t)
                env = np.exp(-4 * t / max(note_dur, 1e-9))
                samples.append(wave * env)
            mono = (np.concatenate(samples) * volume * 32767).astype(np.int16)
            stereo = np.ascontiguousarray(np.column_stack([mono, mono]))
            return pygame.sndarray.make_sound(stereo)
        except Exception:
            return None

    def _on_volume_change(self, v: float, label):
        self.volume = v / 100
        label.configure(text=f"{int(v)}%")
        self._snd("slider")

    def _snd(self, name: str):
        if not self._snd_ready:
            return
        snd = self._sounds.get(name)
        if snd:
            try:
                vol = max(0.01, self.volume * 0.85)
                snd.set_volume(vol)
                ch = self._pg_mixer.find_channel(False)
                if ch:
                    ch.set_volume(vol)
                    ch.play(snd)
                else:
                    snd.play()
            except Exception:
                pass

    # ── Widget factories with built-in sounds ─────────────────────────────────

    def _btn(self, parent, *, sound="btn", command=None, **kwargs) -> ctk.CTkButton:
        def _cmd():
            self._snd(sound)
            if command:
                command()

        return ctk.CTkButton(parent, command=_cmd, **kwargs)

    def _seg(self, parent, *, on_change=None, **kwargs) -> ctk.CTkSegmentedButton:
        def _cmd(v):
            self._snd("seg")
            if on_change:
                on_change(v)

        return ctk.CTkSegmentedButton(parent, command=_cmd, **kwargs)

    # ══════════════════════════════════════════════════════════
    #  SCREENS
    # ══════════════════════════════════════════════════════════

    def _show_game_menu(self):
        self._clear()
        self._init_sound()

        bg_canvas = tk.Canvas(self.main_frame, bg=self._BG_DARK, highlightthickness=0)
        bg_canvas.place(relwidth=1, relheight=1)
        bg_canvas.update_idletasks()
        self._draw_stars(bg_canvas)
        bg_canvas.bind("<Configure>", lambda e, c=bg_canvas: self._draw_stars(c))

        outer = ctk.CTkFrame(self.main_frame, fg_color="transparent", corner_radius=0)
        outer.place(relwidth=1, relheight=1)
        outer.grid_rowconfigure(0, weight=1)
        outer.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(
            outer,
            fg_color=self._BG_MID,
            corner_radius=24,
            border_width=1,
            border_color=self._BG_CARD,
            bg_color="transparent",
        )
        card.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")
        card.grid_rowconfigure(list(range(8)), weight=1)
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkFrame(card, fg_color=self._ACCENT, height=6, corner_radius=3).grid(
            row=0, column=0, padx=60, pady=(32, 0), sticky="ew"
        )
        ctk.CTkLabel(
            card, text=self._t("title"), font=self._F_TITLE, text_color=self._TEXT_MAIN
        ).grid(row=1, column=0, pady=(18, 2))
        ctk.CTkLabel(
            card,
            text=self._t("subtitle"),
            font=self._F_SUBTITLE,
            text_color=self._TEXT_DIM,
        ).grid(row=2, column=0, pady=(0, 24))

        _b = dict(
            width=260, height=52, corner_radius=14, font=self._F_BTN, text_color="#fff"
        )
        self._btn(
            card,
            text=self._t("play"),
            command=self._show_setup,
            fg_color=self._ACCENT,
            hover_color="#5a6bff",
            sound="btn",
            **_b,
        ).grid(row=3, column=0, pady=8)
        self._btn(
            card,
            text=self._t("settings"),
            command=self._show_settings,
            fg_color=self._BG_CARD,
            hover_color="#2e3354",
            sound="btn",
            **_b,
        ).grid(row=4, column=0, pady=8)
        self._btn(
            card,
            text=self._t("back_to_app"),
            command=self._exit_to_app,
            fg_color="#2d1f2f",
            hover_color="#3d2040",
            sound="back",
            **_b,
        ).grid(row=5, column=0, pady=8)

        lang_row = ctk.CTkFrame(card, fg_color="transparent")
        lang_row.grid(row=6, column=0, pady=(16, 28))
        ctk.CTkLabel(
            lang_row,
            text=self._t("language") + ":",
            font=self._F_LABEL,
            text_color=self._TEXT_DIM,
        ).pack(side="left", padx=8)

        def _lang_change(v):
            self._snd("seg")
            self.lang = "am" if v in ("አማርኛ", "አማረኛ") else "en"
            self._show_game_menu()

        ctk.CTkSegmentedButton(
            lang_row,
            values=[self._t("lang_en"), self._t("lang_am")],
            command=_lang_change,
            font=self._F_LABEL,
            selected_color=self._ACCENT,
            selected_hover_color="#5a6bff",
            unselected_color=self._BG_CARD,
            fg_color=self._BG_CARD,
        ).pack(side="left")

    def _show_settings(self):
        self._clear()

        bg_canvas = tk.Canvas(self.main_frame, bg=self._BG_DARK, highlightthickness=0)
        bg_canvas.place(relwidth=1, relheight=1)
        bg_canvas.update_idletasks()
        self._draw_stars(bg_canvas)
        bg_canvas.bind("<Configure>", lambda e, c=bg_canvas: self._draw_stars(c))

        outer = ctk.CTkFrame(self.main_frame, fg_color="transparent", corner_radius=0)
        outer.place(relwidth=1, relheight=1)
        outer.grid_rowconfigure(0, weight=1)
        outer.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(
            outer,
            fg_color=self._BG_MID,
            corner_radius=24,
            border_width=1,
            border_color=self._BG_CARD,
            bg_color="transparent",
        )
        card.grid(row=0, column=0, padx=60, pady=40, sticky="nsew")
        card.grid_columnconfigure(1, weight=1)

        def row_label(r, key):
            ctk.CTkLabel(
                card,
                text=self._t(key) + ":",
                font=self._F_LABEL,
                text_color=self._TEXT_DIM,
                anchor="e",
            ).grid(row=r, column=0, padx=(30, 12), pady=18, sticky="e")

        ctk.CTkLabel(
            card,
            text=self._t("settings"),
            font=self._F_TITLE,
            text_color=self._TEXT_MAIN,
        ).grid(row=0, column=0, columnspan=2, pady=(28, 8))

        row_label(1, "volume")
        vol_var = ctk.DoubleVar(value=self.volume * 100)
        vol_label = ctk.CTkLabel(
            card,
            text=f"{int(self.volume * 100)}%",
            font=self._F_LABEL,
            text_color=self._TEXT_MAIN,
        )
        vol_label.grid(row=1, column=2, padx=(0, 20))
        ctk.CTkSlider(
            card,
            from_=0,
            to=100,
            variable=vol_var,
            width=280,
            button_color=self._ACCENT,
            button_hover_color="#5a6bff",
            progress_color=self._ACCENT,
            command=lambda v: self._on_volume_change(float(v), vol_label),
        ).grid(row=1, column=1, padx=(0, 30), sticky="w")

        row_label(2, "language")

        def _on_lang_change(v):
            self._snd("seg")
            self.lang = "am" if v in ("አማርኛ", "አማረኛ", "Amharic") else "en"
            self._show_settings()

        lang_seg = ctk.CTkSegmentedButton(
            card,
            values=["English", "አማርኛ"],
            font=self._F_LABEL,
            selected_color=self._ACCENT,
            selected_hover_color="#5a6bff",
            unselected_color=self._BG_CARD,
            fg_color=self._BG_CARD,
            command=_on_lang_change,
        )
        lang_seg.set("አማርኛ" if self.lang == "am" else "English")
        lang_seg.grid(row=2, column=1, padx=(0, 30), sticky="w", pady=18)

        self._btn(
            card,
            text=self._t("back"),
            command=self._show_game_menu,
            width=200,
            height=48,
            corner_radius=14,
            font=self._F_BTN,
            fg_color=self._BG_CARD,
            hover_color="#2e3354",
            text_color=self._TEXT_MAIN,
            sound="back",
        ).grid(row=8, column=0, columnspan=3, pady=(18, 32))

    def _show_setup(self):
        self._clear()

        bg_canvas = tk.Canvas(self.main_frame, bg=self._BG_DARK, highlightthickness=0)
        bg_canvas.place(relwidth=1, relheight=1)
        bg_canvas.update_idletasks()
        self._draw_stars(bg_canvas)
        bg_canvas.bind("<Configure>", lambda e, c=bg_canvas: self._draw_stars(c))

        outer = ctk.CTkFrame(self.main_frame, fg_color="transparent", corner_radius=0)
        outer.place(relwidth=1, relheight=1)
        outer.grid_rowconfigure(0, weight=1)
        outer.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(
            outer,
            fg_color=self._BG_MID,
            corner_radius=24,
            border_width=1,
            border_color=self._BG_CARD,
            bg_color="transparent",
        )
        card.grid(row=0, column=0, padx=60, pady=40, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card, text=self._t("play"), font=self._F_TITLE, text_color=self._TEXT_MAIN
        ).grid(row=0, column=0, pady=(28, 8))
        ctk.CTkLabel(
            card,
            text=self._t("mode_label"),
            font=self._F_LABEL,
            text_color=self._TEXT_DIM,
        ).grid(row=1, column=0, pady=(12, 4))

        def _on_mode(v):
            self._snd("seg")
            self.mode = (
                "letters"
                if v in (self._t("mode_letters"), "Letters", "ፊደሎች")
                else "words" if v in (self._t("mode_words"), "Words", "ቃላት") else "both"
            )

        mode_seg = ctk.CTkSegmentedButton(
            card,
            values=[
                self._t("mode_letters"),
                self._t("mode_words"),
                self._t("mode_both"),
            ],
            font=self._F_BTN,
            selected_color=self._ACCENT,
            selected_hover_color="#5a6bff",
            unselected_color=self._BG_CARD,
            fg_color=self._BG_CARD,
            command=_on_mode,
        )
        mode_seg.set(self._t(f"mode_{self.mode}"))
        mode_seg.grid(row=2, column=0, padx=40, pady=(4, 20), sticky="ew")

        ctk.CTkLabel(
            card,
            text=self._t("difficulty"),
            font=self._F_LABEL,
            text_color=self._TEXT_DIM,
        ).grid(row=3, column=0, pady=(0, 4))

        def _on_diff(v):
            self._snd("seg")
            self.difficulty = (
                "easy"
                if v in (self._t("diff_easy"), "Easy", "ቀላል")
                else "hard" if v in (self._t("diff_hard"), "Hard", "ከባድ") else "medium"
            )

        diff_seg = ctk.CTkSegmentedButton(
            card,
            values=[self._t("diff_easy"), self._t("diff_medium"), self._t("diff_hard")],
            font=self._F_BTN,
            selected_color=self._ACCENT2,
            selected_hover_color="#7c5bfa",
            unselected_color=self._BG_CARD,
            fg_color=self._BG_CARD,
            command=_on_diff,
        )
        diff_seg.set(self._t(f"diff_{self.difficulty}"))
        diff_seg.grid(row=4, column=0, padx=40, pady=(4, 32), sticky="ew")

        _b = dict(
            width=240, height=52, corner_radius=14, font=self._F_BTN, text_color="#fff"
        )
        self._btn(
            card,
            text=self._t("play"),
            command=self._start_game,
            fg_color=self._ACCENT,
            hover_color="#5a6bff",
            sound="btn",
            **_b,
        ).grid(row=5, column=0, pady=6)
        self._btn(
            card,
            text=self._t("back"),
            command=self._show_game_menu,
            fg_color=self._BG_CARD,
            hover_color="#2e3354",
            sound="back",
            **_b,
        ).grid(row=6, column=0, pady=(6, 32))

    # ══════════════════════════════════════════════════════════
    #  GAME
    # ══════════════════════════════════════════════════════════

    def _start_game(self):
        self._boss = None
        self._items.clear()
        self.score = self._INITIAL_SCORE
        self.lives = self._DIFFICULTY[self.difficulty]["lives"]
        self.level = 1
        self._paused = False
        self._tag_counter = 0
        self._pause_overlay_shown = False
        d = self._DIFFICULTY[self.difficulty]
        self._current_speed = d["start_speed"]
        self._spawn_interval = d["spawn_rate"]
        self._spawn_timer = 0.0
        self._level_timer = 0.0
        self._last_tick = time.time()
        self._clear()
        self._running = True
        self._init_sound()
        self._build_game_ui()
        self._tick()

    def _build_game_ui(self):
        outer = self.main_frame
        for i in range(3):
            outer.grid_rowconfigure(i, weight=1 if i == 1 else 0)
        outer.grid_columnconfigure(0, weight=1)

        hud = ctk.CTkFrame(outer, fg_color=self._BG_MID, height=56, corner_radius=0)
        hud.grid(row=0, column=0, sticky="ew")
        hud.grid_columnconfigure(2, weight=1)
        hud.grid_propagate(False)

        self._score_label = ctk.CTkLabel(
            hud,
            text=f"{self._t('score')}: {self.score}",
            font=self._F_HUD,
            text_color=self._GREEN,
        )
        self._score_label.grid(row=0, column=0, padx=24, pady=12, sticky="w")

        self._level_label = ctk.CTkLabel(
            hud,
            text=f"{self._t('level')}: {self.level}",
            font=self._F_HUD,
            text_color=self._ACCENT,
        )
        self._level_label.grid(row=0, column=1, padx=12, pady=12, sticky="w")

        self._lives_label = ctk.CTkLabel(
            hud, text="♥ " * self.lives, font=("Segoe UI", 15), text_color=self._RED
        )
        self._lives_label.grid(row=0, column=2, padx=12, pady=12, sticky="w")

        self._pause_btn = self._btn(
            hud,
            text=self._t("pause"),
            command=self._toggle_pause,
            width=110,
            height=34,
            corner_radius=10,
            font=("Segoe UI", 13, "bold"),
            fg_color=self._BG_CARD,
            hover_color="#2e3354",
            text_color=self._TEXT_MAIN,
            sound="btn",
        )
        self._pause_btn.grid(row=0, column=3, padx=(0, 20), pady=10, sticky="e")

        self._game_area = ctk.CTkFrame(outer, fg_color=self._BG_DARK, corner_radius=0)
        self._game_area.grid(row=1, column=0, sticky="nsew")
        self._game_area.grid_rowconfigure(0, weight=1)
        self._game_area.grid_columnconfigure(0, weight=1)

        self._canvas = tk.Canvas(
            self._game_area, bg=self._BG_DARK, highlightthickness=0
        )
        self._canvas.grid(row=0, column=0, sticky="nsew")

        def _on_canvas_configure(e):
            self._STARS = []
            self._draw_stars(self._canvas)
            self._draw_danger_line()

        self._canvas.bind("<Configure>", _on_canvas_configure)
        self._canvas.after(
            50, lambda: (self._draw_stars(self._canvas), self._draw_danger_line())
        )

        inp = ctk.CTkFrame(outer, fg_color=self._BG_MID, height=68, corner_radius=0)
        inp.grid(row=2, column=0, sticky="ew")
        inp.grid_columnconfigure(0, weight=1)
        inp.grid_propagate(False)

        self._input_var = tk.StringVar()
        self._input_var.trace_add("write", self._on_input_change)

        self._input_entry = ctk.CTkEntry(
            inp,
            textvariable=self._input_var,
            placeholder_text=self._t("type_here"),
            font=self._F_INPUT,
            fg_color=self._INPUT_BG,
            border_color=self._ACCENT,
            border_width=2,
            text_color=self._TEXT_MAIN,
            corner_radius=12,
            height=46,
        )
        self._input_entry.grid(row=0, column=0, padx=24, pady=11, sticky="ew")
        self._input_entry.focus()
        self._input_entry.bind("<Return>", lambda e: self._submit_input())

    def _draw_danger_line(self):
        if not self._canvas or not self._canvas.winfo_exists():
            return
        w, h = self._canvas.winfo_width(), self._canvas.winfo_height()
        self._canvas.delete("dangerline")
        self._canvas.create_line(
            0,
            h - 72,
            w,
            h - 72,
            fill=self._RED,
            width=2,
            dash=(8, 6),
            tags="dangerline",
        )

    # ── Input handling ────────────────────────────────────────────────────────

    def _on_input_change(self, *_):
        if not self._running or self._paused or not self._canvas:
            return
        typed = self._input_var.get()
        if typed:
            self._snd("key")

        for item in self._items:
            color = (
                self._GREEN
                if (not item["matched"] and item["text"].startswith(typed) and typed)
                else item["color"]
            )
            self._canvas.itemconfig(item["tag"], fill=color)

        if self._boss and typed:
            color = (
                self._BOSS_HIT_COLOR
                if self._boss["text"].startswith(typed)
                else self._BOSS_COLOR
            )
            self._canvas.itemconfig(self._boss["tag"], fill=color)

    def _submit_input(self):
        typed = self._input_var.get().strip()
        if not typed:
            return

        # Boss check first
        if self._boss and self._boss["text"] == typed:
            self._boss["hits"] += 1
            hits = self._boss["hits"]
            if hits >= self._BOSS_HITS:
                self._boss_success()
            else:
                new_label = self._boss_label(self._boss["text"], hits)
                for t in (
                    self._boss["tag"],
                    self._boss["glow_tag"],
                    self._boss["glow_tag2"],
                ):
                    try:
                        self._canvas.itemconfig(t, text=new_label)
                    except Exception:
                        pass
                self._flash_boss_hit()
                self._snd("match")
            self._input_var.set("")
            return

        # Normal items
        matched = False
        for item in list(self._items):
            if item["text"] == typed:
                self._items.remove(item)
                self._canvas.delete(item["tag"])
                self.score += self._SCORE_GAIN
                self._update_hud()
                self._spawn_burst(item["x"], item["y"], item["color"])
                self._snd("match")
                matched = True
                break
        if not matched:
            self._snd("wrong")
        self._input_var.set("")

    # ── Particles ─────────────────────────────────────────────────────────────

    def _spawn_burst(self, x: float, y: float, color: str):
        for _ in range(8):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(20, 60)
            dx, dy = math.cos(angle) * speed, math.sin(angle) * speed
            tag = f"p_{time.time()}_{random.random()}"
            r = random.randint(3, 7)
            self._canvas.create_oval(
                x - r, y - r, x + r, y + r, fill=color, outline="", tags=tag
            )
            self._anim_particle(tag, x, y, dx, dy, 6)

    def _anim_particle(self, tag, x, y, dx, dy, steps):
        if not self._canvas or not self._canvas.winfo_exists() or steps <= 0:
            self._canvas and self._canvas.delete(tag)
            return
        nx, ny = x + dx * 0.15, y + dy * 0.15
        self._canvas.move(tag, dx * 0.15, dy * 0.15)
        self._canvas.after(
            25,
            lambda: self._anim_particle(
                tag, nx, ny, dx * 0.85, dy * 0.85 + 2, steps - 1
            ),
        )

    # ══════════════════════════════════════════════════════════
    #  BOSS WORDS
    # ══════════════════════════════════════════════════════════

    def _boss_label(self, text: str, hits: int) -> str:
        filled = "".join(self._HIT_DIGITS[i] for i in range(hits))
        remaining = "○" * (self._BOSS_HITS - hits)
        return f"★ {text}  {filled}{remaining}"

    def _spawn_boss(self, canvas_w: int):
        words = self._words_for_difficulty()
        pool = [w for w in words if len(w) >= 3] or words
        text = random.choice(pool)

        x = random.randint(60, max(61, canvas_w - 60))
        self._tag_counter += 1
        base_tag = f"boss_{self._tag_counter}"
        glow_tag = f"bossglow_{self._tag_counter}"
        glow_tag2 = f"bossglow2_{self._tag_counter}"

        label = self._boss_label(text, 0)

        self._canvas.create_text(
            x + 2,
            -28,
            text=label,
            font=self._BOSS_FONT,
            fill=self._BOSS_OUTLINE,
            tags=glow_tag2,
            anchor="center",
        )
        self._canvas.create_text(
            x,
            -30,
            text=label,
            font=self._BOSS_FONT,
            fill=self._BOSS_OUTLINE,
            tags=glow_tag,
            anchor="center",
        )
        self._canvas.create_text(
            x,
            -30,
            text=label,
            font=self._BOSS_FONT,
            fill=self._BOSS_COLOR,
            tags=base_tag,
            anchor="center",
        )

        self._boss = {
            "text": text,
            "x": float(x),
            "y": -30.0,
            "speed": self._current_speed * self._BOSS_SPEED_MULT,
            "hits": 0,
            "tag": base_tag,
            "glow_tag": glow_tag,
            "glow_tag2": glow_tag2,
        }

    def _boss_success(self):
        if not self._boss:
            return
        bx, by = self._boss["x"], self._boss["y"]
        self._remove_boss_canvas_items()
        self._boss = None

        self.lives = min(self.lives + 1, 10)
        self._update_hud()
        self._spawn_burst(bx, by, self._BOSS_COLOR)
        self._spawn_burst(bx - 20, by + 10, self._BOSS_HIT_COLOR)
        self._spawn_burst(bx + 20, by + 10, self._BOSS_HIT_COLOR)
        self._snd("levelup")

        try:
            self._lives_label.configure(text_color=self._BOSS_COLOR)
            self.root.after(
                600,
                lambda: (
                    self._lives_label.configure(text_color=self._RED)
                    if self._lives_label and self._lives_label.winfo_exists()
                    else None
                ),
            )
        except Exception:
            pass

    def _boss_miss(self, boss: dict):
        """Boss reached the danger line — disappear silently, no penalty."""
        self._remove_boss_canvas_items(boss)
        if self._boss is boss:
            self._boss = None

    def _remove_boss_canvas_items(self, boss: dict | None = None):
        b = boss if boss is not None else self._boss
        if b is None:
            return
        for key in ("tag", "glow_tag", "glow_tag2"):
            try:
                self._canvas.delete(b[key])
            except Exception:
                pass

    def _flash_boss_hit(self):
        if not self._boss:
            return
        try:
            self._canvas.itemconfig(self._boss["tag"], fill=self._BOSS_HIT_COLOR)
            tag = self._boss["tag"]
            self.root.after(
                180,
                lambda: (
                    self._canvas.itemconfig(tag, fill=self._BOSS_COLOR)
                    if self._canvas and self._canvas.winfo_exists()
                    else None
                ),
            )
        except Exception:
            pass

    # ══════════════════════════════════════════════════════════
    #  GAME LOOP
    # ══════════════════════════════════════════════════════════

    def _tick(self):
        if not self._running:
            return
        now = time.time()
        dt = now - self._last_tick
        self._last_tick = now

        if self._paused:
            self.root.after(50, self._tick)
            return

        if not self._canvas or not self._canvas.winfo_exists():
            return

        w, h = self._canvas.winfo_width(), self._canvas.winfo_height()
        danger_y = h - 72

        self._spawn_timer += dt
        if self._spawn_timer >= self._spawn_interval:
            self._spawn_timer = 0.0
            self._spawn_item(w)

        self._level_timer += dt
        if self._level_timer >= 20.0:
            self._level_timer = 0.0
            self._level_up()

        fallen = []
        for item in self._items:
            item["y"] += item["speed"] * dt * 60
            self._canvas.coords(item["tag"], item["x"], item["y"])
            if item["y"] >= danger_y:
                fallen.append(item)

        for item in fallen:
            self._items.remove(item)
            self._canvas.delete(item["tag"])
            self.lives = max(0, self.lives - 1)
            self._update_hud()
            self._flash_score()
            self._snd("miss")

        if self._boss:
            self._boss["y"] += self._boss["speed"] * dt * 60
            ny, nx = self._boss["y"], self._boss["x"]
            self._canvas.coords(self._boss["tag"], nx, ny)
            self._canvas.coords(self._boss["glow_tag"], nx, ny)
            self._canvas.coords(self._boss["glow_tag2"], nx + 2, ny - 2)
            if ny >= danger_y:
                self._boss_miss(self._boss)

        if self.lives <= 0:
            self._game_over()
            return

        self.root.after(16, self._tick)

    def _spawn_item(self, canvas_w: int):
        if canvas_w < 10:
            return

        if self._boss is None and random.random() < self._BOSS_CHANCE:
            self._spawn_boss(canvas_w)
            return

        words = self._words_for_difficulty()
        if self.mode == "letters":
            text, font = random.choice(self._LETTERS), self._F_WORD
        elif self.mode == "words":
            text, font = random.choice(words), self._F_WORD_SM
        else:
            if random.random() < 0.45:
                text, font = random.choice(self._LETTERS), self._F_WORD
            else:
                text, font = random.choice(words), self._F_WORD_SM

        x = random.randint(40, max(41, canvas_w - 40))
        color = random.choice(self._WORD_COLORS)
        self._tag_counter += 1
        tag = f"item_{self._tag_counter}"
        self._canvas.create_text(
            x, -30, text=text, font=font, fill=color, tags=tag, anchor="center"
        )
        self._items.append(
            {
                "text": text,
                "x": float(x),
                "y": -30.0,
                "speed": self._current_speed,
                "color": color,
                "tag": tag,
                "matched": False,
            }
        )

    def _level_up(self):
        self.level += 1
        d = self._DIFFICULTY[self.difficulty]
        self._current_speed = min(
            self._current_speed + d["speed_inc"] * self.level, 4.5
        )
        self._spawn_interval = max(
            self._spawn_interval - d["spawn_dec"], d["min_spawn"]
        )
        self._update_hud()
        self._flash_level()
        self._snd("levelup")

    def _update_hud(self):
        if self._score_label and self._score_label.winfo_exists():
            self._score_label.configure(
                text=f"{self._t('score')}: {self.score}",
                text_color=self._GREEN if self.score > 0 else self._RED,
            )
            self._level_label.configure(text=f"{self._t('level')}: {self.level}")
            if self._lives_label and self._lives_label.winfo_exists():
                hearts = ("♥ " * self.lives).strip() or "☆"
                self._lives_label.configure(
                    text=hearts, text_color=self._RED if self.lives > 1 else "#ff4444"
                )

    def _flash_score(self):
        lbl = self._score_label
        if not lbl:
            return
        try:
            lbl.configure(text_color=self._RED)

            def _restore():
                if self._score_label and self._score_label.winfo_exists():
                    self._score_label.configure(
                        text_color=(
                            self._GREEN
                            if self.score > self._INITIAL_SCORE // 2
                            else self._RED
                        )
                    )

            self.root.after(300, _restore)
        except Exception:
            pass

    def _flash_level(self):
        lbl = self._level_label
        if not lbl:
            return
        try:
            lbl.configure(text_color=self._ACCENT2)

            def _restore():
                if self._level_label and self._level_label.winfo_exists():
                    self._level_label.configure(text_color=self._ACCENT)

            self.root.after(500, _restore)
        except Exception:
            pass

    # ── Pause ──────────────────────────────────────────────────────────────────

    def _toggle_pause(self):
        self._paused = not self._paused
        if self._paused:
            self._pause_btn.configure(text=self._t("resume"))
            self._show_pause_popup()
        else:
            self._hide_pause_popup()
            self._pause_btn.configure(text=self._t("pause"))
            self._last_tick = time.time()

    def _show_pause_popup(self):
        if not self.main_frame or not self.main_frame.winfo_exists():
            return
        self._pause_overlay_shown = True

        self._pause_dim = tk.Frame(self.main_frame, bg="#0a0d18")
        self._pause_dim.place(relwidth=1, relheight=1)
        self._pause_dim.lower()

        self._pause_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self._BG_MID,
            corner_radius=16,
            border_width=2,
            border_color=self._ACCENT,
        )
        self._pause_frame.place(relx=0.5, rely=0.5, anchor="center")

        inner = ctk.CTkFrame(self._pause_frame, fg_color="transparent")
        inner.pack(padx=40, pady=32)

        ctk.CTkLabel(
            inner,
            text=self._t("paused"),
            font=("Segoe UI", 32, "bold"),
            text_color=self._TEXT_MAIN,
        ).pack(pady=(0, 4))
        ctk.CTkLabel(
            inner,
            text="⏸  Game is paused",
            font=("Segoe UI", 13),
            text_color=self._TEXT_DIM,
        ).pack(pady=(0, 20))
        ctk.CTkFrame(
            inner, fg_color=self._BG_CARD, height=2, corner_radius=1, width=260
        ).pack(pady=(0, 20))

        _b = dict(
            width=260,
            height=48,
            corner_radius=12,
            font=("Segoe UI", 15, "bold"),
            text_color="#ffffff",
        )
        self._btn(
            inner,
            text="▶  " + self._t("resume"),
            command=self._toggle_pause,
            fg_color=self._ACCENT,
            hover_color="#5a6bff",
            sound="btn",
            **_b,
        ).pack(pady=(0, 10))

        _b2 = {k: v for k, v in _b.items() if k != "text_color"}
        self._btn(
            inner,
            text=self._t("main_menu"),
            command=lambda: (self._hide_pause_popup(), self._show_game_menu()),
            fg_color=self._BG_CARD,
            hover_color="#2e3354",
            text_color=self._TEXT_MAIN,
            sound="back",
            **_b2,
        ).pack(pady=(0, 4))

    def _hide_pause_popup(self):
        for attr in ("_pause_dim", "_pause_frame"):
            w = getattr(self, attr, None)
            if w and w.winfo_exists():
                w.destroy()
            setattr(self, attr, None)
        self._pause_overlay_shown = False

    # ── Game Over ──────────────────────────────────────────────────────────────

    def _game_over(self):
        if not self._running:
            return
        self._running = False
        self._boss = None
        self._snd("gameover")
        final_score, final_level = self.score, self.level
        self._clear()

        bg_canvas = tk.Canvas(self.main_frame, bg=self._BG_DARK, highlightthickness=0)
        bg_canvas.place(relwidth=1, relheight=1)
        bg_canvas.update_idletasks()
        self._draw_stars(bg_canvas)
        bg_canvas.bind("<Configure>", lambda e, c=bg_canvas: self._draw_stars(c))

        outer = ctk.CTkFrame(self.main_frame, fg_color="transparent", corner_radius=0)
        outer.place(relwidth=1, relheight=1)
        outer.grid_rowconfigure(0, weight=1)
        outer.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(
            outer,
            fg_color=self._BG_MID,
            corner_radius=24,
            border_width=1,
            border_color=self._BG_CARD,
            bg_color="transparent",
        )
        card.grid(row=0, column=0, padx=80, pady=60, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card, text=self._t("game_over"), font=self._F_BIG, text_color=self._RED
        ).grid(row=0, column=0, pady=(36, 8))
        ctk.CTkLabel(
            card,
            text=f"{self._t('final_score')}: {final_score}   |   {self._t('level')}: {final_level}",
            font=("Segoe UI", 20),
            text_color=self._TEXT_DIM,
        ).grid(row=1, column=0, pady=(0, 40))

        _b = dict(
            width=220, height=52, corner_radius=14, font=self._F_BTN, text_color="#fff"
        )
        self._btn(
            card,
            text=self._t("play_again"),
            command=self._start_game,
            fg_color=self._ACCENT,
            hover_color="#5a6bff",
            sound="btn",
            **_b,
        ).grid(row=2, column=0, pady=8)
        self._btn(
            card,
            text=self._t("main_menu"),
            command=self._show_game_menu,
            fg_color=self._BG_CARD,
            hover_color="#2e3354",
            sound="btn",
            **_b,
        ).grid(row=3, column=0, pady=8)
        self._btn(
            card,
            text=self._t("back_to_app"),
            command=self._exit_to_app,
            fg_color="#2d1f2f",
            hover_color="#3d2040",
            sound="back",
            **_b,
        ).grid(row=4, column=0, pady=(8, 36))


class AmharicTypingRaceMenu(Menu):
    """
    A self-contained typing race widget.

    Parameters
    ----------
    root : tk/ctk root or frame
        Parent widget. Passed again in open_menu, but stored here too.
    appearance_mode : str
        "dark" or "light" (default "dark").
    color_theme : str
        customtkinter color theme (default "blue").
    """

    # ── Nested NPC ────────────────────────────────────────────────────────────
    class _NPC:
        def __init__(self, profile, total_words, lane):
            self.name = profile["name"]
            self.color = profile["color"]
            self.wpm_min, self.wpm_max = profile["wpm_range"]
            self.hesitation = profile["hesitation"]
            self.total_words = total_words
            self.lane = lane
            self.progress = 0.0
            self.words_done = 0
            self.finished = False
            self.finish_time = None
            self._next_word_time = float("inf")

        def unfreeze(self):
            self._schedule_next(offset=random.uniform(0.1, 0.4))

        def _schedule_next(self, offset=0):
            wpm = random.uniform(self.wpm_min, self.wpm_max)
            delay = (60.0 / wpm) + offset
            if random.random() < self.hesitation:
                delay += random.uniform(0.1, 0.5)
            self._next_word_time = time.time() + delay

        def update(self, now):
            if self.finished or now < self._next_word_time:
                return
            self.words_done = min(self.words_done + 1, self.total_words)
            self.progress = self.words_done / self.total_words
            if self.words_done >= self.total_words:
                self.finished = True
                self.finish_time = now
            else:
                self._schedule_next()

    # ── Class-level constants ─────────────────────────────────────────────────
    RACE_WORD_COUNT = 30
    PLAYER_COLOR = "#4fc3f7"
    ROAD_COLOR = "#1c1c30"
    STRIPE_COLOR = "#2e2e50"
    GRASS_COLOR = "#0d1f0d"
    TRACK_BG = "#0d0d1a"
    CAR_W = 52
    CAR_H = 28
    TRACK_H = 80
    START_X = 90
    FINISH_PAD = 70

    LIGHT_COLORS_ON = ["#f44336", "#ff9800", "#4caf50"]
    LIGHT_COLORS_OFF = ["#2a0a0a", "#2a1800", "#0a1a0a"]

    DEFAULT_WORD_BANKS = {
        "amharic": [
            "ፈጣን",
            "ቡናማ",
            "ቀበሮ",
            "ሰነፍ",
            "ውሻ",
            "ዘሎ",
            "ያልፋል",
            "ቀዝቃዛ",
            "ጠዋት",
            "ወንዝ",
            "ዳር",
            "ሲሮጥ",
            "ፍጥነት",
            "ልምምድ",
            "ትክክለኝነት",
            "ትኩረት",
            "ትዕግስት",
            "ቁልፍ",
            "ምት",
            "መጨረሻ",
            "መስመር",
            "ቀጥል",
            "ጣቶች",
            "አዕምሮ",
            "ጡንቻ",
            "ትውስታ",
            "ቁልፍ",
            "ሰሌዳ",
            "ደረጃ",
            "ፉክክር",
            "ድል",
            "ሽንፈት",
            "ጥረት",
            "ተደጋጋሚ",
            "ልምምድ",
            "ፍጥነት",
            "ሩጫ",
            "መኪና",
            "መንገድ",
            "ፈጣን",
            "ይሁን",
            "ቀጥ",
            "ጠንካራ",
            "ቀላል",
            "ከባድ",
            "ስኬት",
            "ዝግጁ",
            "ግፋ",
            "ፍጥነት",
            "ፊደል",
        ],
    }

    # ── Per-difficulty WPM / hesitation bands (NPCs are randomised within these) ──
    DIFFICULTY_BANDS = {
        #           overall wpm window   hesitation window   spread ±
        "Easy": {
            "wpm_lo": 18,
            "wpm_hi": 46,
            "hes_lo": 0.12,
            "hes_hi": 0.32,
            "spread": 6,
        },
        "Medium": {
            "wpm_lo": 36,
            "wpm_hi": 80,
            "hes_lo": 0.04,
            "hes_hi": 0.16,
            "spread": 8,
        },
        "Hard": {
            "wpm_lo": 58,
            "wpm_hi": 108,
            "hes_lo": 0.00,
            "hes_hi": 0.07,
            "spread": 10,
        },
    }

    # ── Name pools — one per language ────────────────────────────────────────
    NPC_NAMES_ENGLISH = [
        "Turbo",
        "Blaze",
        "Nova",
        "Viper",
        "Storm",
        "Rocket",
        "Comet",
        "Drift",
        "Phantom",
        "Ace",
        "Bolt",
        "Dash",
        "Raze",
        "Spike",
        "Flash",
    ]
    NPC_NAMES_AMHARIC = [
        "ፍጥነት",  # Speed
        "ነጎድጓድ",  # Thunder
        "ብልጭታ",  # Flash / Spark
        "ኮከብ",  # Star
        "ነፋስ",  # Wind
        "እሳት",  # Fire
        "አውሎ",  # Whirlwind
        "ቀስት",  # Arrow
        "ወርቅ",  # Gold
        "ሰማይ",  # Sky
        "ጀግና",  # Hero
        "ዶፍ",  # Downpour
        "ብርሃን",  # Light
        "ዘላቂ",  # Enduring
        "ድንቅ",  # Wonder / Amazing
    ]

    # ── Car colour palette (sampled without replacement per race) ─────────────
    NPC_COLOR_POOL = [
        "#ef5350",
        "#ff9800",
        "#ab47bc",
        "#26c6da",
        "#66bb6a",
        "#ffa726",
        "#ec407a",
        "#7e57c2",
        "#26a69a",
        "#d4e157",
        "#ff7043",
        "#42a5f5",
        "#8d6e63",
        "#78909c",
        "#ffca28",
    ]

    UI_STRINGS = {
        "english": {
            "title": "Amharic TYPING RACE",
            "configure": "Configure your race and hit Start",
            "get_ready": "Get ready …",
            "in_progress": "🏎  Race in progress …",
            "language": "Language",
            "difficulty": "Difficulty",
            "start_btn": "Start Race",
            "race_again": "Race Again",
            "wpm": "WPM",
            "acc": "ACC",
            "waiting": "Waiting for race to start …",
            "type_here": "Type here!",
            "get_ready_lbl": "GET READY",
            "go": "GO!",
            "finish": "FINISH",
            "you": "YOU",
            "difficulties": {"Easy": "Easy", "Medium": "Medium", "Hard": "Hard"},
            "win_titles": {
                1: "🥇  YOU WIN!",
                2: "🥈  2nd Place!",
                3: "🥉  3rd Place",
                4: "💨  Last Place…",
            },
            "win_msgs": {
                1: "You beat everyone — incredible driving!",
                2: "So close to the top! Push harder next time.",
                3: "Solid race — can you get to the podium?",
                4: "The NPCs smoked you. Keep practising!",
            },
            "your_speed": "Your speed",
            "words_typed": "Words typed",
            "you_marker": " ← YOU",
        },
        "amharic": {
            "title": "የአማረኛ ጽሁፍ ውድድር",
            "configure": "ሩጫዎን ያዋቅሩ እና ጀምር የሚለውን ይጫኑ",
            "get_ready": "ተዘጋጁ …",
            "in_progress": "ሩጫው በሂደት ላይ ነው …",
            "language": "ቋንቋ",
            "difficulty": "ክብደት",
            "start_btn": "ሩጫ ጀምር",
            "race_again": "እንደገና ሩጫ",
            "wpm": "ቃላት/ደቂቃ",
            "acc": "ትክክለኛነት",
            "waiting": "ሩጫ ለመጀመር በመጠባበቅ ላይ …",
            "type_here": "እዚህ ይጻፉ!",
            "get_ready_lbl": "ተዘጋጁ",
            "go": "ሂዱ! 🏁",
            "finish": "መጨረሻ",
            "you": "እርስዎ",
            "difficulties": {"Easy": "ቀላል", "Medium": "መካከለኛ", "Hard": "ከባድ"},
            "win_titles": {
                1: "🥇  አሸነፉ!",
                2: "🥈  2ኛ ቦታ!",
                3: "🥉  3ኛ ቦታ",
                4: "💨  የመጨረሻ ቦታ…",
            },
            "win_msgs": {
                1: "ሁሉንም አሸነፉ — አስደናቂ ሩጫ!",
                2: "ከፍተኛ ቦታ በጣም ቅርብ ነበሩ! ቀጥሎ ይሞክሩ።",
                3: "ጥሩ ሩጫ — ወደ ፖዲየም መውጣት ይቻላል?",
                4: "NPC'ዎቹ ለብልቦትዋል። ልምምድ ያድርጉ!",
            },
            "your_speed": "የእርስዎ ፍጥነት",
            "words_typed": "የተጻፉ ቃላቶች",
            "you_marker": " ← እርስዎ",
        },
    }

    # ── Init ──────────────────────────────────────────────────────────────────
    def __init__(self, root=None, appearance_mode="dark", color_theme="blue"):
        ctk.set_appearance_mode(appearance_mode)
        ctk.set_default_color_theme(color_theme)

        self._root = root
        self._widgets = []
        self._container = None

        self.on_back_button_pressed = signal(f"on_back_button_pressed{self}")

        # Race state
        self._race_active = False
        self._race_started = False
        self._start_time = None
        self._player_prog = 0.0
        self._player_done = False
        self._player_finish_time = None
        self._npcs = []
        self._anim_job = None
        self._finish_order = []

        # Word bank & paragraph
        self._word_banks = dict(self.DEFAULT_WORD_BANKS)
        self._words = []
        self._word_results = []
        self._current_idx = 0
        self._words_correct = 0
        self._race_words_target = self.RACE_WORD_COUNT

        # Options vars (created when open_menu is called)
        self._language = None
        self._difficulty = None

    # ── Public API ────────────────────────────────────────────────────────────
    def open_menu(self, root):
        self._root = root
        self._language = ctk.StringVar(value="english")
        self._difficulty = ctk.StringVar(value="Medium")

        self._build_ui(root)
        self._setup_race()

    def close_menu(self):
        self._stop_race()
        if self._container:
            self._container.pack_forget()

    # ── Build UI ──────────────────────────────────────────────────────────────
    def _build_ui(self, parent):
        self._container = ctk.CTkFrame(parent, fg_color=self.TRACK_BG, corner_radius=0)
        self._container.pack(fill="both", expand=True)

        s = self._get_strings()

        # ── Header ──
        hdr = ctk.CTkFrame(
            self._container, height=52, corner_radius=0, fg_color="#080812"
        )
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        self._back_btn = ctk.CTkButton(
            hdr,
            text="◀ Back",
            width=80,
            height=32,
            corner_radius=6,
            font=ctk.CTkFont("Courier New", 11, weight="bold"),
            fg_color="transparent",
            hover_color="#1a1a30",
            text_color="#6666aa",
            border_width=1,
            border_color="#2a2a4a",
            command=self._on_back_click,
        )
        self._back_btn.pack(side="left", padx=(12, 4), pady=10)

        self._title_lbl = ctk.CTkLabel(
            hdr,
            text=s["title"],
            font=ctk.CTkFont("Courier New", 20, weight="bold"),
            text_color=self.PLAYER_COLOR,
        )
        self._title_lbl.pack(side="left", padx=8, pady=10)
        self._status_lbl = ctk.CTkLabel(
            hdr,
            text=s["configure"],
            font=ctk.CTkFont("Courier New", 12),
            text_color="#777",
        )
        self._status_lbl.pack(side="right", padx=20)

        # ── Options bar ──
        opts = ctk.CTkFrame(self._container, fg_color="#0d0d1f", height=50)
        opts.pack(fill="x")
        opts.pack_propagate(False)

        LANG_LABELS = ["English", "አማርኛ"]
        self._lang_lbl = ctk.CTkLabel(
            opts, text=s["language"], font=ctk.CTkFont(size=12), text_color="#888"
        )
        self._lang_lbl.pack(side="left", padx=(16, 4))
        self._lang_menu = ctk.CTkOptionMenu(
            opts,
            values=LANG_LABELS,
            variable=ctk.StringVar(value=LANG_LABELS[0]),
            width=110,
            height=30,
            font=ctk.CTkFont(size=12),
            fg_color="#1a1a2e",
            button_color="#2a2a4e",
            button_hover_color="#3a3a6e",
            command=self._on_lang_change,
        )
        self._lang_menu.pack(side="left", padx=(0, 4))

        ctk.CTkFrame(opts, width=1, fg_color="#333").pack(
            side="left", fill="y", padx=8, pady=10
        )

        self._diff_lbl = ctk.CTkLabel(
            opts, text=s["difficulty"], font=ctk.CTkFont(size=12), text_color="#888"
        )
        self._diff_lbl.pack(side="left", padx=(4, 4))
        diff_vals = ["Easy", "Medium", "Hard"]
        diff_display = [s["difficulties"][k] for k in diff_vals]
        self._diff_menu = ctk.CTkOptionMenu(
            opts,
            values=diff_display,
            variable=ctk.StringVar(value=diff_display[1]),
            width=110,
            height=30,
            font=ctk.CTkFont(size=12),
            fg_color="#1a1a2e",
            button_color="#2a2a4e",
            button_hover_color="#3a3a6e",
            command=self._on_diff_change,
        )
        self._diff_menu.pack(side="left", padx=(0, 4))

        # ── Track canvas ──
        canvas_h = self.TRACK_H * 4 + 30
        cf = ctk.CTkFrame(self._container, fg_color=self.TRACK_BG, corner_radius=0)
        cf.pack(fill="x", padx=16, pady=(8, 0))
        self._canvas = tk.Canvas(
            cf, height=canvas_h, bg=self.TRACK_BG, highlightthickness=0
        )
        self._canvas.pack(fill="x", expand=True)
        self._canvas.bind("<Configure>", lambda e: self._redraw())

        # ── Prompt display ──
        pf = ctk.CTkFrame(self._container, corner_radius=10, fg_color="#10101e")
        pf.pack(fill="x", padx=16, pady=(8, 0))
        self._prompt_box = ctk.CTkTextbox(
            pf,
            height=90,
            wrap="word",
            font=ctk.CTkFont("Courier New", 14),
            fg_color="transparent",
            state="disabled",
            text_color="#ccc",
        )
        self._prompt_box.pack(fill="x", padx=12, pady=8)

        # ── Input entry ──
        self._input_var = ctk.StringVar()
        self._input_var.trace_add("write", self._on_input_change)
        self._entry = ctk.CTkEntry(
            self._container,
            textvariable=self._input_var,
            height=48,
            corner_radius=10,
            font=ctk.CTkFont("Courier New", 15),
            placeholder_text=s["waiting"],
            border_width=2,
            border_color="#333",
            state="disabled",
        )
        self._entry.pack(fill="x", padx=16, pady=(8, 0))
        self._entry.bind("<KeyRelease>", self._on_key_release)

        # ── Bottom bar ──
        bot = ctk.CTkFrame(self._container, fg_color="#080812", height=64)
        bot.pack(fill="x", padx=0, pady=(8, 0))
        bot.pack_propagate(False)

        stats = ctk.CTkFrame(bot, fg_color="transparent")
        stats.pack(side="left", padx=16, pady=8)
        self._wpm_lbl = ctk.CTkLabel(
            stats,
            text=f"{s['wpm']}: —",
            font=ctk.CTkFont("Courier New", 13),
            text_color=self.PLAYER_COLOR,
        )
        self._wpm_lbl.pack(side="left")
        self._acc_lbl = ctk.CTkLabel(
            stats,
            text=f"{s['acc']}: —",
            font=ctk.CTkFont("Courier New", 13),
            text_color="#66bb6a",
        )
        self._acc_lbl.pack(side="left", padx=16)

        self._cd_canvas = tk.Canvas(
            bot, width=120, height=48, bg="#080812", highlightthickness=0
        )
        self._cd_canvas.pack(side="left", expand=True)
        self._cd_items = []
        self._cd_step = 0
        self._cd_job = None
        self._cd_active = False
        self._build_countdown_lights()

        self._start_btn = ctk.CTkButton(
            bot,
            text=s["start_btn"],
            width=130,
            height=38,
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1b5e20",
            hover_color="#2e7d32",
            command=self._open_countdown,
        )
        self._start_btn.pack(side="right", padx=16, pady=13)

        # ── Result overlay ──
        self._overlay = ctk.CTkFrame(
            self._container,
            corner_radius=14,
            fg_color="#0e0e20",
            border_width=2,
            border_color=self.PLAYER_COLOR,
        )
        self._ov_title = ctk.CTkLabel(
            self._overlay,
            text="",
            font=ctk.CTkFont("Courier New", 26, weight="bold"),
            text_color=self.PLAYER_COLOR,
        )
        self._ov_title.pack(pady=(22, 4))
        self._ov_body = ctk.CTkLabel(
            self._overlay,
            text="",
            font=ctk.CTkFont("Courier New", 13),
            text_color="#aaa",
            justify="center",
        )
        self._ov_body.pack(pady=(0, 8))
        self._race_again_btn = ctk.CTkButton(
            self._overlay,
            text=s["race_again"],
            width=130,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._setup_race,
        )
        self._race_again_btn.pack(pady=(4, 22))

        self._container.bind(
            "<Configure>", lambda e: self._container.after_idle(self._redraw)
        )

    # ── Strings helper ────────────────────────────────────────────────────────
    def _get_strings(self):
        lang = self._language.get() if self._language else "english"
        return self.UI_STRINGS[lang]

    # ── Language/option callbacks ─────────────────────────────────────────────
    def _on_lang_change(self, display_val):
        if display_val == "English":
            self._language.set("english")
        else:
            self._language.set("amharic")
        self._refresh_ui_strings()
        if not self._race_active:
            self._setup_race()

    def _on_diff_change(self, display_val):
        s = self._get_strings()
        for k, v in s["difficulties"].items():
            if v == display_val:
                self._difficulty.set(k)
                break
        if not self._race_active:
            self._setup_race()

    def _on_option_change(self):
        if not self._race_active:
            self._setup_race()

    def _refresh_ui_strings(self):
        if not self._container:
            return
        s = self._get_strings()
        self._title_lbl.configure(text=s["title"])
        self._status_lbl.configure(text=s["configure"])
        self._lang_lbl.configure(text=s["language"])
        self._diff_lbl.configure(text=s["difficulty"])
        self._start_btn.configure(text=s["start_btn"])
        self._race_again_btn.configure(text=s["race_again"])
        self._wpm_lbl.configure(text=f"{s['wpm']}: —")
        self._acc_lbl.configure(text=f"{s['acc']}: —")
        diff_vals = ["Easy", "Medium", "Hard"]
        diff_display = [s["difficulties"][k] for k in diff_vals]
        cur_key = self._difficulty.get()
        self._diff_menu.configure(values=diff_display)
        self._diff_menu.set(s["difficulties"].get(cur_key, diff_display[1]))

    # ── Public word bank loader ───────────────────────────────────────────────
    def load_word_bank(self, json_path: str):
        """
        Load a custom word bank from a JSON file path.
        Expected format:  {"easy": [...], "medium": [...], "hard": [...]}
        Keys are case-insensitive. Unused keys are ignored.
        Call before open_menu, or between races.
        """
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError(
                'JSON must be an object: {"easy": [], "medium": [], "hard": []}'
            )
        mapping = {k.lower(): v for k, v in data.items()}
        for level_key, diff_key in [
            ("easy", "Easy"),
            ("medium", "Medium"),
            ("hard", "Hard"),
        ]:
            if level_key in mapping:
                words = [str(w).strip() for w in mapping[level_key] if str(w).strip()]
                if len(words) < 5:
                    raise ValueError(f"'{level_key}' needs at least 5 words")
                self._word_banks[f"_diff_{diff_key}"] = words
        if self._container and not self._race_active:
            self._setup_race()

    # ── Generate words batch ──────────────────────────────────────────────────
    def _generate_words(self, count=None):
        if count is None:
            count = self.RACE_WORD_COUNT
        diff = self._difficulty.get()
        diff_bank_key = f"_diff_{diff}"
        if diff_bank_key in self._word_banks:
            bank = self._word_banks[diff_bank_key]
        else:
            bank = self._word_banks.get("amharic", list(self._word_banks.values())[0])
        return random.choices(bank, k=count)

    # ── NPC profile builder ───────────────────────────────────────────────────
    def _make_npc_profiles(self, count=3):
        """
        Build *count* fully randomised NPC profiles for the current difficulty.

        Each NPC gets:
        • a unique name drawn randomly from NPC_NAME_POOL
        • a unique car colour drawn randomly from NPC_COLOR_POOL
        • a wpm_range centred on a random base within DIFFICULTY_BANDS,
          spread by ±spread so no two NPCs ever feel identical
        • a hesitation value sampled uniformly within the difficulty band
        """
        band = self.DIFFICULTY_BANDS[self._difficulty.get()]
        spread = band["spread"]

        lang = self._language.get() if self._language else "english"
        name_pool = (
            self.NPC_NAMES_AMHARIC if lang == "amharic" else self.NPC_NAMES_ENGLISH
        )
        names = random.sample(name_pool, min(count, len(name_pool)))
        colors = random.sample(
            self.NPC_COLOR_POOL, min(count, len(self.NPC_COLOR_POOL))
        )

        profiles = []
        for i in range(count):
            base = random.uniform(band["wpm_lo"], band["wpm_hi"])
            wpm_min = max(5, round(base - spread))
            wpm_max = round(base + spread)
            hesitation = round(random.uniform(band["hes_lo"], band["hes_hi"]), 3)

            profiles.append(
                {
                    "name": names[i],
                    "color": colors[i],
                    "wpm_range": (wpm_min, wpm_max),
                    "hesitation": hesitation,
                }
            )

        return profiles

    # ── Race setup ────────────────────────────────────────────────────────────
    def _setup_race(self):
        self._hide_overlay()
        self._stop_race()

        s = self._get_strings()

        self._race_words_target = self.RACE_WORD_COUNT
        self._words = self._generate_words()
        self._word_results = []
        self._current_idx = 0
        self._words_correct = 0

        self._race_active = False
        self._race_started = False
        self._start_time = None
        self._player_prog = 0.0
        self._player_done = False
        self._player_finish_time = None
        self._finish_order = []

        profiles = self._make_npc_profiles(count=3)
        self._npcs = [
            self._NPC(p, self._race_words_target, lane=i + 1)
            for i, p in enumerate(profiles)
        ]

        self._input_var.set("")
        self._entry.configure(
            state="disabled",
            placeholder_text=s["waiting"],
            border_color="#333",
        )
        self._wpm_lbl.configure(text=f"{s['wpm']}: —")
        self._acc_lbl.configure(text=f"{s['acc']}: —")
        self._status_lbl.configure(text=s["configure"])
        self._start_btn.configure(state="normal", text=s["start_btn"])
        self._lang_menu.configure(state="normal")
        self._diff_menu.configure(state="normal")
        if hasattr(self, "_cd_items") and self._cd_items:
            for i in range(3):
                self._set_cd_light(i, False)
            self._cd_canvas.itemconfig(self._cd_go_text, text="")

        self._container.after(50, self._redraw)
        self._render_prompt()

    def _stop_race(self):
        self._race_active = False
        self._cd_active = False
        if self._cd_job:
            try:
                self._container.after_cancel(self._cd_job)
            except Exception:
                pass
            self._cd_job = None
        if self._anim_job:
            self._container.after_cancel(self._anim_job)
            self._anim_job = None

    def _on_back_click(self):
        if self.on_back_button_pressed:
            self.on_back_button_pressed.send(self)

    # ── Countdown lights ──────────────────────────────────────────────────────
    def _build_countdown_lights(self):
        c = self._cd_canvas
        c.delete("all")
        self._cd_items = []
        r = 16
        xs = [22, 60, 98]
        cy = 24
        for i, cx in enumerate(xs):
            c.create_oval(
                cx - r - 2,
                cy - r - 2,
                cx + r + 2,
                cy + r + 2,
                fill="#080818",
                outline="#1a1a35",
                width=1,
            )
            light = c.create_oval(
                cx - r,
                cy - r,
                cx + r,
                cy + r,
                fill=self.LIGHT_COLORS_OFF[i],
                outline="",
            )
            c.create_oval(
                cx - r + 4,
                cy - r + 4,
                cx - r + 10,
                cy - r + 10,
                fill="#ffffff",
                outline="white",
            )
            self._cd_items.append(light)
        self._cd_go_text = c.create_text(
            60, 24, text="", fill="#4caf50", font=("Courier New", 18, "bold")
        )

    def _set_cd_light(self, idx, on: bool):
        color = self.LIGHT_COLORS_ON[idx] if on else self.LIGHT_COLORS_OFF[idx]
        self._cd_canvas.itemconfig(self._cd_items[idx], fill=color)

    def _open_countdown(self):
        if self._cd_active:
            return
        s = self._get_strings()
        self._start_btn.configure(state="disabled")
        self._lang_menu.configure(state="disabled")
        self._diff_menu.configure(state="disabled")
        self._status_lbl.configure(text=s["get_ready"])
        self._cd_active = True
        self._cd_step = 0
        for i in range(3):
            self._set_cd_light(i, False)
        self._cd_canvas.itemconfig(self._cd_go_text, text="")
        self._cd_tick()

    def _cd_tick(self):
        s = self._get_strings()
        for i in range(3):
            self._set_cd_light(i, False)
        self._cd_canvas.itemconfig(self._cd_go_text, text="")

        step = self._cd_step
        if step < 3:
            self._set_cd_light(step, True)
            self._cd_step += 1
            self._cd_job = self._container.after(900, self._cd_tick)
        else:
            for i in range(3):
                self._set_cd_light(i, True)
            self._cd_canvas.itemconfig(
                self._cd_go_text, text=s["go"].replace(" 🏁", "")
            )
            self._cd_job = self._container.after(700, self._launch_race)

    def _launch_race(self):
        self._cd_active = False
        self._container.after(
            400,
            lambda: (
                self._cd_canvas.itemconfig(self._cd_go_text, text="")
                if self._cd_canvas.winfo_exists()
                else None
            ),
        )
        for i in range(3):
            self._set_cd_light(i, False)

        s = self._get_strings()
        self._race_active = True
        self._race_started = True
        self._start_time = time.time()
        self._status_lbl.configure(text=s["in_progress"])
        self._entry.configure(
            state="normal",
            placeholder_text=s["type_here"],
            border_color=self.PLAYER_COLOR,
        )
        self._entry.focus()
        for npc in self._npcs:
            npc.unfreeze()
        self._animate()

    # ── Input handling — mirrors TypingTestMenu exactly ───────────────────────

    def _on_input_change(self, *_):
        """StringVar trace — mirrors TypingTestMenu._on_input_change."""
        if not self._race_active:
            return
        value = self._input_var.get()
        if value.endswith(" ") or value.endswith("\u00a0"):
            self._commit_word(value.rstrip(" \u00a0"))
            return
        self._render_prompt(value)

    def _on_key_release(self, event):
        """KeyRelease — mirrors TypingTestMenu._on_key_release."""
        if not self._race_active:
            return
        value = self._input_var.get()
        if value.endswith(" ") or value.endswith("\u00a0"):
            self._commit_word(value.rstrip(" \u00a0"))
            return
        self._render_prompt(value)

    def _commit_word(self, typed: str):
        """Single commit path — mirrors TypingTestMenu._commit_word."""
        if not self._race_active:
            return
        typed = typed.strip()
        if not typed:
            self._input_var.set("")
            return

        target = self._words[self._current_idx]
        correct = typed == target
        if correct:
            self._words_correct += 1
        self._word_results.append(correct)

        self._player_prog = min(self._words_correct / self._race_words_target, 1.0)
        self._current_idx += 1
        self._input_var.set("")
        self._entry.after(
            0,
            lambda: (
                self._entry.delete(0, "end") if self._entry.winfo_exists() else None
            ),
        )

        s = self._get_strings()
        elapsed = time.time() - self._start_time
        wpm = int(self._words_correct / (elapsed / 60)) if elapsed > 0 else 0
        acc = round(self._words_correct / max(self._current_idx, 1) * 100, 1)
        self._wpm_lbl.configure(text=f"{s['wpm']}: {wpm}")
        self._acc_lbl.configure(text=f"{s['acc']}: {acc}%")

        if self._current_idx >= len(self._words) - 10:
            self._words += self._generate_words()

        if self._player_prog >= 1.0 and not self._player_done:
            self._player_done = True
            self._player_finish_time = time.time()
            self._finish_order.append(("YOU", self._player_finish_time))
            self._entry.configure(state="disabled")

        self._render_prompt()

    # ── Animation ─────────────────────────────────────────────────────────────
    def _animate(self):
        if not self._race_active:
            return
        now = time.time()
        for npc in self._npcs:
            was = npc.finished
            npc.update(now)
            if npc.finished and not was:
                self._finish_order.append((npc.name, npc.finish_time))

        self._canvas.delete("car")
        self._draw_cars()

        all_npc_done = all(n.finished for n in self._npcs)
        if self._player_done and all_npc_done:
            self._end_race()
            return
        if all_npc_done and not self._player_done:
            last = max(n.finish_time for n in self._npcs)
            if now - last > 25:
                self._player_done = True
                self._finish_order.append(("YOU", now))
                self._entry.configure(state="disabled")
                self._end_race()
                return

        self._anim_job = self._container.after(50, self._animate)

    # ── End race ──────────────────────────────────────────────────────────────
    def _end_race(self):
        self._race_active = False
        if self._anim_job:
            self._container.after_cancel(self._anim_job)

        s = self._get_strings()
        you = s["you"]

        self._finish_order.sort(key=lambda x: x[1])
        positions = {n: i + 1 for i, (n, _) in enumerate(self._finish_order)}
        player_pos = positions.get(you, positions.get("YOU", 4))

        title = s["win_titles"].get(player_pos, s["win_titles"][4])
        msg = s["win_msgs"].get(player_pos, s["win_msgs"][4])

        lines = []
        for i, (name, ft) in enumerate(self._finish_order):
            elapsed = ft - self._start_time
            marker = s["you_marker"] if name in ("YOU", you) else ""
            display = you if name == "YOU" else name
            lines.append(f"  {i+1}.  {display:<10}  {elapsed:.1f}s{marker}")

        elapsed = (self._player_finish_time or time.time()) - self._start_time
        wpm = int((self._words_correct / 1) / (elapsed / 60)) if elapsed > 0 else 0
        body = msg + "\n\n" + "\n".join(lines) + f"\n\n  {s['your_speed']}: {wpm} WPM"

        self._show_overlay(title, body)
        self._start_btn.configure(state="normal", text=s["start_btn"])

    # ── Prompt rendering ──────────────────────────────────────────────────────
    def _render_prompt(self, current_typed=""):
        pb = self._prompt_box
        pb.configure(state="normal")
        pb.delete("1.0", "end")

        pb.tag_config("done_ok", foreground="#4caf50")
        pb.tag_config("done_err", foreground="#f44336")
        pb.tag_config("active_ch_ok", foreground="#ffee58")
        pb.tag_config("active_ch_err", foreground="#f44336", background="#2a0a0a")
        pb.tag_config("active_cur", foreground="#ffffff", background="#4fc3f7")
        pb.tag_config("active_rest", foreground="#ffee58", underline=True)
        pb.tag_config("upcoming", foreground="#555")
        pb.tag_config("space", foreground="#2a2a3a")

        for i, word in enumerate(self._words):
            if i < self._current_idx:
                result = self._word_results[i] if i < len(self._word_results) else True
                tag = "done_ok" if result else "done_err"
                pb.insert("end", word, tag)
                pb.insert("end", " ", "space")
            elif i == self._current_idx:
                for j, ch in enumerate(word):
                    if j < len(current_typed):
                        tag = (
                            "active_ch_ok"
                            if current_typed[j] == ch
                            else "active_ch_err"
                        )
                    elif j == len(current_typed):
                        tag = "active_cur"
                    else:
                        tag = "active_rest"
                    pb.insert("end", ch, tag)
                pb.insert("end", " ", "space")
            else:
                pb.insert("end", word, "upcoming")
                pb.insert("end", " ", "space")

        try:
            pb.see(f"1.{sum(len(w)+1 for w in self._words[:self._current_idx])}")
        except Exception:
            pb.see("end")

        pb.configure(state="disabled")

    # ── Track / car drawing ───────────────────────────────────────────────────
    def _redraw(self):
        self._draw_track()
        self._draw_cars()

    def _canvas_width(self):
        w = self._canvas.winfo_width()
        return w if w > 100 else 860

    def _finish_x(self):
        return self._canvas_width() - self.FINISH_PAD

    def _track_len(self):
        return self._finish_x() - self.START_X

    def _draw_track(self):
        c = self._canvas
        cw = self._canvas_width()
        ch = self.TRACK_H * 4 + 30
        c.delete("track")
        for lane in range(4):
            y0 = lane * self.TRACK_H + 15
            y1 = y0 + self.TRACK_H
            if lane == 0:
                c.create_rectangle(
                    0, 0, cw, y0 + 6, fill=self.GRASS_COLOR, outline="", tags="track"
                )
            if lane == 3:
                c.create_rectangle(
                    0, y1 - 6, cw, ch, fill=self.GRASS_COLOR, outline="", tags="track"
                )
            c.create_rectangle(
                0, y0 + 6, cw, y1 - 6, fill=self.ROAD_COLOR, outline="", tags="track"
            )
            if lane < 3:
                for x in range(0, cw, 28):
                    c.create_rectangle(
                        x,
                        y1 - 8,
                        x + 14,
                        y1 - 6,
                        fill=self.STRIPE_COLOR,
                        outline="",
                        tags="track",
                    )
        fx = self._finish_x()
        sq = 10
        for row in range(ch // sq + 1):
            for col in range(2):
                color = "#fff" if (row + col) % 2 == 0 else "#000"
                c.create_rectangle(
                    fx + col * sq,
                    row * sq,
                    fx + col * sq + sq,
                    row * sq + sq,
                    fill=color,
                    outline="",
                    tags="track",
                )
        s = self._get_strings()
        c.create_text(
            fx + sq,
            ch // 2,
            text=s["finish"],
            fill="#ccc",
            font=("Courier New", 8, "bold"),
            angle=90,
            tags="track",
        )
        c.create_line(
            self.START_X,
            0,
            self.START_X,
            ch,
            fill="#333",
            width=2,
            dash=(6, 4),
            tags="track",
        )

    def _draw_cars(self):
        c = self._canvas
        s = self._get_strings()
        you = s["you"]

        def car_x(prog):
            return int(self.START_X + prog * self._track_len())

        def lane_cy(lane):
            return lane * self.TRACK_H + 15 + self.TRACK_H // 2

        all_racers = [(you, self._player_prog)] + [
            (n.name, n.progress) for n in self._npcs
        ]
        leader_name = max(all_racers, key=lambda x: x[1])[0]

        self._draw_car(
            c,
            car_x(self._player_prog),
            lane_cy(0),
            self.PLAYER_COLOR,
            you,
            leader=(leader_name == you),
        )
        for npc in self._npcs:
            self._draw_car(
                c,
                car_x(npc.progress),
                lane_cy(npc.lane),
                npc.color,
                npc.name,
                leader=(leader_name == npc.name),
            )

    def _draw_car(self, c, x, y, color, name, leader=False):
        hw, hh = self.CAR_W // 2, self.CAR_H // 2
        c.create_oval(
            x - hw + 4,
            y + hh - 2,
            x + hw - 4,
            y + hh + 5,
            fill="#000",
            outline="",
            tags="car",
        )
        c.create_rectangle(
            x - hw,
            y - hh + 6,
            x + hw,
            y + hh,
            fill=color,
            outline="",
            tags="car",
        )
        c.create_rectangle(
            x - hw + 10,
            y - hh,
            x + hw - 8,
            y - hh + 8,
            fill=color,
            outline="",
            tags="car",
        )
        c.create_rectangle(
            x - hw + 11,
            y - hh + 1,
            x + hw - 9,
            y - hh + 7,
            fill="#1a2a3a",
            outline="",
            tags="car",
        )
        c.create_rectangle(
            x - hw,
            y - hh + 8,
            x - hw + 4,
            y - hh + 14,
            fill="#ff1744",
            outline="",
            tags="car",
        )
        c.create_rectangle(
            x + hw - 4,
            y - hh + 8,
            x + hw,
            y - hh + 14,
            fill="#fffde7",
            outline="",
            tags="car",
        )
        for wx in [x - hw + 9, x + hw - 9]:
            c.create_oval(
                wx - 7,
                y + hh - 9,
                wx + 7,
                y + hh + 5,
                fill="#222",
                outline="#444",
                width=2,
                tags="car",
            )
            c.create_oval(
                wx - 3,
                y + hh - 5,
                wx + 3,
                y + hh + 1,
                fill="#555",
                outline="",
                tags="car",
            )
        c.create_text(
            x - hw - 6,
            y,
            text=name,
            fill=color,
            font=("Courier New", 9, "bold"),
            anchor="e",
            tags="car",
        )
        if leader:
            cx, cy = x, y - hh - 4
            pts = [
                cx - 10,
                cy,
                cx - 6,
                cy - 8,
                cx,
                cy - 4,
                cx + 6,
                cy - 8,
                cx + 10,
                cy,
                cx + 10,
                cy + 2,
                cx - 10,
                cy + 2,
            ]
            c.create_polygon(
                pts, fill="#ffd700", outline="#ff8f00", width=1, tags="car"
            )
            for jx, jy in [(cx - 6, cy - 8), (cx, cy - 5), (cx + 6, cy - 8)]:
                c.create_oval(
                    jx - 2,
                    jy - 2,
                    jx + 2,
                    jy + 2,
                    fill="#ff1744",
                    outline="",
                    tags="car",
                )

    # ── Overlay ───────────────────────────────────────────────────────────────
    def _show_overlay(self, title, body):
        self._ov_title.configure(text=title)
        self._ov_body.configure(text=body)
        self._overlay.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.60)

    def _hide_overlay(self):
        if self._overlay:
            self._overlay.place_forget()


class AmharicDodgeMenu(Menu):
    """Lane-dodge typing game — patched version."""

    # ── Nested car object ────────────────────────────────────────────────────
    class _Car:
        __slots__ = ("lane", "x", "color", "resolved")

        def __init__(self, lane: int, x: float, color: str):
            self.lane = lane
            self.x = x
            self.color = color
            self.resolved = False

    # ── Visual / layout constants ─────────────────────────────────────────────
    LANES = 6  # ← was 4
    TRACK_H = 68  # ← was 80 (keeps 6 lanes fitting nicely)
    CAR_W = 52
    CAR_H = 28
    PLAYER_X = 108
    WORD_X = 200
    SPAWN_X_PAD = 70

    TRACK_BG = "#0d0d1a"
    ROAD_COLOR = "#1c1c30"
    STRIPE_COLOR = "#2e2e50"
    GRASS_COLOR = "#0d1f0d"
    PLAYER_COLOR = "#4fc3f7"
    HIT_COLOR = "#f44336"

    WORD_DEFAULT_CLR = "#ffd54f"
    WORD_PLAYER_CLR = "#4fc3f7"
    WORD_DANGER_CLR = "#ff5252"
    WORD_HINT_CLR = "#b9f6ca"

    # ── Difficulty bands ──────────────────────────────────────────────────────
    DIFFICULTY_BANDS = {
        "Easy": {
            "speed": 110,
            "spawn_base_ms": 2_800,
            "spawn_min_ms": 950,
            "spawn_ramp_ms": 100,
        },
        "Medium": {
            "speed": 155,
            "spawn_base_ms": 2_300,
            "spawn_min_ms": 620,
            "spawn_ramp_ms": 130,
        },
        "Hard": {
            "speed": 215,
            "spawn_base_ms": 1_600,
            "spawn_min_ms": 380,
            "spawn_ramp_ms": 170,
        },
    }

    LIVES_MAX = 3
    FRAME_MS = 33
    SPEED_RAMP = 14
    RAMP_EVERY = 6
    HIT_BOX_RATIO = 0.78
    HIT_FLASH_FRAMES = 9
    DANGER_LOOKAHEAD = 280

    LIGHT_COLORS_ON = ["#f44336", "#ff9800", "#4caf50"]
    LIGHT_COLORS_OFF = ["#2a0a0a", "#2a1800", "#0a1a0a"]

    NPC_COLOR_POOL = [
        "#ef5350",
        "#ff9800",
        "#ab47bc",
        "#26c6da",
        "#66bb6a",
        "#ffa726",
        "#ec407a",
        "#7e57c2",
        "#26a69a",
        "#d4e157",
        "#ff7043",
        "#42a5f5",
        "#8d6e63",
        "#78909c",
        "#ffca28",
    ]

    # ── Difficulty-tiered Amharic word banks ──────────────────────────────────
    # Easy   = short words (2-3 Ethiopic syllable blocks)
    AMHARIC_WORDS_EASY = [
        "ውሻ",
        "ዳር",
        "ቁልፍ",
        "ምት",
        "ድል",
        "ጥረት",
        "ሩጫ",
        "ነፋስ",
        "ቀስት",
        "ወርቅ",
        "ሰላም",
        "ጉዞ",
        "ድምፅ",
        "ቀለም",
        "ኮከብ",
        "እሳት",
        "ደረጃ",
        "ፊደል",
        "ሕልም",
        "ዶፍ",
        "ቀበሮ",
        "ሰነፍ",
        "ዘሎ",
    ]

    # Medium = 4-5 block words (original mix)
    AMHARIC_WORDS_MEDIUM = [
        "ፈጣን",
        "ቡናማ",
        "ያልፋል",
        "ቀዝቃዛ",
        "ጠዋት",
        "ወንዝ",
        "ፍጥነት",
        "ልምምድ",
        "ትኩረት",
        "ትዕግስት",
        "መስመር",
        "ቀጥል",
        "ጣቶች",
        "አዕምሮ",
        "ጡንቻ",
        "ትውስታ",
        "ሰሌዳ",
        "ፉክክር",
        "ሽንፈት",
        "መኪና",
        "መንገድ",
        "ይሁን",
        "ጠንካራ",
        "ቀላል",
        "ከባድ",
        "ስኬት",
        "ዝግጁ",
        "ግፋ",
        "ነጎድጓድ",
        "ብልጭታ",
        "አውሎ",
        "ሕይወት",
        "ድንቅ",
    ]

    # Hard  = longer / compound words (6+ blocks)
    AMHARIC_WORDS_HARD = [
        "መጨረሻ",
        "ብርሃን",
        "ሲሮጥ",
        "ትኩረት",
        "ፍጥነት",
        "ልምምድ",
        "ትዕግስት",
        "ትውስታ",
        "ነጎድጓድ",
        "ብልጭታ",
        "ስኬት",
        "ፉክክር",
        "ሽንፈት",
        "ዝግጁ",
        "አዕምሮ",
        "ሰሌዳ",
        "ያስወጋቸው",
        "ጨዋታ",
        "ተዘጋጅ",
        "ፍጥነቱ",
        "መስመሩ",
        "ሩጫውን",
        "ቀጥለህ",
        "ጡንቻህ",
        "ሰሌዳህ",
    ]

    # Back-compat: keep the flat list for any code that references it directly
    AMHARIC_WORDS = AMHARIC_WORDS_MEDIUM

    # ── Bilingual UI strings ──────────────────────────────────────────────────
    UI_STRINGS = {
        "english": {
            "title": "AMHARIC DODGE",
            "subtitle": "Type a lane word to switch lanes and dodge!",
            "start_btn": "Start",
            "play_again": "Play Again",
            "lives": "Lives",
            "score": "Dodged",
            "wpm": "WPM",
            "get_ready": "Get Ready…",
            "go": "GO!",
            "type_here": "Type a lane word to dodge!",
            "waiting": "Waiting for game to start…",
            "game_over": "GAME OVER",
            "your_score": "Cars dodged",
            "your_wpm": "Avg WPM",
            "well_done": "Nice driving!",
            "language": "Language",
            "difficulty": "Difficulty",
            "difficulties": {"Easy": "Easy", "Medium": "Medium", "Hard": "Hard"},
        },
        "amharic": {
            "title": "አማርኛ ማስወጋት",
            "subtitle": "ቃሉን ይጻፉ ለሌላ መስመር ለመሄድ!",
            "start_btn": "ጀምር",
            "play_again": "እንደገና",
            "lives": "ህይወት",
            "score": "ያስወጋቸው",
            "wpm": "ቃ/ደ",
            "get_ready": "ተዘጋጅ…",
            "go": "ሂድ!",
            "type_here": "ቃሉን ይጻፉ!",
            "waiting": "ጨዋታ ለመጀመር…",
            "game_over": "ጨዋታ አለቀ",
            "your_score": "ያስወጋቸው መኪናዎች",
            "your_wpm": "አማካኝ ፍጥነት",
            "well_done": "ጥሩ ሩጫ!",
            "language": "ቋንቋ",
            "difficulty": "ክብደት",
            "difficulties": {"Easy": "ቀላል", "Medium": "መካከለኛ", "Hard": "ከባድ"},
        },
    }

    # ── Init ──────────────────────────────────────────────────────────────────
    def __init__(self, root=None, appearance_mode="dark", color_theme="blue"):
        ctk.set_appearance_mode(appearance_mode)
        ctk.set_default_color_theme(color_theme)

        self._root = root
        self._container = None

        self.on_back_button_pressed = signal(f"on_back_button_pressed{self}")

        self._game_active = False
        self._player_lane = self.LANES // 2
        self._lives = self.LIVES_MAX
        self._score = 0
        self._words_typed = 0
        self._start_time = None
        self._cars = []
        self._lane_words = []
        self._current_speed = 0.0
        self._hit_flash = 0
        self._last_frame_time = None

        self._anim_job = None
        self._spawn_job = None

        self._cd_active = False
        self._cd_step = 0
        self._cd_job = None
        self._cd_items = []
        self._cd_go_text = None

        self._language = None
        self._difficulty = None
        self._input_var = None

        # Custom word bank loaded from JSON; None = use built-in banks
        self._custom_word_bank: dict | None = None

    # ── Public API ────────────────────────────────────────────────────────────
    def load_word_bank(self, path: str) -> None:
        """Load a custom word bank from a JSON file.

        The file must contain an object with at least one of the keys
        ``"easy"``, ``"medium"``, or ``"hard"`` (case-insensitive), each
        mapping to a list of strings::

            {
                "easy":   ["ውሻ", "ዳር", ...],
                "medium": ["ፈጣን", "ትኩረት", ...],
                "hard":   ["ያስወጋቸው", "ትዕግስት", ...]
            }

        Any tier that is absent or empty falls back to the built-in bank
        for that difficulty.  Call this before ``open_menu()`` or between
        games; it takes effect on the next ``_setup_game()`` call.

        Raises ``FileNotFoundError`` if *path* does not exist and
        ``ValueError`` if the JSON is structurally invalid.
        """
        with open(path, encoding="utf-8") as fh:
            raw: dict = json.load(fh)

        if not isinstance(raw, dict):
            raise ValueError(
                f"Word bank JSON must be an object, got {type(raw).__name__}"
            )

        # Normalise keys to title-case ("easy" → "Easy") and validate values
        normalised: dict[str, list[str]] = {}
        for key, words in raw.items():
            tier = key.strip().capitalize()  # "easy"/"Easy"/"EASY" → "Easy"
            if tier not in ("Easy", "Medium", "Hard"):
                raise ValueError(
                    f"Unknown difficulty tier '{key}'. Expected easy/medium/hard."
                )
            if not isinstance(words, list) or not all(
                isinstance(w, str) for w in words
            ):
                raise ValueError(f"Tier '{key}' must be a list of strings.")
            if words:  # silently skip empty tiers
                normalised[tier] = words

        if not normalised:
            raise ValueError("Word bank file contained no usable tiers.")

        self._custom_word_bank = normalised

    def open_menu(self, root):
        self._root = root
        self._language = ctk.StringVar(value="english")
        self._difficulty = ctk.StringVar(value="Medium")
        self._build_ui(root)
        self._setup_game()

    def close_menu(self):
        self._stop_game()
        if self._container:
            self._container.pack_forget()

    # ── UI Construction ───────────────────────────────────────────────────────
    def _build_ui(self, parent):
        self._container = ctk.CTkFrame(parent, fg_color=self.TRACK_BG, corner_radius=0)
        self._container.pack(fill="both", expand=True)
        s = self._get_strings()

        # Header
        hdr = ctk.CTkFrame(
            self._container, height=52, corner_radius=0, fg_color="#080812"
        )
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        ctk.CTkButton(
            hdr,
            text="◀ Back",
            width=80,
            height=32,
            corner_radius=6,
            font=ctk.CTkFont("Courier New", 11, weight="bold"),
            fg_color="transparent",
            hover_color="#1a1a30",
            text_color="#6666aa",
            border_width=1,
            border_color="#2a2a4a",
            command=self._on_back_click,
        ).pack(side="left", padx=(12, 4), pady=10)
        self._title_lbl = ctk.CTkLabel(
            hdr,
            text=s["title"],
            font=ctk.CTkFont("Courier New", 20, weight="bold"),
            text_color=self.PLAYER_COLOR,
        )
        self._title_lbl.pack(side="left", padx=8)
        self._status_lbl = ctk.CTkLabel(
            hdr,
            text=s["subtitle"],
            font=ctk.CTkFont("Courier New", 12),
            text_color="#777",
        )
        self._status_lbl.pack(side="right", padx=20)

        # Options bar
        opts = ctk.CTkFrame(self._container, height=44, fg_color="#0d0d1f")
        opts.pack(fill="x")
        opts.pack_propagate(False)
        self._lang_lbl = ctk.CTkLabel(
            opts, text=s["language"], font=ctk.CTkFont(size=12), text_color="#888"
        )
        self._lang_lbl.pack(side="left", padx=(16, 4))
        self._lang_menu = ctk.CTkOptionMenu(
            opts,
            values=["English", "አማርኛ"],
            variable=ctk.StringVar(value="English"),
            width=110,
            height=30,
            font=ctk.CTkFont(size=12),
            fg_color="#1a1a2e",
            button_color="#2a2a4e",
            button_hover_color="#3a3a6e",
            command=self._on_lang_change,
        )
        self._lang_menu.pack(side="left", padx=(0, 8))
        ctk.CTkFrame(opts, width=1, fg_color="#333").pack(
            side="left", fill="y", padx=4, pady=10
        )
        self._diff_lbl = ctk.CTkLabel(
            opts, text=s["difficulty"], font=ctk.CTkFont(size=12), text_color="#888"
        )
        self._diff_lbl.pack(side="left", padx=(8, 4))
        diff_vals = ["Easy", "Medium", "Hard"]
        diff_display = [s["difficulties"][k] for k in diff_vals]
        self._diff_menu = ctk.CTkOptionMenu(
            opts,
            values=diff_display,
            variable=ctk.StringVar(value=diff_display[1]),
            width=120,
            height=30,
            font=ctk.CTkFont(size=12),
            fg_color="#1a1a2e",
            button_color="#2a2a4e",
            button_hover_color="#3a3a6e",
            command=self._on_diff_change,
        )
        self._diff_menu.pack(side="left")

        # Track canvas
        cf = ctk.CTkFrame(self._container, fg_color=self.TRACK_BG, corner_radius=0)
        cf.pack(fill="both", expand=True, padx=16, pady=(8, 0))
        self._canvas = tk.Canvas(cf, bg=self.TRACK_BG, highlightthickness=0)
        self._canvas.pack(fill="both", expand=True)
        self._canvas.bind("<Configure>", lambda e: self._redraw())

        # Typing entry
        self._input_var = ctk.StringVar()
        self._input_var.trace_add("write", self._on_input_change)
        self._entry = ctk.CTkEntry(
            self._container,
            textvariable=self._input_var,
            height=48,
            corner_radius=10,
            font=ctk.CTkFont("Courier New", 15),
            placeholder_text=s["waiting"],
            border_width=2,
            border_color="#333",
            state="disabled",
        )
        self._entry.pack(fill="x", padx=16, pady=(8, 0))

        # HUD / bottom bar
        bot = ctk.CTkFrame(self._container, fg_color="#080812", height=64)
        bot.pack(fill="x", pady=(8, 0))
        bot.pack_propagate(False)
        stats = ctk.CTkFrame(bot, fg_color="transparent")
        stats.pack(side="left", padx=16, pady=8)
        self._lives_lbl = ctk.CTkLabel(
            stats, text="", font=ctk.CTkFont("Courier New", 13), text_color="#f44336"
        )
        self._lives_lbl.pack(side="left")
        self._score_lbl = ctk.CTkLabel(
            stats,
            text=f"{s['score']}: 0",
            font=ctk.CTkFont("Courier New", 13),
            text_color="#66bb6a",
        )
        self._score_lbl.pack(side="left", padx=16)
        self._wpm_lbl = ctk.CTkLabel(
            stats,
            text=f"{s['wpm']}: —",
            font=ctk.CTkFont("Courier New", 13),
            text_color=self.PLAYER_COLOR,
        )
        self._wpm_lbl.pack(side="left", padx=16)
        self._cd_canvas = tk.Canvas(
            bot, width=120, height=48, bg="#080812", highlightthickness=0
        )
        self._cd_canvas.pack(side="left", expand=True)
        self._build_countdown_lights()
        self._start_btn = ctk.CTkButton(
            bot,
            text=s["start_btn"],
            width=130,
            height=38,
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1b5e20",
            hover_color="#2e7d32",
            command=self._open_countdown,
        )
        self._start_btn.pack(side="right", padx=16, pady=13)

        # Result overlay
        self._overlay = ctk.CTkFrame(
            self._container,
            corner_radius=14,
            fg_color="#0e0e20",
            border_width=2,
            border_color=self.PLAYER_COLOR,
        )
        self._ov_title = ctk.CTkLabel(
            self._overlay,
            text="",
            font=ctk.CTkFont("Courier New", 26, weight="bold"),
            text_color=self.PLAYER_COLOR,
        )
        self._ov_title.pack(pady=(22, 4))
        self._ov_body = ctk.CTkLabel(
            self._overlay,
            text="",
            font=ctk.CTkFont("Courier New", 13),
            text_color="#aaa",
            justify="center",
        )
        self._ov_body.pack(pady=(0, 8))
        self._play_again_btn = ctk.CTkButton(
            self._overlay,
            text=s["play_again"],
            width=130,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._setup_game,
        )
        self._play_again_btn.pack(pady=(4, 22))

        self._container.bind(
            "<Configure>", lambda e: self._container.after_idle(self._redraw)
        )

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _get_strings(self):
        lang = self._language.get() if self._language else "english"
        return self.UI_STRINGS[lang]

    def _word_bank(self) -> list:
        """Return the word list for the current difficulty.

        Custom bank (loaded via ``load_word_bank``) takes priority; falls
        back to the built-in tier if the custom bank has no entry for this
        difficulty.
        """
        diff = self._difficulty.get() if self._difficulty else "Medium"
        builtin = {
            "Easy": self.AMHARIC_WORDS_EASY,
            "Medium": self.AMHARIC_WORDS_MEDIUM,
            "Hard": self.AMHARIC_WORDS_HARD,
        }.get(diff, self.AMHARIC_WORDS_MEDIUM)

        if self._custom_word_bank:
            return self._custom_word_bank.get(diff, builtin)
        return builtin

    def _on_lang_change(self, val):
        self._language.set("amharic" if val == "አማርኛ" else "english")
        self._refresh_ui_strings()
        if not self._game_active:
            self._setup_game()

    def _on_diff_change(self, display_val):
        s = self._get_strings()
        for k, v in s["difficulties"].items():
            if v == display_val:
                self._difficulty.set(k)
                break
        if not self._game_active:
            self._setup_game()

    def _refresh_ui_strings(self):
        if not self._container:
            return
        s = self._get_strings()
        self._title_lbl.configure(text=s["title"])
        self._status_lbl.configure(text=s["subtitle"])
        self._lang_lbl.configure(text=s["language"])
        self._diff_lbl.configure(text=s["difficulty"])
        self._start_btn.configure(text=s["start_btn"])
        self._play_again_btn.configure(text=s["play_again"])
        diff_vals = ["Easy", "Medium", "Hard"]
        diff_display = [s["difficulties"][k] for k in diff_vals]
        cur_key = self._difficulty.get()
        self._diff_menu.configure(values=diff_display)
        self._diff_menu.set(s["difficulties"].get(cur_key, diff_display[1]))
        self._update_hud()

    def _on_back_click(self):
        if self.on_back_button_pressed:
            self.on_back_button_pressed.send(self)

    # ── Countdown lights ──────────────────────────────────────────────────────
    def _build_countdown_lights(self):
        c = self._cd_canvas
        c.delete("all")
        self._cd_items = []
        r, cy = 16, 24
        for i, cx in enumerate([22, 60, 98]):
            c.create_oval(
                cx - r - 2,
                cy - r - 2,
                cx + r + 2,
                cy + r + 2,
                fill="#080818",
                outline="#1a1a35",
                width=1,
            )
            light = c.create_oval(
                cx - r,
                cy - r,
                cx + r,
                cy + r,
                fill=self.LIGHT_COLORS_OFF[i],
                outline="",
            )
            c.create_oval(
                cx - r + 4,
                cy - r + 4,
                cx - r + 10,
                cy - r + 10,
                fill="#ffffff",
                outline="white",
            )
            self._cd_items.append(light)
        self._cd_go_text = c.create_text(
            60, 24, text="", fill="#4caf50", font=("Courier New", 18, "bold")
        )

    def _set_cd_light(self, idx, on):
        self._cd_canvas.itemconfig(
            self._cd_items[idx],
            fill=self.LIGHT_COLORS_ON[idx] if on else self.LIGHT_COLORS_OFF[idx],
        )

    def _open_countdown(self):
        if self._cd_active:
            return
        self._start_btn.configure(state="disabled")
        self._lang_menu.configure(state="disabled")
        self._diff_menu.configure(state="disabled")
        self._status_lbl.configure(text=self._get_strings()["get_ready"])
        self._cd_active = True
        self._cd_step = 0
        for i in range(3):
            self._set_cd_light(i, False)
        self._cd_canvas.itemconfig(self._cd_go_text, text="")
        self._cd_tick()

    def _cd_tick(self):
        for i in range(3):
            self._set_cd_light(i, False)
        self._cd_canvas.itemconfig(self._cd_go_text, text="")
        if self._cd_step < 3:
            self._set_cd_light(self._cd_step, True)
            self._cd_step += 1
            self._cd_job = self._container.after(900, self._cd_tick)
        else:
            for i in range(3):
                self._set_cd_light(i, True)
            self._cd_canvas.itemconfig(self._cd_go_text, text=self._get_strings()["go"])
            self._cd_job = self._container.after(700, self._launch_game)

    def _launch_game(self):
        self._cd_active = False
        self._container.after(
            400,
            lambda: (
                self._cd_canvas.itemconfig(self._cd_go_text, text="")
                if self._cd_canvas.winfo_exists()
                else None
            ),
        )
        for i in range(3):
            self._set_cd_light(i, False)
        s = self._get_strings()
        self._game_active = True
        self._start_time = time.time()
        self._last_frame_time = time.time()
        self._entry.configure(
            state="normal",
            placeholder_text=s["type_here"],
            border_color=self.PLAYER_COLOR,
        )
        self._entry.focus()
        self._status_lbl.configure(text="🚗  Dodge the oncoming cars!")
        self._schedule_spawn()
        self._animate()

    # ── Game setup / teardown ─────────────────────────────────────────────────
    def _band(self):
        return self.DIFFICULTY_BANDS[self._difficulty.get()]

    def _setup_game(self):
        self._hide_overlay()
        self._stop_game()
        s = self._get_strings()

        self._game_active = False
        self._player_lane = self.LANES // 2
        self._lives = self.LIVES_MAX
        self._score = 0
        self._words_typed = 0
        self._cars = []
        self._current_speed = float(self._band()["speed"])
        self._hit_flash = 0
        self._start_time = None

        # ── Pick LANES unique words from the difficulty-appropriate bank ──
        bank = self._word_bank()
        if len(bank) >= self.LANES:
            self._lane_words = random.sample(bank, self.LANES)
        else:
            self._lane_words = random.choices(bank, k=self.LANES)

        self._input_var.set("")
        self._entry.configure(
            state="disabled", placeholder_text=s["waiting"], border_color="#333"
        )
        self._start_btn.configure(state="normal", text=s["start_btn"])
        self._lang_menu.configure(state="normal")
        self._diff_menu.configure(state="normal")
        self._update_hud()
        self._status_lbl.configure(text=s["subtitle"])
        for i in range(3):
            self._set_cd_light(i, False)
        if self._cd_go_text:
            self._cd_canvas.itemconfig(self._cd_go_text, text="")
        self._container.after(50, self._redraw)

    def _stop_game(self):
        self._game_active = False
        self._cd_active = False
        for attr in ("_cd_job", "_anim_job", "_spawn_job"):
            job = getattr(self, attr, None)
            if job:
                try:
                    self._container.after_cancel(job)
                except Exception:
                    pass
                setattr(self, attr, None)

    # ── HUD ───────────────────────────────────────────────────────────────────
    def _update_hud(self):
        s = self._get_strings()
        hearts = "❤️" * self._lives + "🖤" * (self.LIVES_MAX - self._lives)
        self._lives_lbl.configure(text=f"{s['lives']}: {hearts}")
        self._score_lbl.configure(text=f"{s['score']}: {self._score}")
        if self._start_time:
            elapsed = max(time.time() - self._start_time, 0.001)
            wpm = int(self._words_typed / (elapsed / 60))
            self._wpm_lbl.configure(text=f"{s['wpm']}: {wpm}")
        else:
            self._wpm_lbl.configure(text=f"{s['wpm']}: —")

    # ── Spawn ─────────────────────────────────────────────────────────────────
    def _spawn_interval_ms(self):
        b = self._band()
        tiers = self._score // self.RAMP_EVERY
        return max(b["spawn_min_ms"], b["spawn_base_ms"] - tiers * b["spawn_ramp_ms"])

    def _schedule_spawn(self):
        if not self._game_active:
            return
        self._spawn_job = self._container.after(
            self._spawn_interval_ms(), self._do_spawn
        )

    def _do_spawn(self):
        if not self._game_active:
            return
        cw = self._canvas_width()
        lane = random.randint(0, self.LANES - 1)
        color = random.choice(self.NPC_COLOR_POOL)
        self._cars.append(self._Car(lane, cw + self.SPAWN_X_PAD, color))
        self._schedule_spawn()

    # ── Input ─────────────────────────────────────────────────────────────────
    def _on_input_change(self, *_):
        if not self._game_active:
            return
        typed = self._input_var.get().strip()
        for i, word in enumerate(self._lane_words):
            if typed == word:
                self._switch_to_lane(i)
                self._input_var.set("")
                return
        self._draw_scene()

    def _switch_to_lane(self, lane_idx):
        self._player_lane = lane_idx
        self._words_typed += 1
        if self._words_typed % self.RAMP_EVERY == 0:
            self._current_speed += self.SPEED_RAMP
        bank = self._word_bank()
        used = {self._lane_words[i] for i in range(self.LANES) if i != lane_idx}
        pool = [w for w in bank if w not in used] or bank
        self._lane_words[lane_idx] = random.choice(pool)
        self._update_hud()
        self._redraw()

    # ── Animation loop ────────────────────────────────────────────────────────
    def _animate(self):
        if not self._game_active:
            return
        now = time.time()
        dt = min(now - (self._last_frame_time or now), 0.1)
        self._last_frame_time = now
        for car in self._cars:
            car.x -= self._current_speed * dt

        hit_threshold = self.CAR_W * self.HIT_BOX_RATIO
        surviving = []
        score_changed = False
        for car in self._cars:
            if not car.resolved:
                if (
                    car.lane == self._player_lane
                    and abs(car.x - self.PLAYER_X) < hit_threshold
                ):
                    car.resolved = True
                    self._hit_flash = self.HIT_FLASH_FRAMES
                    self._lives -= 1
                    self._update_hud()
                    if self._lives <= 0:
                        surviving.append(car)
                        self._cars = surviving
                        self._end_game()
                        return
                elif car.x < self.PLAYER_X - self.CAR_W:
                    car.resolved = True
                    self._score += 1
                    score_changed = True
            if car.x > -(self.CAR_W * 2):
                surviving.append(car)
        self._cars = surviving
        if score_changed:
            self._update_hud()
        if self._hit_flash > 0:
            self._hit_flash -= 1
        self._redraw()
        self._anim_job = self._container.after(self.FRAME_MS, self._animate)

    # ── End game ──────────────────────────────────────────────────────────────
    def _end_game(self):
        self._game_active = False
        for attr in ("_anim_job", "_spawn_job"):
            job = getattr(self, attr, None)
            if job:
                try:
                    self._container.after_cancel(job)
                except Exception:
                    pass
                setattr(self, attr, None)
        self._entry.configure(state="disabled")
        self._start_btn.configure(state="normal")
        s = self._get_strings()
        elapsed = max(time.time() - (self._start_time or time.time()), 0.001)
        wpm = int(self._words_typed / (elapsed / 60))
        body = (
            f"{s['your_score']}: {self._score}\n"
            f"{s['your_wpm']}: {wpm}\n\n"
            f"{s['well_done']}"
        )
        self._show_overlay(s["game_over"], body)

    # ── Drawing ───────────────────────────────────────────────────────────────
    def _canvas_width(self):
        w = self._canvas.winfo_width()
        return w if w > 100 else 860

    def _canvas_height(self):
        h = self._canvas.winfo_height()
        return h if h > 50 else self.TRACK_H * self.LANES + 30

    def _lane_cy(self, lane):
        return lane * self.TRACK_H + 15 + self.TRACK_H // 2

    def _redraw(self):
        self._draw_track()
        self._draw_scene()

    def _draw_track(self):
        c = self._canvas
        cw = self._canvas_width()
        ch = self._canvas_height()
        c.delete("track")

        # ── Full-canvas road base ──────────────────────────────────────────
        c.create_rectangle(0, 0, cw, ch, fill=self.ROAD_COLOR, outline="", tags="track")

        # ── Thin grass edge strips (top 15 px, bottom 15 px only) ─────────
        GRASS_EDGE = 15
        c.create_rectangle(
            0, 0, cw, GRASS_EDGE, fill=self.GRASS_COLOR, outline="", tags="track"
        )
        # Bottom grass only goes to actual canvas height, not beyond the last lane
        last_lane_bottom = self.LANES * self.TRACK_H + GRASS_EDGE
        c.create_rectangle(
            0, last_lane_bottom, cw, ch, fill=self.GRASS_COLOR, outline="", tags="track"
        )

        # ── Lane road surfaces + dashed dividers ──────────────────────────
        for lane in range(self.LANES):
            y0 = lane * self.TRACK_H + GRASS_EDGE
            y1 = y0 + self.TRACK_H
            c.create_rectangle(
                0, y0 + 3, cw, y1 - 3, fill=self.ROAD_COLOR, outline="", tags="track"
            )
            if lane < self.LANES - 1:
                for x in range(0, cw, 28):
                    c.create_rectangle(
                        x,
                        y1 - 7,
                        x + 14,
                        y1 - 5,
                        fill=self.STRIPE_COLOR,
                        outline="",
                        tags="track",
                    )

        # ── Player zone: subtle semi-transparent tint (NOT a solid wall) ──
        # The road still shows through behind the player car.
        gx = self.PLAYER_X + self.CAR_W // 2 + 12
        # Stipple gives a darkened-but-see-through effect on Tk canvas
        c.create_rectangle(
            0, 0, gx, ch, fill="#09091a", outline="", stipple="gray50", tags="track"
        )
        c.create_line(gx, 0, gx, ch, fill="#1e1e3a", width=2, dash=(6, 4), tags="track")

    def _draw_scene(self):
        c = self._canvas
        typed = self._input_var.get().strip() if self._input_var else ""
        c.delete("car")
        c.delete("word")

        for lane in range(self.LANES):
            word = self._lane_words[lane] if lane < len(self._lane_words) else ""
            cy = self._lane_cy(lane)
            is_player = lane == self._player_lane

            danger = any(
                car.lane == lane
                and self.PLAYER_X < car.x < self.PLAYER_X + self.DANGER_LOOKAHEAD
                for car in self._cars
            )

            if is_player:
                word_color = self.WORD_PLAYER_CLR
            elif danger:
                word_color = self.WORD_DANGER_CLR
            else:
                word_color = self.WORD_DEFAULT_CLR

            is_partial = bool(typed) and word.startswith(typed) and not is_player
            if is_partial:
                est_w = max(len(word) * 14, 40)
                c.create_rectangle(
                    self.WORD_X - 8,
                    cy - 14,
                    self.WORD_X + est_w + 8,
                    cy + 14,
                    fill="#0d2a0d",
                    outline="#4caf50",
                    width=1,
                    tags="word",
                )
                word_color = self.WORD_HINT_CLR

            c.create_text(
                self.WORD_X,
                cy,
                text=word,
                fill=word_color,
                font=("Courier New", 13, "bold"),
                anchor="w",
                tags="word",
            )

            if is_player:
                c.create_text(
                    self.WORD_X - 16,
                    cy,
                    text="▶",
                    fill=self.PLAYER_COLOR,
                    font=("Courier New", 11),
                    anchor="e",
                    tags="word",
                )
            if danger and not is_player:
                c.create_text(
                    self.WORD_X - 16,
                    cy,
                    text="⚠",
                    fill=self.WORD_DANGER_CLR,
                    font=("Courier New", 11),
                    anchor="e",
                    tags="word",
                )

        for car in self._cars:
            self._draw_car(
                c, int(car.x), self._lane_cy(car.lane), car.color, facing_left=True
            )

        pcol = self.HIT_COLOR if self._hit_flash > 0 else self.PLAYER_COLOR
        self._draw_car(
            c,
            self.PLAYER_X,
            self._lane_cy(self._player_lane),
            pcol,
            label="YOU",
            facing_left=False,
        )

    def _draw_car(self, c, x, y, color, label="", facing_left=True):
        hw, hh = self.CAR_W // 2, self.CAR_H // 2
        c.create_oval(
            x - hw + 4,
            y + hh - 2,
            x + hw - 4,
            y + hh + 5,
            fill="#000",
            outline="",
            tags="car",
        )
        c.create_rectangle(
            x - hw, y - hh + 6, x + hw, y + hh, fill=color, outline="", tags="car"
        )
        c.create_rectangle(
            x - hw + 10,
            y - hh,
            x + hw - 8,
            y - hh + 8,
            fill=color,
            outline="",
            tags="car",
        )
        c.create_rectangle(
            x - hw + 11,
            y - hh + 1,
            x + hw - 9,
            y - hh + 7,
            fill="#1a2a3a",
            outline="",
            tags="car",
        )
        if facing_left:
            c.create_rectangle(
                x - hw,
                y - hh + 8,
                x - hw + 4,
                y - hh + 14,
                fill="#fffde7",
                outline="",
                tags="car",
            )
            c.create_rectangle(
                x + hw - 4,
                y - hh + 8,
                x + hw,
                y - hh + 14,
                fill="#ff1744",
                outline="",
                tags="car",
            )
        else:
            c.create_rectangle(
                x - hw,
                y - hh + 8,
                x - hw + 4,
                y - hh + 14,
                fill="#ff1744",
                outline="",
                tags="car",
            )
            c.create_rectangle(
                x + hw - 4,
                y - hh + 8,
                x + hw,
                y - hh + 14,
                fill="#fffde7",
                outline="",
                tags="car",
            )
        for wx in [x - hw + 9, x + hw - 9]:
            c.create_oval(
                wx - 7,
                y + hh - 9,
                wx + 7,
                y + hh + 5,
                fill="#222",
                outline="#444",
                width=2,
                tags="car",
            )
            c.create_oval(
                wx - 3,
                y + hh - 5,
                wx + 3,
                y + hh + 1,
                fill="#555",
                outline="",
                tags="car",
            )
        if label:
            c.create_text(
                x - hw - 6,
                y,
                text=label,
                fill=color,
                font=("Courier New", 9, "bold"),
                anchor="e",
                tags="car",
            )

    # ── Overlay ───────────────────────────────────────────────────────────────
    def _show_overlay(self, title, body):
        self._ov_title.configure(text=title)
        self._ov_body.configure(text=body)
        self._overlay.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.60)

    def _hide_overlay(self):
        if self._overlay:
            self._overlay.place_forget()


class TypingTestMenu(Menu):
    """
    Usage
    -----
        menu = TypingTestMenu(root, language_manager, word_bank_path="assets/words_en.json")
        menu.open_menu()
        menu.close_menu()

    Signals
    -------
        menu.on_back_button_pressed, fired when the back button is clicked
    """

    # ── colour tokens ──────────────────────────────────────────────────────────
    _CORRECT_W = "#22c55e"
    _INCORRECT_W = "#ef4444"
    _CORRECT_C = "#86efac"
    _INCORRECT_C = "#fca5a5"
    _UNTYPED_DARK = "#6b7280"
    _UNTYPED_LITE = "#9ca3af"
    _ACTIVE_FG_D = "#e2e8f0"
    _ACTIVE_FG_L = "#1e293b"
    _ACTIVE_BG_D = "#374151"
    _ACTIVE_BG_L = "#dbeafe"
    _CARET_BG = "#3b82f6"
    _CARET_FG = "#ffffff"

    # ── analytics colour tokens ────────────────────────────────────────────────
    _GRAPH_BG_D = "#1a1b2e"
    _GRAPH_BG_L = "#f1f5f9"
    _GRAPH_AXIS_D = "#6b7280"
    _GRAPH_AXIS_L = "#374151"
    _GRAPH_GRID_D = "#2a2a40"
    _GRAPH_GRID_L = "#e2e8f0"
    _GRAPH_TXT_D = "#e2e8f0"
    _GRAPH_TXT_L = "#1e293b"
    _GRAPH_PT_D = "#60a5fa"
    _GRAPH_PT_L = "#2563eb"
    _GRAPH_LN_D = "#334155"
    _GRAPH_LN_L = "#cbd5e1"
    _GRAPH_AVG_D = "#f59e0b"
    _GRAPH_AVG_L = "#d97706"

    # ── analytics options (all class-level) ───────────────────────────────────
    _YAXIS_OPTIONS = ["WPM", "Accuracy"]
    _PERIOD_OPTIONS = ["Hour", "Day", "Week", "Month", "Year"]
    _STAT_OPTIONS = ["Average", "Best", "Worst", "Count"]
    _DB_NAME = "typing_results.db"
    _GRAPH_PT_R = 5  # point radius in pixels
    _GRAPH_MARGIN = (65, 25, 25, 55)  # left, right, top, bottom

    # ── period → seconds lookup (class-level) ─────────────────────────────────
    _PERIOD_SECONDS = {
        "Hour": 3_600,
        "Day": 86_400,
        "Week": 604_800,
        "Month": 2_592_000,
        "Year": 31_536_000,
    }

    # ── built-in word bank ─────────────────────────────────────────────────────
    _DEFAULT_WORDS = [
        "ነው",
        "ነበር",
        "አለ",
        "የለም",
        "አይደለም",
        "ይሆናል",
        "ሆነ",
        "አለች",
        "ነች",
        "ናቸው",
        "ሆኑ",
        "አደረገ",
        "አለ",
        "ሄደ",
        "መጣ",
        "አየ",
        "አወቀ",
        "ወሰደ",
        "ሰጠ",
        "ተናገረ",
        "አለፈ",
        "ቆመ",
        "ጀመረ",
        "ጨረሰ",
        "ተመለሰ",
        "ፈለገ",
        "አገኘ",
        "ሞከረ",
        "ቻለ",
        "ሞተ",
        "እና",
        "ወይም",
        "ግን",
        "ስለዚህ",
        "ምክንያቱም",
        "እንዲሁም",
        "አሁን",
        "ከዚያ",
        "እዚህ",
        "እዚያ",
        "ዛሬ",
        "ትናንት",
        "ነገ",
        "ብዙ",
        "ትንሽ",
        "ሁሉ",
        "አንድ",
        "ሁለት",
        "ሦስት",
        "አራት",
        "አምስት",
        "ስድስት",
        "ሰባት",
        "ስምንት",
        "ዘጠኝ",
        "አስር",
        "ሰው",
        "ልጅ",
        "ሴት",
        "ወንድ",
        "ቤት",
        "ስም",
        "ጊዜ",
        "ቀን",
        "ዓመት",
        "ወር",
        "ሥራ",
        "ገንዘብ",
        "ምግብ",
        "ውሃ",
        "አገር",
        "ከተማ",
        "መንገድ",
        "ትምህርት",
        "መጽሐፍ",
        "ቋንቋ",
        "ቤተሰብ",
        "ወዳጅ",
        "ፍቅር",
        "ሰላም",
        "ችግር",
        "መልስ",
        "ጥያቄ",
        "ምክር",
        "ሐሳብ",
        "ፈቃድ",
        "እርዳታ",
        "እኔ",
        "አንተ",
        "እሱ",
        "እሷ",
        "እኛ",
        "እናንተ",
        "እነሱ",
        "የእኔ",
        "የአንተ",
        "የእሱ",
        "ጥሩ",
        "መጥፎ",
        "ትልቅ",
        "ትንሽ",
        "አዲስ",
        "ያረጀ",
        "ፈጣን",
        "ዝግተኛ",
        "ቀላል",
        "ከባድ",
    ]

    # ─────────────────────────────────────────────────────────────────────────
    # __init__
    # ─────────────────────────────────────────────────────────────────────────

    def __init__(self, root, language_manager: LanguageManager, word_bank_path=None):
        super().__init__()
        if not root:
            warnings.warn(
                "attempted to create TypingTestMenu with none root, menu not created"
            )
            return
        if not language_manager:
            warnings.warn(
                "attempted to create TypingTestMenu with none language_manager, "
                "menu not created"
            )
            return

        self.root = root
        self.language_manager = language_manager
        self.on_back_button_pressed = signal(f"on back button pressed {self}")

        self._word_bank = self._load_word_bank(word_bank_path)

        # ── typing-test state ──────────────────────────────────────────────
        self._words: list = []
        self._committed: list = []  # list[bool]
        self._current_word_idx: int = 0
        self._current_typed: str = ""
        self._start_time = None
        self._running: bool = False
        self._timer_thread = None
        self._test_duration: int = 30
        self._time_left: float = 30.0
        self._wpm: int = 0
        self._acc: int = 100
        self._finished: bool = False

        # ── test-view widget references ────────────────────────────────────
        self.main_frame = None
        self.header_frame = None
        self.back_button = None
        self.title_label = None
        self.control_bar = None
        self.time_label = None
        self.stat_label = None
        self._dur_buttons: dict = {}
        self.text_canvas = None
        self.input_field = None
        self._input_var = None
        self.wpm_label = None
        self.acc_label = None
        self.restart_btn = None
        self._analytics_btn = None  # NEW – header shortcut to analytics

        # ── result overlay ─────────────────────────────────────────────────
        self._result_overlay = None
        self._result_wpm_val = None
        self._result_acc_val = None

        # ── analytics overlay (built lazily) ──────────────────────────────
        self._analytics_frame = None
        self._graph_canvas = None  # raw tk.Canvas
        self._y_var = None  # StringVar: WPM | Accuracy
        self._period_var = None  # StringVar: Hour | Day | Week | Month | Year
        self._stat_var = None  # StringVar: Average | Best | Worst | Count
        self._stat_val_label = None
        self._date_var = None  # StringVar: specific date filter
        self._date_menu = None

    # ─────────────────────────────────────────────────────────────────────────
    # Menu protocol
    # ─────────────────────────────────────────────────────────────────────────

    def open_menu(self):
        self._init_db()  # ensure DB exists
        if not self.main_frame:
            self.main_frame = CTkFrame(self.root, fg_color="transparent")
            self._build_ui()

        self.main_frame.pack(expand=True, fill="both")
        self._new_test()
        self.root.update_idletasks()

    def close_menu(self):
        self._running = False
        if self.main_frame:
            self.main_frame.pack_forget()
        self.root.update_idletasks()

    # ─────────────────────────────────────────────────────────────────────────
    # Build – test view
    # ─────────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        self._build_header()
        self._build_control_bar()
        self._build_text_area()
        self._build_input_area()
        self._build_stats_bar()
        self._build_result_overlay()
        # analytics frame is built lazily in _show_analytics()

    # ── Header: back button + title + analytics shortcut ──────────────────────

    def _build_header(self):
        if not self.header_frame:
            self.header_frame = CTkFrame(self.main_frame, fg_color="transparent")
            self.header_frame.pack(fill="x", side="top")

        back_black_icon_path = (
            pathlib.Path(__file__).parent.parent
            / "assets"
            / "images"
            / "icons"
            / "back_icon_black.png"
        )
        back_white_icon_path = (
            pathlib.Path(__file__).parent.parent
            / "assets"
            / "images"
            / "icons"
            / "back_icon_white.png"
        )

        if not self.back_button:
            self.back_button = ImageButton(
                self.header_frame,
                light_image_path=back_black_icon_path,
                dark_image_path=back_white_icon_path,
                sizex=30,
                sizey=30,
                size_change_amount=1,
            )
            self.back_button.pack(side="left", pady=10, padx=10)
            self.back_button.on_mouse_click.connect(self._on_back_icon_pressed)

        if not self.title_label:
            self.title_label = CTkLabel(self.header_frame, text="", font=("Roboto", 25))
            self.language_manager.register_widget(self.title_label, "typing_test_title")
            self.title_label.pack(side="left", pady=10, padx=4)

        if not self._analytics_btn:
            self._analytics_btn = CTkButton(
                self.header_frame,
                text="",
                width=95,
                height=30,
                font=("Roboto", 13),
                command=self._show_analytics,
            )
            self.language_manager.register_widget(self._analytics_btn, "analytics_btn")
            self._analytics_btn.pack(side="right", padx=10, pady=10)

    # ── Input area ─────────────────────────────────────────────────────────────

    def _build_input_area(self):
        input_frame = CTkFrame(self.main_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=10, pady=50)

        self._input_var = StringVar()
        self._input_var.trace_add("write", self._on_input_change)

        self.input_field = CTkEntry(
            input_frame,
            textvariable=self._input_var,
            font=("Courier New", 17, "bold"),
            height=44,
            placeholder_text="",
        )
        self.input_field.pack(fill="x")
        self.input_field.bind("<KeyRelease>", self._on_key_release)

    # ── Stats bar ──────────────────────────────────────────────────────────────

    def _build_stats_bar(self):
        stats_frame = CTkFrame(self.main_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=10, pady=5)

        self.wpm_label = CTkLabel(stats_frame, text="", font=("Roboto", 14, "bold"))
        self.language_manager.register_widget(self.wpm_label, "typing_wpm_live")
        self.wpm_label.pack(side="left", padx=(0, 16))

        self.acc_label = CTkLabel(stats_frame, text="", font=("Roboto", 14, "bold"))
        self.language_manager.register_widget(self.acc_label, "typing_acc_live")
        self.acc_label.pack(side="left")

        self.restart_btn = CTkButton(
            stats_frame,
            text="",
            width=110,
            height=34,
            font=("Roboto", 14),
            command=self._new_test,
        )
        self.language_manager.register_widget(self.restart_btn, "typing_restart")
        self.restart_btn.pack(side="right")

    # ── Result overlay ─────────────────────────────────────────────────────────

    def _build_result_overlay(self):
        """Card placed with place() over the centre of main_frame."""
        self._result_overlay = CTkFrame(
            self.main_frame,
            corner_radius=16,
            border_width=2,
        )

        self._result_title_lbl = CTkLabel(
            self._result_overlay, text="", font=("Roboto", 18, "bold")
        )
        self.language_manager.register_widget(
            self._result_title_lbl, "typing_test_complete"
        )
        self._result_title_lbl.pack(pady=(24, 6))

        stats_inner = CTkFrame(self._result_overlay)
        stats_inner.pack(padx=24, pady=8, fill="x")
        stats_inner.grid_columnconfigure(0, weight=1, minsize=120)
        stats_inner.grid_columnconfigure(1, weight=1, minsize=120)

        wpm_hdr = CTkLabel(stats_inner, text="", font=("Roboto", 13))
        self.language_manager.register_widget(wpm_hdr, "typing_wpm")
        wpm_hdr.grid(row=0, column=0, pady=(16, 2), padx=16)

        acc_hdr = CTkLabel(stats_inner, text="", font=("Roboto", 13))
        self.language_manager.register_widget(acc_hdr, "typing_accuracy")
        acc_hdr.grid(row=0, column=1, pady=(16, 2), padx=16)

        self._result_wpm_val = CTkLabel(
            stats_inner, text="—", font=("Roboto", 52, "bold")
        )
        self._result_wpm_val.grid(row=1, column=0, pady=(0, 16), padx=16)

        self._result_acc_val = CTkLabel(
            stats_inner, text="—", font=("Roboto", 52, "bold")
        )
        self._result_acc_val.grid(row=1, column=1, pady=(0, 16), padx=16)

        try_again_btn = CTkButton(
            self._result_overlay,
            text="",
            font=("Roboto", 15),
            height=40,
            command=self._new_test,
        )
        self.language_manager.register_widget(try_again_btn, "typing_try_again")
        try_again_btn.pack(pady=(6, 22), padx=30, fill="x")

    def _show_result_overlay(self):
        self._result_overlay.place(relx=0.5, rely=0.5, anchor="center")
        self._result_overlay.lift()

    def _hide_result_overlay(self):
        self._result_overlay.place_forget()

    # ─────────────────────────────────────────────────────────────────────────
    # Test logic
    # ─────────────────────────────────────────────────────────────────────────

    def _new_test(self):
        self._finished = False
        self._running = False
        self._start_time = None
        self._time_left = float(self._test_duration)
        self._committed = []
        self._current_word_idx = 0
        self._current_typed = ""
        self._wpm = 0
        self._acc = 100
        self._words = random.choices(self._word_bank, k=70)

        self._hide_result_overlay()
        self._render_text()
        self._input_var.set("")
        self.input_field.configure(
            state="normal",
            placeholder_text=self.language_manager.translate("typing_placeholder")
            or "",
        )
        self.input_field.focus()
        self.stat_label.configure(text=str(self._test_duration))
        self.wpm_label.configure(
            text=self.language_manager.translate("typing_wpm_live") or "WPM: —"
        )
        self.acc_label.configure(
            text=self.language_manager.translate("typing_acc_live") or "Accuracy: —%"
        )
        self._update_dur_buttons(self._test_duration)

    def _set_duration(self, dur: int):
        self._test_duration = dur
        self._update_dur_buttons(dur)
        self._new_test()

    def _update_dur_buttons(self, active: int):
        for dur, btn in self._dur_buttons.items():
            if dur == active:
                btn.configure(fg_color=("#1f6aa5", "#1f6aa5"))
            else:
                btn.configure(fg_color=("gray75", "gray25"))

    # ── Input handlers ─────────────────────────────────────────────────────────

    def _on_input_change(self, *_):
        if self._finished:
            return
        value = self._input_var.get()
        if value.endswith(" ") or value.endswith("\u00a0"):
            self._commit_word(value.rstrip())
            return
        self._current_typed = value
        if self._current_typed and not self._running:
            self._start_timer()
        self._render_text()

    def _on_key_release(self, _event):
        if self._finished:
            return
        value = self._input_var.get()
        if value.endswith(" ") or value.endswith("\u00a0"):
            self._commit_word(value.rstrip())
            return
        self._current_typed = value
        self._render_text()

    def _commit_word(self, typed: str):
        if self._finished:
            return
        typed = typed.strip()
        if not typed:
            self._input_var.set("")
            return

        expected = self._words[self._current_word_idx]
        self._committed.append(typed == expected)
        self._current_word_idx += 1
        self._current_typed = ""
        self._input_var.set("")
        self.input_field.after(
            0,
            lambda: (
                self.input_field.delete(0, "end")
                if self.input_field.winfo_exists()
                else None
            ),
        )

        if not self._running:
            self._start_timer()

        self._render_text()
        self._update_stats()

        if self._current_word_idx >= len(self._words):
            self._finish()

    def _on_back_icon_pressed(self, sender):
        self.on_back_button_pressed.send(self)

    # ── Timer ──────────────────────────────────────────────────────────────────

    def _start_timer(self):
        self._running = True
        self._start_time = time.time()
        self._timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
        self._timer_thread.start()

    def _timer_loop(self):
        while self._running:
            elapsed = time.time() - self._start_time
            self._time_left = max(0.0, self._test_duration - elapsed)
            remaining = int(self._time_left) + (1 if self._time_left > 0 else 0)
            if self.stat_label.winfo_exists():
                self.stat_label.after(
                    0,
                    lambda r=remaining: self.stat_label.configure(text=str(r)),
                )
            self._update_stats()
            if self._time_left <= 0:
                self._running = False
                self.stat_label.after(0, self._finish)
                break
            time.sleep(0.1)

    # ── Stats ──────────────────────────────────────────────────────────────────

    def _update_stats(self):
        if self._start_time is None:
            return
        elapsed = time.time() - self._start_time
        if elapsed < 0.3:
            return
        n = len(self._committed)
        total_chars = sum(len(self._words[i]) for i in range(n))
        correct_chars = sum(
            len(self._words[i]) for i, ok in enumerate(self._committed) if ok
        )
        wpm = int((correct_chars / 5) / (elapsed / 60))
        acc = int((correct_chars / total_chars) * 100) if total_chars else 100
        self._wpm = wpm
        self._acc = acc

        wpm_tpl = (
            self.language_manager.translate("typing_wpm_live_value") or "WPM: {wpm}"
        )
        acc_tpl = (
            self.language_manager.translate("typing_acc_live_value")
            or "Accuracy: {acc}%"
        )
        self.wpm_label.after(
            0, lambda: self.wpm_label.configure(text=wpm_tpl.format(wpm=wpm))
        )
        self.acc_label.after(
            0, lambda: self.acc_label.configure(text=acc_tpl.format(acc=acc))
        )

    # ── Render ─────────────────────────────────────────────────────────────────

    def _theme_colors(self):
        mode = ctk.get_appearance_mode()
        if mode == "Dark":
            return self._UNTYPED_DARK, self._ACTIVE_FG_D, self._ACTIVE_BG_D
        return self._UNTYPED_LITE, self._ACTIVE_FG_L, self._ACTIVE_BG_L

    def _render_text(self):
        untyped, active_fg, active_bg = self._theme_colors()
        tb = self.text_canvas
        tb.configure(state="normal")
        tb.delete("1.0", "end")

        tb.tag_config("correct_word", foreground=self._CORRECT_W)
        tb.tag_config("incorrect_word", foreground=self._INCORRECT_W)
        tb.tag_config("untyped", foreground=untyped)
        tb.tag_config("cur_ok", foreground=self._CORRECT_C)
        tb.tag_config("cur_err", foreground=self._INCORRECT_C)
        tb.tag_config("cur_untyped", foreground=active_fg)
        tb.tag_config("active_bg", background=active_bg)
        tb.tag_config("caret", foreground=self._CARET_FG, background=self._CARET_BG)

        typed = self._current_typed

        for w_idx, word in enumerate(self._words):
            if w_idx > 0:
                tb.insert("end", " ", "untyped")

            if w_idx < len(self._committed):
                tag = "correct_word" if self._committed[w_idx] else "incorrect_word"
                tb.insert("end", word, tag)

            elif w_idx == self._current_word_idx:
                for c_idx, ch in enumerate(word):
                    if c_idx < len(typed):
                        tag = "cur_ok" if typed[c_idx] == ch else "cur_err"
                        tb.insert("end", ch, (tag, "active_bg"))
                    elif c_idx == len(typed):
                        tb.insert("end", ch, ("caret",))
                    else:
                        tb.insert("end", ch, ("cur_untyped", "active_bg"))

                if len(typed) >= len(word):
                    tb.insert("end", " ", ("caret",))
                    for ex in typed[len(word) :]:
                        tb.insert("end", ex, ("cur_err", "active_bg"))
            else:
                tb.insert("end", word, "untyped")

        chars_before = sum(
            len(self._words[i]) + 1 for i in range(self._current_word_idx)
        )
        try:
            tb.see(f"1.0 + {chars_before} chars")
        except Exception:
            pass

        tb.configure(state="disabled")

    # ── Finish (saves result to DB) ────────────────────────────────────────────

    def _finish(self):
        if self._finished:
            return
        self._finished = True
        self._running = False
        self._update_stats()
        self.input_field.configure(state="disabled")
        self._result_wpm_val.configure(text=str(self._wpm))
        self._result_acc_val.configure(text=f"{self._acc}%")
        self._save_result(self._wpm, self._acc, self._test_duration)  # ← persists
        self._show_result_overlay()

    # ── Word bank loader ───────────────────────────────────────────────────────

    @staticmethod
    def _load_word_bank(json_path) -> list:
        """
        Accepts two JSON formats:
            ["word1", "word2", ...]
            {"words": ["word1", "word2", ...]}
        Falls back to the built-in list on any error.
        """
        if json_path is None:
            return TypingTestMenu._DEFAULT_WORDS
        path = pathlib.Path(json_path)
        if not path.exists():
            warnings.warn(
                f"TypingTestMenu: word bank not found at {path}, "
                "using built-in words"
            )
            return TypingTestMenu._DEFAULT_WORDS
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return [str(w) for w in data if w]
            if isinstance(data, dict) and "words" in data:
                return [str(w) for w in data["words"] if w]
            warnings.warn(
                "TypingTestMenu: unexpected word bank format, using built-in words"
            )
        except Exception as exc:
            warnings.warn(
                f"TypingTestMenu: failed to load word bank ({exc}), "
                "using built-in words"
            )
        return TypingTestMenu._DEFAULT_WORDS

    # =========================================================================
    # DATABASE
    # =========================================================================

    @staticmethod
    def _db_path() -> pathlib.Path:
        """Return path to the SQLite file, creating the data/ folder if needed."""
        d = pathlib.Path(__file__).parent.parent / "data"
        d.mkdir(parents=True, exist_ok=True)
        return d / TypingTestMenu._DB_NAME

    def _init_db(self):
        """Create the results table if it doesn't already exist."""
        try:
            with sqlite3.connect(str(self._db_path())) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS results (
                        id       INTEGER PRIMARY KEY AUTOINCREMENT,
                        ts       REAL    NOT NULL,
                        wpm      INTEGER NOT NULL,
                        accuracy INTEGER NOT NULL,
                        duration INTEGER NOT NULL
                    )
                    """)
        except Exception as exc:
            warnings.warn(f"TypingTestMenu: could not init DB ({exc})")

    def _save_result(self, wpm: int, acc: int, duration: int):
        """Persist a completed test to the database."""
        try:
            with sqlite3.connect(str(self._db_path())) as conn:
                conn.execute(
                    "INSERT INTO results (ts, wpm, accuracy, duration) "
                    "VALUES (?, ?, ?, ?)",
                    (time.time(), wpm, acc, duration),
                )
        except Exception as exc:
            warnings.warn(f"TypingTestMenu: could not save result ({exc})")

    def _load_results(self, period: str) -> list:
        delta = self._PERIOD_SECONDS.get(period, 86_400)
        since = time.time() - delta

        date_filter = self._date_var.get() if self._date_var else "All"

        try:
            with sqlite3.connect(str(self._db_path())) as conn:
                if date_filter == "All":
                    return conn.execute(
                        "SELECT ts, wpm, accuracy FROM results "
                        "WHERE ts >= ? ORDER BY ts ASC",
                        (since,),
                    ).fetchall()
                else:
                    # parse the selected date and get midnight-to-midnight bounds
                    day = datetime.datetime.strptime(date_filter, "%Y-%m-%d")
                    day_start = day.replace(hour=0, minute=0, second=0).timestamp()
                    day_end = day.replace(hour=23, minute=59, second=59).timestamp()
                    return conn.execute(
                        "SELECT ts, wpm, accuracy FROM results "
                        "WHERE ts BETWEEN ? AND ? ORDER BY ts ASC",
                        (day_start, day_end),
                    ).fetchall()
        except Exception as exc:
            warnings.warn(f"TypingTestMenu: could not load results ({exc})")
            return []

    # =========================================================================
    # ANALYTICS VIEW
    # =========================================================================

    def _get_recorded_dates(self) -> list:
        """Return a sorted list of date strings ('YYYY-MM-DD') that have recorded tests, plus 'All'."""
        try:
            with sqlite3.connect(str(self._db_path())) as conn:
                rows = conn.execute(
                    "SELECT ts FROM results ORDER BY ts DESC"
                ).fetchall()
            dates = sorted(
                {
                    datetime.datetime.fromtimestamp(r[0]).strftime("%Y-%m-%d")
                    for r in rows
                },
                reverse=True,
            )
            return ["All"] + dates
        except Exception as exc:
            warnings.warn(f"TypingTestMenu: could not load dates ({exc})")
            return ["All"]

    def _refresh_date_dropdown(self):
        """Repopulate the date dropdown with currently recorded dates."""
        if self._date_menu is None:
            return
        dates = self._get_recorded_dates()
        self._date_menu.configure(values=dates)
        if self._date_var.get() not in dates:
            self._date_var.set(dates[0])
        # ── Show / hide ────────────────────────────────────────────────────────────

    def _show_analytics(self):
        if self._analytics_frame is None:
            self._build_analytics_view()
        self._refresh_date_dropdown()  # <-- sync dates with DB
        self._analytics_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self._analytics_frame.lift()
        self.root.after(80, self._update_analytics)

    def _hide_analytics(self):
        if self._analytics_frame:
            self._analytics_frame.place_forget()

    # ── Build ──────────────────────────────────────────────────────────────────

    def _build_analytics_view(self):
        self._analytics_frame = CTkFrame(
            self.main_frame, corner_radius=0, fg_color="transparent"
        )

        # ── header ────────────────────────────────────────────────────────
        hdr = CTkFrame(self._analytics_frame, fg_color="transparent")
        hdr.pack(fill="x", side="top")

        back_btn = CTkButton(
            hdr,
            text="",
            width=80,
            height=30,
            font=("Roboto", 13),
            command=self._hide_analytics,
        )
        self.language_manager.register_widget(back_btn, "analytics_back_btn")
        back_btn.pack(side="left", padx=10, pady=10)

        analytics_title_lbl = CTkLabel(hdr, text="", font=("Roboto", 25))
        self.language_manager.register_widget(analytics_title_lbl, "analytics_title")
        analytics_title_lbl.pack(side="left", padx=4, pady=10)

        # ── control bar ───────────────────────────────────────────────────
        ctrl = CTkFrame(self._analytics_frame, fg_color="transparent")
        ctrl.pack(fill="x", padx=10, pady=(0, 6))

        yaxis_lbl = CTkLabel(ctrl, text="", font=("Roboto", 13))
        self.language_manager.register_widget(yaxis_lbl, "analytics_yaxis_label")
        yaxis_lbl.pack(side="left", padx=(0, 4))

        self._y_var = StringVar(value="WPM")
        CTkOptionMenu(
            ctrl,
            variable=self._y_var,
            values=self._YAXIS_OPTIONS,
            width=115,
            font=("Roboto", 13),
            command=lambda _: self._update_analytics(),
        ).pack(side="left", padx=(0, 18))

        period_lbl = CTkLabel(ctrl, text="", font=("Roboto", 13))
        self.language_manager.register_widget(period_lbl, "analytics_period_label")
        period_lbl.pack(side="left", padx=(0, 4))

        self._period_var = StringVar(value="Day")
        CTkOptionMenu(
            ctrl,
            variable=self._period_var,
            values=self._PERIOD_OPTIONS,
            width=105,
            font=("Roboto", 13),
            command=lambda _: self._update_analytics(),
        ).pack(side="left", padx=(0, 18))

        stat_lbl = CTkLabel(ctrl, text="", font=("Roboto", 13))
        self.language_manager.register_widget(stat_lbl, "analytics_stat_label")
        stat_lbl.pack(side="left", padx=(0, 4))

        self._stat_var = StringVar(value="Average")
        CTkOptionMenu(
            ctrl,
            variable=self._stat_var,
            values=self._STAT_OPTIONS,
            width=115,
            font=("Roboto", 13),
            command=lambda _: self._update_stat_display(),
        ).pack(side="left", padx=(0, 18))

        # ── date filter ───────────────────────────────────────────────────
        ctrl2 = CTkFrame(self._analytics_frame, fg_color="transparent")
        ctrl2.pack(fill="x", padx=10, pady=(0, 6))

        date_lbl = CTkLabel(ctrl2, text="", font=("Roboto", 13))
        self.language_manager.register_widget(date_lbl, "analytics_date_label")
        date_lbl.pack(side="left", padx=(0, 4))

        self._date_var = StringVar(value="All")
        self._date_menu = CTkOptionMenu(
            ctrl2,
            variable=self._date_var,
            values=self._get_recorded_dates(),
            width=150,
            font=("Roboto", 13),
            command=lambda _: self._update_analytics(),
        )
        self._date_menu.pack(side="left")

        # ── graph area ────────────────────────────────────────────────────
        graph_frame = CTkFrame(self._analytics_frame, corner_radius=10)
        graph_frame.pack(fill="both", expand=True, padx=10, pady=(0, 4))

        self._graph_canvas = tk.Canvas(graph_frame, highlightthickness=0)
        self._graph_canvas.pack(fill="both", expand=True, padx=4, pady=4)
        self._graph_canvas.bind("<Configure>", lambda _e: self._draw_graph())

        # ── stat summary row ──────────────────────────────────────────────
        stat_frame = CTkFrame(self._analytics_frame, fg_color="transparent")
        stat_frame.pack(fill="x", padx=10, pady=(2, 10))

        self._stat_val_label = CTkLabel(
            stat_frame,
            text=self.language_manager.translate("analytics_complete_a_test")
            or "Complete a test to see analytics.",
            font=("Roboto", 14, "bold"),
        )
        self._stat_val_label.pack(pady=5)

    def _update_stat_display(self):
        """Compute and show the selected stat for the current period."""
        if self._stat_val_label is None:
            return

        period = self._period_var.get()
        stat = self._stat_var.get()
        rows = self._load_results(period)

        if not rows:
            self._stat_val_label.configure(
                text=f"No tests recorded in this {period.lower()}."
            )
            return

        n = len(rows)
        wpms = [r[1] for r in rows]
        accs = [r[2] for r in rows]

        if stat == "Average":
            w = int(sum(wpms) / n)
            a = int(sum(accs) / n)
            text = f"Avg WPM: {w}  •  Avg Accuracy: {a}%  •  Tests: {n}"
        elif stat == "Best":
            text = (
                f"Best WPM: {max(wpms)}  •  "
                f"Best Accuracy: {max(accs)}%  •  Tests: {n}"
            )
        elif stat == "Worst":
            text = (
                f"Worst WPM: {min(wpms)}  •  "
                f"Worst Accuracy: {min(accs)}%  •  Tests: {n}"
            )
        elif stat == "Count":
            text = f"Tests completed this {period.lower()}: {n}"
        else:
            text = ""

        self._stat_val_label.configure(text=text)

    def _build_control_bar(self):
        if not self.control_bar:
            self.control_bar = CTkFrame(self.main_frame, fg_color="transparent")
            self.control_bar.pack(fill="x", padx=10, pady=(0, 8))

        self.stat_label = CTkLabel(
            self.control_bar,
            text=str(self._test_duration),
            font=("Roboto", 34, "bold"),
        )
        self.stat_label.pack(side="right", padx=16)

        centre_group = CTkFrame(self.control_bar, fg_color="transparent")
        centre_group.pack(side="left", expand=True)

        self.time_label = CTkLabel(centre_group, text="", font=("Roboto", 13))
        self.language_manager.register_widget(self.time_label, "typing_time_label")
        self.time_label.pack(side="left", padx=(0, 6))

        for dur in [15, 30, 60, 120]:
            b = CTkButton(
                centre_group,
                text=f"{dur}s",
                width=52,
                height=30,
                font=("Roboto", 13),
                command=lambda d=dur: self._set_duration(d),
            )
            b.pack(side="left", padx=3)
            self._dur_buttons[dur] = b

    def _build_text_area(self):
        text_frame = CTkFrame(self.main_frame, corner_radius=10)
        text_frame.pack(fill="x", padx=10, pady=(0, 5))

        self.text_canvas = CTkTextbox(
            text_frame,
            font=("Courier New", 22, "bold"),
            wrap="word",
            state="disabled",
            height=180,
            border_width=0,
        )
        self.text_canvas.pack(fill="both", expand=True, padx=6, pady=6)
        # ── Graph drawing ──────────────────────────────────────────────────────────

    def _update_analytics(self):
        """Redraw the graph and refresh the stat summary."""
        self._draw_graph()
        self._update_stat_display()

    @staticmethod
    def _format_ts(ts: float, period: str) -> str:
        """Return a short label for a Unix timestamp given the active period."""
        dt = datetime.datetime.fromtimestamp(ts)
        if period in ("Hour", "Day"):
            return dt.strftime("%H:%M")
        if period == "Week":
            return dt.strftime("%a %d")
        if period == "Month":
            return dt.strftime("%b %d")
        if period == "Year":
            return dt.strftime("%b %Y")
        return dt.strftime("%H:%M")

    def _draw_graph(self):
        c = self._graph_canvas
        if c is None or not c.winfo_exists():
            return
        c.delete("all")

        W = c.winfo_width()
        H = c.winfo_height()
        if W < 10 or H < 10:
            return

        # ── theme colours ──────────────────────────────────────────────
        is_dark = ctk.get_appearance_mode() == "Dark"
        bg = self._GRAPH_BG_D if is_dark else self._GRAPH_BG_L
        ax = self._GRAPH_AXIS_D if is_dark else self._GRAPH_AXIS_L
        grd = self._GRAPH_GRID_D if is_dark else self._GRAPH_GRID_L
        txt = self._GRAPH_TXT_D if is_dark else self._GRAPH_TXT_L
        pt = self._GRAPH_PT_D if is_dark else self._GRAPH_PT_L
        ln = self._GRAPH_LN_D if is_dark else self._GRAPH_LN_L
        av = self._GRAPH_AVG_D if is_dark else self._GRAPH_AVG_L

        c.configure(bg=bg)

        ml, mr, mt, mb = self._GRAPH_MARGIN
        pw = W - ml - mr
        ph = H - mt - mb
        ox = ml
        oy = H - mb

        # ── data ───────────────────────────────────────────────────────
        period = self._period_var.get()
        y_axis = self._y_var.get()
        rows = self._load_results(period)

        # ── Y range ────────────────────────────────────────────────────
        if y_axis == "Accuracy":
            y_min, y_max = 0, 100
        else:
            if rows:
                raw_max = max(r[1] for r in rows)
                y_max = ((max(raw_max + 10, 50) + 9) // 10) * 10
            else:
                y_max = 100
            y_min = 0

        # ── X range ────────────────────────────────────────────────────
        now = time.time()
        delta = self._PERIOD_SECONDS.get(period, 86_400)
        t_start = now - delta
        t_end = now

        # ── coordinate helpers ─────────────────────────────────────────
        def to_cx(ts: float) -> float:
            span = t_end - t_start
            return ox + ((ts - t_start) / span if span else 0.5) * pw

        def to_cy(val: float) -> float:
            span = y_max - y_min
            return oy - ((val - y_min) / span if span else 0.5) * ph

        # ── grid lines ────────────────────────────────────────────────
        N_Y, N_X = 5, 5
        for i in range(N_Y + 1):
            yp = oy - int(i * ph / N_Y)
            c.create_line(ox, yp, ox + pw, yp, fill=grd, width=1)
        for i in range(N_X + 1):
            xp = ox + int(i * pw / N_X)
            c.create_line(xp, mt, xp, oy, fill=grd, width=1)

        # ── axes ──────────────────────────────────────────────────────
        c.create_line(ox, mt, ox, oy + 1, fill=ax, width=2)
        c.create_line(ox, oy, ox + pw, oy, fill=ax, width=2)

        # ── Y-axis labels + title ──────────────────────────────────────
        for i in range(N_Y + 1):
            val = y_min + (y_max - y_min) * i / N_Y
            yp = oy - int(i * ph / N_Y)
            lbl = f"{int(val)}%" if y_axis == "Accuracy" else str(int(val))
            c.create_text(
                ox - 6, yp, text=lbl, fill=txt, anchor="e", font=("Roboto", 9)
            )

        y_title = "Accuracy %" if y_axis == "Accuracy" else "WPM"
        c.create_text(
            13,
            mt + ph // 2,
            text=y_title,
            fill=txt,
            font=("Roboto", 10, "bold"),
            angle=90,
        )

        # ── X-axis labels ──────────────────────────────────────────────
        for i in range(N_X + 1):
            ts = t_start + i * (t_end - t_start) / N_X
            xp = ox + int(i * pw / N_X)
            lbl = self._format_ts(ts, period)
            c.create_text(
                xp, oy + 14, text=lbl, fill=txt, anchor="n", font=("Roboto", 8)
            )

        # ── no-data placeholder ────────────────────────────────────────
        if not rows:
            c.create_text(
                ox + pw // 2,
                mt + ph // 2,
                text=self.language_manager.translate("analytics_no_data")
                or (
                    "No tests recorded in this period.\n"
                    "Complete a test to populate the chart."
                ),
                fill=txt,
                font=("Roboto", 12),
                justify="center",
            )
            return

        # ── connecting line ────────────────────────────────────────────
        pts = []
        for row in rows:
            v = row[1] if y_axis == "WPM" else row[2]
            pts += [to_cx(row[0]), to_cy(v)]
        if len(pts) >= 4:
            c.create_line(*pts, fill=ln, width=1.5, smooth=True)

        # ── average reference line ─────────────────────────────────────
        vals = [r[1] if y_axis == "WPM" else r[2] for r in rows]
        avg_val = sum(vals) / len(vals)
        avg_y = to_cy(avg_val)
        avg_lbl = (
            f"avg {int(avg_val)}%" if y_axis == "Accuracy" else f"avg {int(avg_val)}"
        )
        c.create_line(ox, avg_y, ox + pw, avg_y, fill=av, width=1, dash=(6, 4))
        c.create_text(
            ox + pw - 4,
            avg_y - 8,
            text=avg_lbl,
            fill=av,
            anchor="e",
            font=("Roboto", 9, "bold"),
        )
        # ── best reference line ────────────────────────────────────────────
        best_val = max(vals)
        best_y = to_cy(best_val)
        best_lbl = (
            f"best {int(best_val)}%"
            if y_axis == "Accuracy"
            else f"best {int(best_val)}"
        )
        c.create_line(ox, best_y, ox + pw, best_y, fill="#22c55e", width=1, dash=(6, 4))
        c.create_text(
            ox + pw - 4,
            best_y - 8,
            text=best_lbl,
            fill="#22c55e",
            anchor="e",
            font=("Roboto", 9, "bold"),
        )

        # ── worst reference line ───────────────────────────────────────────
        worst_val = min(vals)
        worst_y = to_cy(worst_val)
        worst_lbl = (
            f"worst {int(worst_val)}%"
            if y_axis == "Accuracy"
            else f"worst {int(worst_val)}"
        )
        c.create_line(
            ox, worst_y, ox + pw, worst_y, fill="#ef4444", width=1, dash=(6, 4)
        )
        c.create_text(
            ox + pw - 4,
            worst_y - 8,
            text=worst_lbl,
            fill="#ef4444",
            anchor="e",
            font=("Roboto", 9, "bold"),
        )
        # ── data points ───────────────────────────────────────────────
        r = self._GRAPH_PT_R
        for row in rows:
            v = row[1] if y_axis == "WPM" else row[2]
            px = to_cx(row[0])
            py = to_cy(v)
            c.create_oval(
                px - r,
                py - r,
                px + r,
                py + r,
                fill=pt,
                outline="white",
                width=1,
            )
