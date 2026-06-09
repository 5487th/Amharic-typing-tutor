"""
Typing Race — Amharic word-by-word racing with endless random paragraphs.
Requirements: pip install customtkinter
Usage:
    race = TypingRaceMenu(root)
    race.on_back_button_pressed = lambda: print("back pressed")
    race.open_menu(root)

    # Load a custom word bank from a JSON file:
    # race.load_word_bank("/path/to/words.json")
    # JSON format: {"easy": [...], "medium": [...], "hard": [...]}
"""

import customtkinter as ctk
import tkinter as tk
import time
import random
import json
import os

# ── Default word banks ────────────────────────────────────────────────────────
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

NPC_DIFFICULTIES = {
    "Easy": [
        {
            "name": "Turbo",
            "color": "#ef5350",
            "wpm_range": (20, 30),
            "hesitation": 0.20,
        },
        {
            "name": "Blaze",
            "color": "#ff9800",
            "wpm_range": (25, 38),
            "hesitation": 0.15,
        },
        {"name": "Nova", "color": "#ab47bc", "wpm_range": (30, 42), "hesitation": 0.12},
    ],
    "Medium": [
        {
            "name": "Turbo",
            "color": "#ef5350",
            "wpm_range": (38, 52),
            "hesitation": 0.12,
        },
        {
            "name": "Blaze",
            "color": "#ff9800",
            "wpm_range": (50, 65),
            "hesitation": 0.08,
        },
        {"name": "Nova", "color": "#ab47bc", "wpm_range": (60, 78), "hesitation": 0.05},
    ],
    "Hard": [
        {
            "name": "Turbo",
            "color": "#ef5350",
            "wpm_range": (60, 75),
            "hesitation": 0.05,
        },
        {
            "name": "Blaze",
            "color": "#ff9800",
            "wpm_range": (72, 88),
            "hesitation": 0.03,
        },
        {
            "name": "Nova",
            "color": "#ab47bc",
            "wpm_range": (82, 100),
            "hesitation": 0.01,
        },
    ],
}

UI_STRINGS = {
    "english": {
        "title": "TYPING RACE",
        "configure": "Configure your race and hit Start",
        "get_ready": "Get ready …",
        "in_progress": "🏎  Race in progress …",
        "language": "🌐 Language",
        "difficulty": "⚡ Difficulty",
        "start_btn": "▶  Start Race",
        "race_again": "Race Again",
        "wpm": "WPM",
        "acc": "ACC",
        "waiting": "Waiting for race to start …",
        "type_here": "Type here!",
        "get_ready_lbl": "GET READY",
        "go": "GO! 🏁",
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
        "title": "የጽህፈት ሩጫ",
        "configure": "ሩጫዎን ያዋቅሩ እና ጀምር የሚለውን ይጫኑ",
        "get_ready": "ተዘጋጁ …",
        "in_progress": "🏎  ሩጫ በሂደት ላይ …",
        "language": "🌐 ቋንቋ",
        "difficulty": "⚡ ደረጃ",
        "start_btn": "▶  ሩጫ ጀምር",
        "race_again": "እንደገና ሩጫ",
        "wpm": "ቃ/ደ",
        "acc": "ትክ",
        "waiting": "ሩጫ ለመጀመር በመጠባበቅ ላይ …",
        "type_here": "እዚህ ይተይቡ!",
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
            1: "ሁሉንም ረቱ — አስደናቂ ሩጫ!",
            2: "ከፍተኛ ቦታ በጣም ቅርብ ነበሩ! ቀጥሎ ይሞክሩ።",
            3: "ጥሩ ሩጫ — ወደ ፖዲየም መውጣት ይቻላል?",
            4: "NPCዎቹ አሸነፉዎት። ልምምድ ያድርጉ!",
        },
        "your_speed": "የእርስዎ ፍጥነት",
        "words_typed": "የተተየቡ ቃላቶች",
        "you_marker": " ← እርስዎ",
    },
}

# Fixed race word count — paragraph is endless, this seeds the initial batch
RACE_WORD_COUNT = 30

PLAYER_COLOR = "#4fc3f7"
ROAD_COLOR = "#1c1c30"
STRIPE_COLOR = "#2e2e50"
GRASS_COLOR = "#0d1f0d"
TRACK_BG = "#0d0d1a"
CAR_W, CAR_H = 52, 28
TRACK_H = 80
START_X = 90
FINISH_PAD = 70


# ── Base Menu interface ───────────────────────────────────────────────────────
class Menu:
    def open_menu(self, root):
        pass

    def close_menu(self):
        pass


# ── NPC ───────────────────────────────────────────────────────────────────────
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


# ── Main TypingRaceMenu ───────────────────────────────────────────────────────
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

    def __init__(self, root=None, appearance_mode="dark", color_theme="blue"):
        ctk.set_appearance_mode(appearance_mode)
        ctk.set_default_color_theme(color_theme)

        self._root = root
        self._widgets = []  # top-level frames to show/hide
        self._container = None

        # Callbacks
        self.on_back_button_pressed = None  # set by host: lambda: ...

        # State
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
        self._word_banks = dict(DEFAULT_WORD_BANKS)
        self._words = []  # current paragraph word list (grows endlessly)
        self._word_results = []  # True=correct False=wrong per submitted word
        self._current_idx = 0  # which word we're on
        self._words_correct = 0  # words typed correctly
        self._race_words_target = RACE_WORD_COUNT

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
        self._container = ctk.CTkFrame(parent, fg_color=TRACK_BG, corner_radius=0)
        self._container.pack(fill="both", expand=True)

        s = self._get_strings()

        # ── Header ──
        hdr = ctk.CTkFrame(
            self._container, height=52, corner_radius=0, fg_color="#080812"
        )
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        # Back button (left side)
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
            text_color=PLAYER_COLOR,
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

        # Language dropdown — labels are always in their own language
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

        # Difficulty dropdown
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
        canvas_h = TRACK_H * 4 + 30
        cf = ctk.CTkFrame(self._container, fg_color=TRACK_BG, corner_radius=0)
        cf.pack(fill="x", padx=16, pady=(8, 0))
        self._canvas = tk.Canvas(cf, height=canvas_h, bg=TRACK_BG, highlightthickness=0)
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
        self._input_var.trace_add("write", self._on_type)
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

        # Bind space key for word locking — also catches Amharic IME spaces
        self._entry.bind("<space>", self._on_space)
        self._entry.bind("<KeyRelease>", self._on_key_release)

        # ── Bottom bar ──
        bot = ctk.CTkFrame(self._container, fg_color="#080812", height=64)
        bot.pack(fill="x", padx=0, pady=(8, 0))
        bot.pack_propagate(False)

        # Left: WPM / ACC stats
        stats = ctk.CTkFrame(bot, fg_color="transparent")
        stats.pack(side="left", padx=16, pady=8)
        self._wpm_lbl = ctk.CTkLabel(
            stats,
            text=f"{s['wpm']}: —",
            font=ctk.CTkFont("Courier New", 13),
            text_color=PLAYER_COLOR,
        )
        self._wpm_lbl.pack(side="left")
        self._acc_lbl = ctk.CTkLabel(
            stats,
            text=f"{s['acc']}: —",
            font=ctk.CTkFont("Courier New", 13),
            text_color="#66bb6a",
        )
        self._acc_lbl.pack(side="left", padx=16)

        # Centre: countdown lights canvas (hidden until countdown starts)
        self._cd_canvas = tk.Canvas(
            bot, width=120, height=48, bg="#080812", highlightthickness=0
        )
        self._cd_canvas.pack(side="left", expand=True)
        self._cd_items = []  # (oval_id,) per light
        self._cd_step = 0
        self._cd_job = None
        self._cd_active = False
        self._build_countdown_lights()

        # Right: Start button
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
            border_color=PLAYER_COLOR,
        )
        self._ov_title = ctk.CTkLabel(
            self._overlay,
            text="",
            font=ctk.CTkFont("Courier New", 26, weight="bold"),
            text_color=PLAYER_COLOR,
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
        return UI_STRINGS[lang]

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
        # reverse-map display → key
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
        """Update all translatable labels after language change."""
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
        # Difficulty dropdown — translate labels, preserve selected difficulty key
        diff_vals = ["Easy", "Medium", "Hard"]
        diff_display = [s["difficulties"][k] for k in diff_vals]
        cur_key = self._difficulty.get()
        self._diff_menu.configure(values=diff_display)
        self._diff_menu.set(s["difficulties"].get(cur_key, diff_display[1]))

    # ── Public word bank loader (for programmers) ─────────────────────────────
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
            count = RACE_WORD_COUNT
        diff = self._difficulty.get()
        # Check for programmer-supplied difficulty bank first
        diff_bank_key = f"_diff_{diff}"
        if diff_bank_key in self._word_banks:
            bank = self._word_banks[diff_bank_key]
        else:
            bank = self._word_banks.get("amharic", list(self._word_banks.values())[0])
        return random.choices(bank, k=count)

    # ── Race setup ────────────────────────────────────────────────────────────
    def _setup_race(self):
        self._hide_overlay()
        self._stop_race()

        s = self._get_strings()

        # Paragraph is endless; race ends when player types RACE_WORD_COUNT correct words
        self._race_words_target = RACE_WORD_COUNT
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

        diff = self._difficulty.get()
        profiles = NPC_DIFFICULTIES[diff]
        self._npcs = [
            _NPC(p, self._race_words_target, lane=i + 1) for i, p in enumerate(profiles)
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
        # Reset countdown lights
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
            self.on_back_button_pressed()

    # ── Inline countdown lights ───────────────────────────────────────────────
    LIGHT_COLORS_ON = ["#f44336", "#ff9800", "#4caf50"]
    LIGHT_COLORS_OFF = ["#2a0a0a", "#2a1800", "#0a1a0a"]

    def _build_countdown_lights(self):
        c = self._cd_canvas
        c.delete("all")
        self._cd_items = []
        r = 16
        gap = 36
        total_w = 3 * (r * 2) + 2 * (gap - r * 2)
        # Actually space them evenly across 120px
        xs = [22, 60, 98]
        cy = 24
        for i, cx in enumerate(xs):
            bezel = c.create_oval(
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
            # glare
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
        c = self._cd_canvas
        color = self.LIGHT_COLORS_ON[idx] if on else self.LIGHT_COLORS_OFF[idx]
        c.itemconfig(self._cd_items[idx], fill=color)

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
        # Reset lights
        for i in range(3):
            self._set_cd_light(i, False)
        self._cd_canvas.itemconfig(self._cd_go_text, text="")
        self._cd_tick()

    def _cd_tick(self):
        s = self._get_strings()
        # Reset all lights each tick
        for i in range(3):
            self._set_cd_light(i, False)
        self._cd_canvas.itemconfig(self._cd_go_text, text="")

        step = self._cd_step
        if step < 3:
            self._set_cd_light(step, True)
            self._cd_step += 1
            self._cd_job = self._container.after(900, self._cd_tick)
        else:
            # All lights on + GO
            for i in range(3):
                self._set_cd_light(i, True)
            self._cd_canvas.itemconfig(
                self._cd_go_text, text=s["go"].replace(" 🏁", "")
            )
            self._cd_job = self._container.after(700, self._launch_race)

    def _launch_race(self):
        self._cd_active = False
        # Clear the GO text after a short delay
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
            border_color=PLAYER_COLOR,
        )
        self._entry.focus()
        for npc in self._npcs:
            npc.unfreeze()
        self._animate()

    # ── Typing — word-by-word locking ─────────────────────────────────────────
    def _on_space(self, event):
        """Called when player presses space — evaluate current word."""
        if not self._race_active:
            return
        typed = self._input_var.get().strip()
        typed = typed.strip(" \u00a0\u200b\u202f\u2009\u3000\u1361\u1362")
        if not typed:
            self._input_var.set("")
            return "break"
        target = self._words[self._current_idx]

        correct = typed == target
        if correct:
            self._words_correct += 1
        self._word_results.append(correct)

        # Progress = correct words typed / race target
        self._player_prog = min(self._words_correct / self._race_words_target, 1.0)

        self._current_idx += 1
        self._input_var.set("")

        s = self._get_strings()
        elapsed = time.time() - self._start_time
        wpm = int(self._words_correct / (elapsed / 60)) if elapsed > 0 else 0
        acc = round(self._words_correct / max(self._current_idx, 1) * 100, 1)
        self._wpm_lbl.configure(text=f"{s['wpm']}: {wpm}")
        self._acc_lbl.configure(text=f"{s['acc']}: {acc}%")

        # Keep the visible paragraph well ahead — extend if within 10 words of end
        if self._current_idx >= len(self._words) - 10:
            self._words += self._generate_words()

        if self._player_prog >= 1.0 and not self._player_done:
            self._player_done = True
            self._player_finish_time = time.time()
            self._finish_order.append(("YOU", self._player_finish_time))
            self._entry.configure(state="disabled")

        self._render_prompt()
        return "break"

    def _on_key_release(self, event):
        """Catch Amharic IME word separators that don't fire <space>."""
        if not self._race_active:
            return
        val = self._input_var.get()
        # Check if value ends with any space-like / word-separator character
        SEPARATORS = " \u00a0\u200b\u202f\u2009\u3000\u1361\u1362\u1363"
        if val and val[-1] in SEPARATORS:
            self._on_space(None)

    def _on_type(self, *_):
        if not self._race_active:
            return
        self._render_prompt(self._input_var.get())

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

        # Colour tags
        pb.tag_config("done_ok", foreground="#4caf50")  # bright green
        pb.tag_config("done_err", foreground="#f44336")  # bright red
        pb.tag_config("active_ch_ok", foreground="#ffee58")  # yellow, correct char
        pb.tag_config(
            "active_ch_err", foreground="#f44336", background="#2a0a0a"
        )  # red char, dark bg
        pb.tag_config(
            "active_cur", foreground="#ffffff", background="#4fc3f7"
        )  # cursor position
        pb.tag_config(
            "active_rest", foreground="#ffee58", underline=True
        )  # untyped part of active word
        pb.tag_config("upcoming", foreground="#555")
        pb.tag_config("space", foreground="#2a2a3a")

        for i, word in enumerate(self._words):
            if i < self._current_idx:
                # Already submitted
                result = self._word_results[i] if i < len(self._word_results) else True
                tag = "done_ok" if result else "done_err"
                pb.insert("end", word, tag)
                pb.insert("end", " ", "space")
            elif i == self._current_idx:
                # Active word — char-by-char colouring
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

        # Auto-scroll to keep active word visible
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
        return self._canvas_width() - FINISH_PAD

    def _track_len(self):
        return self._finish_x() - START_X

    def _draw_track(self):
        c = self._canvas
        cw = self._canvas_width()
        ch = TRACK_H * 4 + 30
        c.delete("track")
        for lane in range(4):
            y0 = lane * TRACK_H + 15
            y1 = y0 + TRACK_H
            if lane == 0:
                c.create_rectangle(
                    0, 0, cw, y0 + 6, fill=GRASS_COLOR, outline="", tags="track"
                )
            if lane == 3:
                c.create_rectangle(
                    0, y1 - 6, cw, ch, fill=GRASS_COLOR, outline="", tags="track"
                )
            c.create_rectangle(
                0, y0 + 6, cw, y1 - 6, fill=ROAD_COLOR, outline="", tags="track"
            )
            if lane < 3:
                for x in range(0, cw, 28):
                    c.create_rectangle(
                        x,
                        y1 - 8,
                        x + 14,
                        y1 - 6,
                        fill=STRIPE_COLOR,
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
            START_X, 0, START_X, ch, fill="#333", width=2, dash=(6, 4), tags="track"
        )

    def _draw_cars(self):
        c = self._canvas
        s = self._get_strings()
        you = s["you"]

        def car_x(prog):
            return int(START_X + prog * self._track_len())

        def lane_cy(lane):
            return lane * TRACK_H + 15 + TRACK_H // 2

        all_racers = [(you, self._player_prog)] + [
            (n.name, n.progress) for n in self._npcs
        ]
        leader_name = max(all_racers, key=lambda x: x[1])[0]

        self._draw_car(
            c,
            car_x(self._player_prog),
            lane_cy(0),
            PLAYER_COLOR,
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
        hw, hh = CAR_W // 2, CAR_H // 2
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


# ── Standalone runner ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Typing Race")
    root.geometry("920x740")
    root.minsize(700, 600)
    root.configure(fg_color=TRACK_BG)

    game = AmharicTypingRaceMenu(root)
    game.open_menu(root)

    root.mainloop()
