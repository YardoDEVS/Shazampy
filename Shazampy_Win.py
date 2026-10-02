#!/usr/bin/env python3

# Shazampy
# Copyright (c) 2026 Gerardo García Alfaro
# SPDX-License-Identifier: CC-BY-NC-4.0
#
# This source code is made available under the Creative Commons
# Attribution-NonCommercial 4.0 International license (CC BY-NC 4.0).
# You may share and modify it for non-commercial purposes provided that
# appropriate credit is given to the original author, Gerardo García Alfaro,
# a link to the license is provided, and changes are indicated.
# License: https://creativecommons.org/licenses/by-nc/4.0/


import asyncio
import audioop
import ctypes
import json
import os
import queue
import re
import math
import array
import statistics
import subprocess
import tempfile
import threading
import time
import unicodedata
import wave
import webbrowser
from collections import deque
from pathlib import Path

import requests
import pyaudiowpatch as pyaudio
from shazamio import Shazam
import tkinter as tk
from tkinter import font

APP_TITLE = "Shazampy by Gerardo G. A."
PAYPAL_URL = "https://paypal.me/produccionesyardo"

LANGUAGE_ORDER = ["en", "es", "pt", "fr", "it", "de", "ar"]
LANGUAGE_NAMES = {
    "en": "English",
    "es": "Español",
    "pt": "Português",
    "fr": "Français",
    "it": "Italiano",
    "de": "Deutsch",
    "ar": "العربية",
}

TRANSLATIONS = {
    "en": {
        "listening": "Listening continuously…",
        "waiting_song": "Waiting for a song…",
        "searching_lyrics": "Searching for synchronized lyrics…",
        "no_lyrics": "No synchronized lyrics found.",
        "input": "Audio input",
        "buffer": "buffer",
        "shazam": "Shazam",
        "lrc": "LRC",
        "lrc_offset": "LRC offset",
        "language": "Language",
        "donate": "☕ Buy me a coffee: https://paypal.me/produccionesyardo",
        "controls": "←/→ or W/S ±0.25s · ↑/↓ ±1s · A/D language · F audio input · Space restart listening",
        "ffmpeg_missing": "ffmpeg was not found. Install it with: sudo pacman -S ffmpeg",
        "songrec_missing": "ShazamIO is missing. Re-run install_shazampy.py.",
        "audio_error": "The selected audio input could not be opened.",
        "audio_stopped": "Audio capture stopped unexpectedly.",
        "onboard_input": "Onboard input",
        "onboard_output": "Onboard audio output",
        "usb_input": "USB input",
        "usb_output": "USB audio output",
        "bluetooth_input": "Bluetooth input",
        "bluetooth_output": "Bluetooth audio output",
        "hdmi_output": "HDMI/DisplayPort output",
        "other_input": "Audio input",
        "other_output": "Audio output monitor",
    },
    "es": {
        "listening": "Escuchando continuamente…",
        "waiting_song": "Esperando una canción…",
        "searching_lyrics": "Buscando letra sincronizada…",
        "no_lyrics": "No se encontró letra sincronizada.",
        "input": "Entrada de audio",
        "buffer": "búfer",
        "shazam": "Shazam",
        "lrc": "LRC",
        "lrc_offset": "ajuste LRC",
        "language": "Idioma",
        "donate": "☕ Invítame a un café: https://paypal.me/produccionesyardo",
        "controls": "←/→ o W/S ±0,25 s · ↑/↓ ±1 s · A/D idioma · F entrada · Espacio reiniciar escucha",
        "ffmpeg_missing": "No se encontró ffmpeg. Instálalo con: sudo pacman -S ffmpeg",
        "songrec_missing": "Falta ShazamIO. Vuelve a ejecutar install_shazampy.py.",
        "audio_error": "No se pudo abrir la entrada de audio seleccionada.",
        "audio_stopped": "La captura de audio se detuvo inesperadamente.",
        "onboard_input": "Entrada integrada",
        "onboard_output": "Salida de la placa base",
        "usb_input": "Entrada USB",
        "usb_output": "Salida de audio USB",
        "bluetooth_input": "Entrada Bluetooth",
        "bluetooth_output": "Salida de audio Bluetooth",
        "hdmi_output": "Salida HDMI/DisplayPort",
        "other_input": "Entrada de audio",
        "other_output": "Monitor de salida",
    },
    "pt": {
        "listening": "A ouvir continuamente…",
        "waiting_song": "A aguardar uma música…",
        "searching_lyrics": "A procurar letra sincronizada…",
        "no_lyrics": "Não foi encontrada letra sincronizada.",
        "input": "Entrada de áudio",
        "buffer": "buffer",
        "shazam": "Shazam",
        "lrc": "LRC",
        "lrc_offset": "ajuste LRC",
        "language": "Idioma",
        "donate": "☕ Oferece-me um café: https://paypal.me/produccionesyardo",
        "controls": "←/→ ou W/S ±0,25 s · ↑/↓ ±1 s · A/D idioma · F entrada · Espaço reiniciar escuta",
        "ffmpeg_missing": "ffmpeg não foi encontrado. Instale com: sudo pacman -S ffmpeg",
        "songrec_missing": "ShazamIO não está instalado. Execute install_shazampy.py novamente.",
        "audio_error": "Não foi possível abrir a entrada de áudio selecionada.",
        "audio_stopped": "A captura de áudio parou inesperadamente.",
        "onboard_input": "Entrada integrada",
        "onboard_output": "Saída de áudio integrada",
        "usb_input": "Entrada USB",
        "usb_output": "Saída de áudio USB",
        "bluetooth_input": "Entrada Bluetooth",
        "bluetooth_output": "Saída de áudio Bluetooth",
        "hdmi_output": "Saída HDMI/DisplayPort",
        "other_input": "Entrada de áudio",
        "other_output": "Monitor de saída",
    },
    "fr": {
        "listening": "Écoute continue…",
        "waiting_song": "En attente d’un morceau…",
        "searching_lyrics": "Recherche des paroles synchronisées…",
        "no_lyrics": "Aucune parole synchronisée trouvée.",
        "input": "Entrée audio",
        "buffer": "tampon",
        "shazam": "Shazam",
        "lrc": "LRC",
        "lrc_offset": "décalage LRC",
        "language": "Langue",
        "donate": "☕ Offrez-moi un café : https://paypal.me/produccionesyardo",
        "controls": "←/→ ou W/S ±0,25 s · ↑/↓ ±1 s · A/D langue · F entrée · Espace relancer l’écoute",
        "ffmpeg_missing": "ffmpeg est introuvable. Installez-le avec : sudo pacman -S ffmpeg",
        "songrec_missing": "ShazamIO est manquant. Relancez install_shazampy.py.",
        "audio_error": "Impossible d’ouvrir l’entrée audio sélectionnée.",
        "audio_stopped": "La capture audio s’est arrêtée de manière inattendue.",
        "onboard_input": "Entrée intégrée",
        "onboard_output": "Sortie audio intégrée",
        "usb_input": "Entrée USB",
        "usb_output": "Sortie audio USB",
        "bluetooth_input": "Entrée Bluetooth",
        "bluetooth_output": "Sortie audio Bluetooth",
        "hdmi_output": "Sortie HDMI/DisplayPort",
        "other_input": "Entrée audio",
        "other_output": "Moniteur de sortie",
    },
    "it": {
        "listening": "Ascolto continuo…",
        "waiting_song": "In attesa di un brano…",
        "searching_lyrics": "Ricerca del testo sincronizzato…",
        "no_lyrics": "Nessun testo sincronizzato trovato.",
        "input": "Ingresso audio",
        "buffer": "buffer",
        "shazam": "Shazam",
        "lrc": "LRC",
        "lrc_offset": "offset LRC",
        "language": "Lingua",
        "donate": "☕ Offrimi un caffè: https://paypal.me/produccionesyardo",
        "controls": "←/→ o W/S ±0,25 s · ↑/↓ ±1 s · A/D lingua · F ingresso · Spazio riavvia ascolto",
        "ffmpeg_missing": "ffmpeg non è stato trovato. Installalo con: sudo pacman -S ffmpeg",
        "songrec_missing": "ShazamIO non è installato. Esegui di nuovo install_shazampy.py.",
        "audio_error": "Impossibile aprire l’ingresso audio selezionato.",
        "audio_stopped": "L’acquisizione audio si è interrotta inaspettatamente.",
        "onboard_input": "Ingresso integrato",
        "onboard_output": "Uscita audio integrata",
        "usb_input": "Ingresso USB",
        "usb_output": "Uscita audio USB",
        "bluetooth_input": "Ingresso Bluetooth",
        "bluetooth_output": "Uscita audio Bluetooth",
        "hdmi_output": "Uscita HDMI/DisplayPort",
        "other_input": "Ingresso audio",
        "other_output": "Monitor uscita audio",
    },
    "de": {
        "listening": "Kontinuierliches Zuhören…",
        "waiting_song": "Warte auf einen Song…",
        "searching_lyrics": "Suche nach synchronisiertem Liedtext…",
        "no_lyrics": "Kein synchronisierter Liedtext gefunden.",
        "input": "Audioeingang",
        "buffer": "Puffer",
        "shazam": "Shazam",
        "lrc": "LRC",
        "lrc_offset": "LRC-Versatz",
        "language": "Sprache",
        "donate": "☕ Spendier mir einen Kaffee: https://paypal.me/produccionesyardo",
        "controls": "←/→ oder W/S ±0,25 s · ↑/↓ ±1 s · A/D Sprache · F Eingang · Leertaste Hören neu starten",
        "ffmpeg_missing": "ffmpeg wurde nicht gefunden. Installiere es mit: sudo pacman -S ffmpeg",
        "songrec_missing": "ShazamIO fehlt. Führe install_shazampy.py erneut aus.",
        "audio_error": "Der gewählte Audioeingang konnte nicht geöffnet werden.",
        "audio_stopped": "Die Audioaufnahme wurde unerwartet beendet.",
        "onboard_input": "Integrierter Eingang",
        "onboard_output": "Integrierter Audioausgang",
        "usb_input": "USB-Eingang",
        "usb_output": "USB-Audioausgang",
        "bluetooth_input": "Bluetooth-Eingang",
        "bluetooth_output": "Bluetooth-Audioausgang",
        "hdmi_output": "HDMI/DisplayPort-Ausgang",
        "other_input": "Audioeingang",
        "other_output": "Ausgangsmonitor",
    },
    "ar": {
        "listening": "الاستماع المستمر…",
        "waiting_song": "في انتظار أغنية…",
        "searching_lyrics": "جارٍ البحث عن كلمات متزامنة…",
        "no_lyrics": "لم يتم العثور على كلمات متزامنة.",
        "input": "إدخال الصوت",
        "buffer": "المخزن المؤقت",
        "shazam": "Shazam",
        "lrc": "LRC",
        "lrc_offset": "إزاحة LRC",
        "language": "اللغة",
        "donate": "☕ ادعمني بفنجان قهوة: https://paypal.me/produccionesyardo",
        "controls": "←/→ أو W/S ±0.25 ث · ↑/↓ ±1 ث · A/D اللغة · F الإدخال · Space إعادة الاستماع",
        "ffmpeg_missing": "لم يتم العثور على ffmpeg. ثبّته باستخدام: sudo pacman -S ffmpeg",
        "songrec_missing": "مكتبة ShazamIO غير مثبتة. شغّل install_shazampy.py مرة أخرى.",
        "audio_error": "تعذر فتح إدخال الصوت المحدد.",
        "audio_stopped": "توقف التقاط الصوت بشكل غير متوقع.",
        "onboard_input": "إدخال مدمج",
        "onboard_output": "خرج صوت مدمج",
        "usb_input": "إدخال USB",
        "usb_output": "خرج صوت USB",
        "bluetooth_input": "إدخال Bluetooth",
        "bluetooth_output": "خرج صوت Bluetooth",
        "hdmi_output": "خرج HDMI/DisplayPort",
        "other_input": "إدخال صوت",
        "other_output": "مراقب خرج الصوت",
    },
}

LRCLIB_URL = "https://lrclib.net/api/search"
ITUNES_LOOKUP_URL = "https://itunes.apple.com/lookup"
USER_AGENT = "Shazampy/4.7-unicode-donations (Windows x64)"

# Debugging. Spotify/playerctl is only a reference; it is never used to choose sync.
DEBUG_SYNC = True
DEBUG_SPOTIFY = False
DEBUG_LOG_TO_FILE = True
WINDOWS_CONFIG_DIR = Path(os.environ.get("APPDATA", str(Path.home()))) / "Shazampy"
DEBUG_LOG_FILE = WINDOWS_CONFIG_DIR / "debug-sync.log"

# Audio
SAMPLE_RATE = 16000
CHANNELS = 1
SAMPLE_WIDTH = 2
WINDOW_SECONDS = 12.0
RECOGNIZE_EVERY_SECONDS = 3.0
CAPTURE_LATENCY_COMPENSATION = 0.08

# Normal sync
SYNC_HISTORY = 5
SYNC_STRENGTH = 0.70
MAX_SOFT_CORRECTION = 0.60
NORMAL_ERROR_WINDOW = 2.5

# Cluster / branch tracker
CLUSTER_GAP_SECONDS = 0.85
BRANCH_STEP_TOLERANCE = 1.50
INITIAL_MIN_RECORDS = 2
INITIAL_MAX_RECORDS = 3
INITIAL_SCORE_MARGIN = 2.0
RELOCATION_CONFIRMATIONS = 2
RELOCATION_MIN_TOTAL_SUPPORT = 5
RELOCATION_MAX_HYPOTHESES = 8

# Lyrics
DEFAULT_LYRICS_OFFSET = 0.0
LRCLIB_RETRIES = 3
UI_UPDATE_MS = 40

# Spectrum analyzer.  Shazampy already captures mono PCM at 16 kHz, so the
# highest representable frequency is 8 kHz (Nyquist).  The visualizer stays
# slightly below that limit and uses a bank of Goertzel filters so no NumPy or
# other extra Python package is required.
SPECTRUM_BARS = 48
SPECTRUM_MIN_HZ = 60.0
SPECTRUM_MAX_HZ = 7500.0
SPECTRUM_SAMPLES = 1024
SPECTRUM_UPDATE_SECONDS = 0.065
SPECTRUM_HEIGHT = 104
SPECTRUM_LABEL_HEIGHT = 20
SPECTRUM_NOISE_GATE = 0.0012
SPECTRUM_DB_RANGE = 44.0
SPECTRUM_ATTACK = 0.72
SPECTRUM_RELEASE = 0.16

# Frequency groups and their colors.  Each bar inherits the color of the band
# it belongs to.
SPECTRUM_GROUPS = (
    (60.0, 120.0,  "SUB",      "#ff4d5a"),
    (120.0, 250.0, "BASS",     "#ff8a3d"),
    (250.0, 500.0, "LOW MID",  "#ffd43b"),
    (500.0, 2000.0, "MID",     "#56d364"),
    (2000.0, 4000.0, "HIGH MID", "#33c9dc"),
    (4000.0, 7600.0, "TREBLE", "#a875ff"),
)

# Window
BASE_WIDTH = 1080
BASE_HEIGHT = 610
MIN_SCALE = 0.70
MAX_SCALE = 2.30

# Config
CONFIG_DIR = WINDOWS_CONFIG_DIR
OFFSETS_FILE = CONFIG_DIR / "offsets-v2.json"

BYTES_PER_SECOND = SAMPLE_RATE * CHANNELS * SAMPLE_WIDTH
WINDOW_BYTES = int(WINDOW_SECONDS * BYTES_PER_SECOND)
READ_CHUNK_BYTES = int(0.10 * BYTES_PER_SECOND)



def register_bundled_windows_fonts():
    """Load installer-downloaded Noto fonts privately for this process.

    No administrator privileges are required. AddFontResourceExW is available
    on Windows 7/10/11 and makes the fonts visible to Tk for this Shazampy
    process only.
    """
    if os.name != "nt":
        return

    font_dir = Path(__file__).resolve().parent / "fonts"
    if not font_dir.exists():
        return

    FR_PRIVATE = 0x10
    add_font = ctypes.windll.gdi32.AddFontResourceExW
    for pattern in ("*.ttf", "*.otf", "*.ttc"):
        for path in font_dir.rglob(pattern):
            try:
                add_font(str(path), FR_PRIVATE, 0)
            except Exception:
                pass


class ShazamPy:
    def __init__(self):
        self.running = True
        self.events = queue.Queue()
        self.snapshot_queue = queue.Queue(maxsize=1)

        self.language_index = 0
        self.language = LANGUAGE_ORDER[0]
        self.center_message_key = "waiting_song"

        self.buffer_lock = threading.Lock()
        self.audio_buffer = bytearray()
        self.last_audio_monotonic = None

        self.ffmpeg_process = None
        self.songrec_process = None
        self.capture_generation = 0

        self.current_song = None
        self.anchor_position = 0.0
        self.anchor_monotonic = None
        self.error_history = deque(maxlen=SYNC_HISTORY)

        # New branch-tracking state.
        self.active_miss_count = 0
        self.relocation_hypotheses = []

        self.candidate_id = None
        self.candidate_records = []

        self.lyrics = []
        self.current_index = -999
        self.lyrics_generation = 0
        self.lyrics_offset = DEFAULT_LYRICS_OFFSET
        self.saved_offsets = self.load_saved_offsets()
        self.selected_lrc_info = None

        # Spectrum analyzer state.  Frequencies are logarithmically spaced so
        # the low end gets useful visual resolution instead of most bars being
        # wasted in the treble range.
        ratio = SPECTRUM_MAX_HZ / SPECTRUM_MIN_HZ
        self.spectrum_frequencies = [
            SPECTRUM_MIN_HZ * (ratio ** (i / (SPECTRUM_BARS - 1)))
            for i in range(SPECTRUM_BARS)
        ]
        self.spectrum_levels = [0.0] * SPECTRUM_BARS
        self.spectrum_last_update = 0.0
        self.spectrum_window = [
            0.5 - 0.5 * math.cos(2.0 * math.pi * i / (SPECTRUM_SAMPLES - 1))
            for i in range(SPECTRUM_SAMPLES)
        ]

        register_bundled_windows_fonts()
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.attributes("-topmost", True)
        self.root.geometry(f"{BASE_WIDTH}x{BASE_HEIGHT}+380+260")
        self.root.minsize(760, 470)
        self.root.configure(bg="#101010")

        self.icon_font_family = self.detect_icon_font_family()
        self.use_emoji_icons = self.icon_font_family is not None

        self.text_font_families = self.detect_text_font_families()
        self.text_font_sets = {
            "song": self.make_multiscript_font_set(14, "bold"),
            "outer": self.make_multiscript_font_set(14),
            "near": self.make_multiscript_font_set(17),
            "current": self.make_multiscript_font_set(22, "bold"),
            "status": self.make_multiscript_font_set(9),
        }

        # Aliases retained for existing layout code.
        self.song_font = self.text_font_sets["song"]["default"]
        self.outer_font = self.text_font_sets["outer"]["default"]
        self.near_font = self.text_font_sets["near"]["default"]
        self.current_font = self.text_font_sets["current"]["default"]
        self.status_font = self.text_font_sets["status"]["default"]

        self.icon_font = font.Font(
            family=self.icon_font_family if self.use_emoji_icons else "Sans",
            size=18 if self.use_emoji_icons else 10,
            weight="normal" if self.use_emoji_icons else "bold",
        )

        self.audio_inputs = self.discover_audio_inputs()
        self.audio_input_index = self.choose_initial_audio_input()
        self.current_audio_input = self.audio_inputs[self.audio_input_index]

        self.song_label = tk.Label(
            self.root,
            text=self.t("listening"),
            fg="#BDBDBD",
            bg="#101010",
            font=self.song_font,
            justify="center",
        )
        self.song_label.pack(pady=(16, 12))

        self.lyric_labels = []
        for row in range(7):
            if row == 3:
                label = tk.Label(
                    self.root,
                    text="",
                    fg="#FFFFFF",
                    bg="#242424",
                    font=self.current_font,
                    wraplength=990,
                    justify="center",
                    padx=12,
                    pady=7,
                )
            elif row in (2, 4):
                label = tk.Label(
                    self.root,
                    text="",
                    fg="#AFAFAF",
                    bg="#101010",
                    font=self.near_font,
                    wraplength=990,
                    justify="center",
                    padx=8,
                    pady=4,
                )
            else:
                label = tk.Label(
                    self.root,
                    text="",
                    fg="#666666",
                    bg="#101010",
                    font=self.outer_font,
                    wraplength=990,
                    justify="center",
                    padx=8,
                    pady=3,
                )
            label.pack(fill="x", padx=22, pady=1)
            self.lyric_labels.append(label)

        self.set_center_message("waiting_song")

        # Responsive status area.  The input icon lives inside a fixed-size
        # clipped box so color emoji cannot paint over the status text.
        # The status fields are separate labels and are rearranged as the
        # window changes size instead of relying on one very long line.
        self.status_frame = tk.Frame(self.root, bg="#101010")
        self.status_frame.pack(pady=(12, 8), padx=20, fill="x")

        self.input_icon_box = tk.Frame(
            self.status_frame,
            bg="#101010",
            width=58,
            height=58,
        )
        self.input_icon_box.pack(side="left", anchor="n", padx=(0, 12))
        self.input_icon_box.pack_propagate(False)

        self.input_icon_label = tk.Label(
            self.input_icon_box,
            text="",
            fg="#AFAFAF",
            bg="#101010",
            font=self.icon_font,
            bd=0,
            highlightthickness=0,
        )
        self.input_icon_label.place(relx=0.5, rely=0.5, anchor="center")

        self.status_body = tk.Frame(self.status_frame, bg="#101010")
        self.status_body.pack(side="left", fill="x", expand=True)

        self.status_fields_frame = tk.Frame(self.status_body, bg="#101010")
        self.status_fields_frame.pack(fill="x", expand=True)

        def make_status_field(anchor="center", justify="center"):
            return tk.Label(
                self.status_fields_frame,
                text="",
                fg="#707070",
                bg="#101010",
                font=self.status_font,
                justify=justify,
                anchor=anchor,
                padx=7,
                pady=1,
            )

        self.input_status_label = make_status_field("w", "left")
        self.shazam_status_label = make_status_field("center", "center")
        self.lrc_status_label = make_status_field("center", "center")
        self.offset_status_label = make_status_field("center", "center")
        self.language_status_label = make_status_field("center", "center")

        self.controls_label = tk.Label(
            self.status_body,
            text="",
            fg="#606060",
            bg="#101010",
            font=self.status_font,
            justify="center",
            anchor="center",
            padx=6,
            pady=2,
        )
        self.controls_label.pack(fill="x", pady=(4, 0))

        # Donation link: intentionally placed between keyboard help and spectrum.
        self.donation_label = tk.Label(
            self.status_body,
            text="",
            fg="#7CCBFF",
            activeforeground="#B7E4FF",
            bg="#101010",
            font=self.status_font,
            justify="center",
            anchor="center",
            cursor="hand2",
            padx=6,
            pady=2,
        )
        self.donation_label.pack(fill="x", pady=(2, 0))
        self.donation_label.bind(
            "<Button-1>",
            lambda event: webbrowser.open_new_tab(PAYPAL_URL),
        )

        # Full-width frequency spectrum at the very bottom of the window.
        # It is intentionally outside status_frame so neither the audio-input
        # icon nor the responsive status grid can overlap it.
        self.spectrum_canvas = tk.Canvas(
            self.root,
            height=SPECTRUM_HEIGHT,
            bg="#08090b",
            bd=0,
            highlightthickness=0,
        )
        self.spectrum_canvas.pack(side="bottom", fill="x", pady=(4, 0))
        self.spectrum_canvas.bind(
            "<Configure>",
            lambda event: self.draw_spectrum(),
        )

        # Kept as an alias for compatibility with older code paths.
        self.status_label = self.controls_label
        self.status_layout_mode = None
        self.layout_status_fields(BASE_WIDTH, 1.0)

        self.bind_keys()
        self.last_scale = None
        self.last_window_width = BASE_WIDTH
        self.root.bind("<Configure>", self.on_resize)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.start_capture_for_current_input()
        threading.Thread(target=self.snapshot_loop, daemon=True).start()
        threading.Thread(target=self.recognition_loop, daemon=True).start()
        self.root.after(UI_UPDATE_MS, self.update)

    # ---------------- Debug ----------------

    def debug_log(self, *lines):
        if not DEBUG_SYNC:
            return
        text_block = "\n".join(str(line) for line in lines)
        print(text_block, flush=True)
        if DEBUG_LOG_TO_FILE:
            try:
                DEBUG_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
                with DEBUG_LOG_FILE.open("a", encoding="utf-8") as fh:
                    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    fh.write(f"[{stamp}]\n{text_block}\n")
            except Exception:
                pass

    def get_spotify_debug_state(self):
        # Kept for shared debug code. Windows build does not depend on playerctl.
        return None

    # ---------------- Icons / UI text ----------------


    def detect_text_font_families(self):
        """Select installed Noto families for broad multilingual rendering.

        Python strings and LRCLIB data are Unicode already. The remaining part
        is making sure Tk has a font with the requested glyphs. The installer
        installs the Noto family, including CJK and emoji fonts.
        """
        available = {name.casefold(): name for name in font.families(self.root)}

        def first(*names):
            for wanted in names:
                actual = available.get(wanted.casefold())
                if actual:
                    return actual
            return None

        default = first(
            "Noto Sans",
            "DejaVu Sans",
            "Segoe UI",
            "Arial",
            "Liberation Sans",
            "Sans",
        ) or "Sans"

        mapping = {
            "default": default,
            "ja": first("Noto Sans CJK JP", "Noto Sans JP", "Yu Gothic UI", "Meiryo") or default,
            "ko": first("Noto Sans CJK KR", "Noto Sans KR", "Malgun Gothic") or default,
            "han": first("Noto Sans CJK SC", "Noto Sans SC", "Microsoft YaHei UI") or default,
            "bopomofo": first("Noto Sans CJK TC", "Noto Sans TC", "Microsoft JhengHei UI") or default,
            "arabic": first("Noto Sans Arabic", "Noto Naskh Arabic", "Segoe UI") or default,
            "hebrew": first("Noto Sans Hebrew", "Segoe UI") or default,
            "armenian": first("Noto Sans Armenian") or default,
            "bengali": first("Noto Sans Bengali") or default,
            "cherokee": first("Noto Sans Cherokee") or default,
            "devanagari": first("Noto Sans Devanagari") or default,
            "ethiopic": first("Noto Sans Ethiopic") or default,
            "georgian": first("Noto Sans Georgian") or default,
            "gujarati": first("Noto Sans Gujarati") or default,
            "gurmukhi": first("Noto Sans Gurmukhi") or default,
            "khmer": first("Noto Sans Khmer") or default,
            "lao": first("Noto Sans Lao") or default,
            "malayalam": first("Noto Sans Malayalam") or default,
            "myanmar": first("Noto Sans Myanmar") or default,
            "odia": first("Noto Sans Oriya", "Noto Sans Odia") or default,
            "sinhala": first("Noto Sans Sinhala") or default,
            "tamil": first("Noto Sans Tamil") or default,
            "telugu": first("Noto Sans Telugu") or default,
            "thai": first("Noto Sans Thai") or default,
            "tibetan": first("Noto Sans Tibetan") or default,
        }
        return mapping

    @staticmethod
    def text_script_key(text):
        """Best-effort script detector for choosing a suitable Noto family."""
        text = unicodedata.normalize("NFC", str(text or ""))

        # Script-specific characters take precedence over Han ideographs.
        for char in text:
            name = unicodedata.name(char, "")
            if "HANGUL" in name:
                return "ko"
            if "HIRAGANA" in name or "KATAKANA" in name:
                return "ja"
            if "BOPOMOFO" in name:
                return "bopomofo"

        name_map = (
            ("ARABIC", "arabic"),
            ("HEBREW", "hebrew"),
            ("ARMENIAN", "armenian"),
            ("BENGALI", "bengali"),
            ("CHEROKEE", "cherokee"),
            ("DEVANAGARI", "devanagari"),
            ("ETHIOPIC", "ethiopic"),
            ("GEORGIAN", "georgian"),
            ("GUJARATI", "gujarati"),
            ("GURMUKHI", "gurmukhi"),
            ("KHMER", "khmer"),
            ("LAO", "lao"),
            ("MALAYALAM", "malayalam"),
            ("MYANMAR", "myanmar"),
            ("ORIYA", "odia"),
            ("ODIA", "odia"),
            ("SINHALA", "sinhala"),
            ("TAMIL", "tamil"),
            ("TELUGU", "telugu"),
            ("THAI", "thai"),
            ("TIBETAN", "tibetan"),
        )
        for char in text:
            name = unicodedata.name(char, "")
            for token, key in name_map:
                if token in name:
                    return key

        for char in text:
            cp = ord(char)
            name = unicodedata.name(char, "")
            if (
                "CJK UNIFIED IDEOGRAPH" in name
                or "CJK COMPATIBILITY IDEOGRAPH" in name
                or 0x3400 <= cp <= 0x4DBF
                or 0x4E00 <= cp <= 0x9FFF
                or 0x20000 <= cp <= 0x323AF
            ):
                return "han"

        return "default"

    def make_multiscript_font_set(self, size, weight="normal"):
        return {
            key: font.Font(family=family, size=size, weight=weight)
            for key, family in self.text_font_families.items()
        }

    def font_for_text(self, role, text):
        key = self.text_script_key(text)
        role_fonts = self.text_font_sets[role]
        return role_fonts.get(key, role_fonts["default"])

    def set_widget_text(self, widget, role, text):
        normalized = unicodedata.normalize("NFC", str(text or ""))
        widget.config(text=normalized, font=self.font_for_text(role, normalized))
        return normalized

    def resize_multiscript_fonts(self, role, size):
        for font_object in self.text_font_sets[role].values():
            font_object.configure(size=size)

    def detect_icon_font_family(self):
        available = {name.casefold(): name for name in font.families(self.root)}
        for wanted in (
            "Noto Color Emoji",
            "Noto Emoji",
            "Symbola",
            "Segoe UI Emoji",
            "Apple Color Emoji",
        ):
            actual = available.get(wanted.casefold())
            if actual:
                return actual
        return None

    @staticmethod
    def device_icon_data(type_key):
        mapping = {
            "onboard_input": ("🎙️", "[MIC]"),
            "onboard_output": ("🔊", "[PCI]"),
            "usb_input": ("🔌", "[USB]"),
            "usb_output": ("🔌", "[USB]"),
            "bluetooth_input": ("📶", "[BT]"),
            "bluetooth_output": ("📶", "[BT]"),
            "hdmi_output": ("🖥️", "[HDMI]"),
            "other_input": ("🎤", "[IN]"),
            "other_output": ("🔈", "[OUT]"),
        }
        return mapping.get(type_key, ("•", "[AUDIO]"))

    def rendered_input_icon(self, item=None):
        item = item or self.current_audio_input
        emoji, fallback = self.device_icon_data(item["type_key"])
        return emoji if self.use_emoji_icons else fallback

    def t(self, key):
        return TRANSLATIONS[self.language].get(key, key)

    def set_center_message(self, key):
        self.center_message_key = key
        for index, label in enumerate(self.lyric_labels):
            text = self.t(key) if index == 3 else ""
            role = "current" if index == 3 else ("near" if index in (2, 4) else "outer")
            self.set_widget_text(label, role, text)

    def change_language(self, direction):
        self.language_index = (self.language_index + direction) % len(LANGUAGE_ORDER)
        self.language = LANGUAGE_ORDER[self.language_index]
        if self.current_song is None:
            self.set_widget_text(self.song_label, "song", self.t("listening"))
        if not self.lyrics and self.center_message_key:
            self.set_center_message(self.center_message_key)
        self.update_status()

    @staticmethod
    def clean_value(value):
        if value is None:
            return ""
        value = str(value).strip()
        if value.casefold() in {"", "null", "(null)", "none", "(none)", "n/a"}:
            return ""
        return value

    # ---------------- Audio discovery ----------------

    def discover_audio_inputs(self):
        """Enumerate Windows inputs and WASAPI loopback outputs."""
        devices = []
        audio = None
        default_input_index = None
        default_loopback_index = None

        try:
            audio = pyaudio.PyAudio()

            try:
                default_input_index = int(
                    audio.get_default_input_device_info()["index"]
                )
            except Exception:
                pass

            try:
                default_loopback_index = int(
                    audio.get_default_wasapi_loopback()["index"]
                )
            except Exception:
                pass

            for info in audio.get_device_info_generator():
                try:
                    index = int(info["index"])
                    max_inputs = int(info.get("maxInputChannels", 0))
                    is_loopback = bool(info.get("isLoopbackDevice", False))
                    if max_inputs <= 0:
                        continue

                    name = self.clean_value(info.get("name")) or f"Windows audio device {index}"
                    haystack = name.casefold()

                    is_usb = "usb" in haystack
                    is_bluetooth = any(x in haystack for x in ("bluetooth", "bt ", "hands-free"))
                    is_hdmi = any(x in haystack for x in ("hdmi", "displayport", "display audio"))
                    is_onboard = any(
                        x in haystack
                        for x in ("realtek", "high definition audio", "speakers", "microphone array")
                    )
                    is_microphone = (
                        not is_loopback
                        and any(x in haystack for x in ("mic", "microphone", "headset"))
                    )

                    if is_loopback:
                        if is_hdmi:
                            type_key = "hdmi_output"
                        elif is_usb:
                            type_key = "usb_output"
                        elif is_bluetooth:
                            type_key = "bluetooth_output"
                        elif is_onboard:
                            type_key = "onboard_output"
                        else:
                            type_key = "other_output"
                    else:
                        if is_usb:
                            type_key = "usb_input"
                        elif is_bluetooth:
                            type_key = "bluetooth_input"
                        elif is_onboard:
                            type_key = "onboard_input"
                        else:
                            type_key = "other_input"

                    devices.append(
                        {
                            "name": str(index),
                            "device_index": index,
                            "description": name,
                            "type_key": type_key,
                            "monitor": is_loopback,
                            "microphone": is_microphone,
                            "default": (
                                index == default_input_index
                                or (is_loopback and index == default_loopback_index)
                            ),
                            "sample_rate": int(float(info.get("defaultSampleRate", 48000))),
                            "channels": max(1, min(2, max_inputs)),
                        }
                    )
                except Exception:
                    continue
        except Exception as exc:
            self.debug_log(f"Windows audio enumeration error: {exc}")
        finally:
            if audio is not None:
                try:
                    audio.terminate()
                except Exception:
                    pass

        if not devices:
            devices = [
                {
                    "name": "0",
                    "device_index": 0,
                    "description": "Default Windows audio input",
                    "type_key": "other_input",
                    "monitor": False,
                    "microphone": True,
                    "default": True,
                    "sample_rate": 48000,
                    "channels": 1,
                }
            ]

        devices.sort(
            key=lambda device: (
                0 if (device["default"] and not device["monitor"]) else 1,
                0 if not device["monitor"] else 1,
                0 if device["microphone"] else 1,
                device["description"].casefold(),
            )
        )

        print()
        print("========== WINDOWS AUDIO SOURCES ==========")
        for index, device in enumerate(devices):
            default_mark = "*" if device["default"] else " "
            _, fallback = self.device_icon_data(device["type_key"])
            mode = "WASAPI LOOPBACK" if device["monitor"] else "INPUT"
            print(
                f"{default_mark} [{index}] {fallback} [{mode}] "
                f"{device['description']} (device {device['device_index']})"
            )
        print("===========================================")
        print()

        return devices

    def choose_initial_audio_input(self):
        for index, device in enumerate(self.audio_inputs):
            if device["default"] and not device["monitor"]:
                return index
        for index, device in enumerate(self.audio_inputs):
            if device["microphone"] and not device["monitor"]:
                return index
        for index, device in enumerate(self.audio_inputs):
            if not device["monitor"]:
                return index
        return 0

    def audio_input_label(self, item=None):
        item = item or self.current_audio_input
        default_marker = " ★" if item.get("default") else ""
        return f"{self.t(item['type_key'])}{default_marker} · {item['description']}"

    def cycle_audio_input(self):
        current_name = self.current_audio_input["name"]
        refreshed = self.discover_audio_inputs()
        current_index = next(
            (i for i, device in enumerate(refreshed) if device["name"] == current_name),
            -1,
        )
        self.audio_inputs = refreshed
        self.audio_input_index = (current_index + 1) % len(self.audio_inputs)
        self.current_audio_input = self.audio_inputs[self.audio_input_index]
        self.start_capture_for_current_input()

    # ---------------- Restart / capture ----------------

    def restart_listening(self):
        self.debug_log(
            "",
            "========================================",
            "SHAZAMPY: RESTARTING LISTENING SESSION",
            "========================================",
        )
        self.start_capture_for_current_input()

    def reset_tracking_state(self):
        self.current_song = None
        self.anchor_position = 0.0
        self.anchor_monotonic = None
        self.error_history.clear()
        self.active_miss_count = 0
        self.relocation_hypotheses = []
        self.candidate_id = None
        self.candidate_records = []
        self.lyrics = []
        self.current_index = -999
        self.lyrics_offset = DEFAULT_LYRICS_OFFSET
        self.selected_lrc_info = None

    def start_capture_for_current_input(self):
        self.capture_generation += 1
        generation = self.capture_generation
        self.lyrics_generation += 1

        for process in (self.ffmpeg_process, self.songrec_process):
            try:
                if process and process.poll() is None:
                    process.terminate()
            except Exception:
                pass
        self.ffmpeg_process = None
        self.songrec_process = None

        with self.buffer_lock:
            self.audio_buffer.clear()
            self.last_audio_monotonic = None

        self.spectrum_levels = [0.0] * SPECTRUM_BARS
        self.spectrum_last_update = 0.0
        if hasattr(self, "spectrum_canvas"):
            self.draw_spectrum()

        while True:
            try:
                self.snapshot_queue.get_nowait()
            except queue.Empty:
                break

        while True:
            try:
                self.events.get_nowait()
            except queue.Empty:
                break

        self.reset_tracking_state()
        self.set_widget_text(self.song_label, "song", self.t("listening"))
        self.set_center_message("waiting_song")
        self.update_status()

        threading.Thread(
            target=self.capture_loop,
            args=(self.current_audio_input["name"], generation),
            daemon=True,
        ).start()

    def capture_loop(self, source_name, generation):
        """Capture microphones or speaker output through Windows WASAPI.

        PyAudioWPatch exposes loopback copies of output devices as inputs. Data
        is converted to mono 16-bit/16 kHz so the recognition and spectrum
        pipeline remains identical to the Linux build.
        """
        audio = None
        stream = None
        try:
            device = next(
                (
                    item
                    for item in self.audio_inputs
                    if item["name"] == source_name
                ),
                self.current_audio_input,
            )

            device_index = int(device["device_index"])
            native_rate = max(8000, int(device.get("sample_rate", 48000)))
            native_channels = max(1, min(2, int(device.get("channels", 1))))
            frames_per_buffer = max(256, int(native_rate * 0.10))

            audio = pyaudio.PyAudio()
            stream = audio.open(
                format=pyaudio.paInt16,
                channels=native_channels,
                rate=native_rate,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=frames_per_buffer,
            )

            rate_state = None

            while self.running and generation == self.capture_generation:
                try:
                    chunk = stream.read(
                        frames_per_buffer,
                        exception_on_overflow=False,
                    )
                except Exception:
                    if generation == self.capture_generation and self.running:
                        self.events.put(("error_key", "audio_stopped"))
                    return

                if native_channels == 2:
                    mono = audioop.tomono(chunk, SAMPLE_WIDTH, 0.5, 0.5)
                else:
                    mono = chunk

                if native_rate != SAMPLE_RATE:
                    mono, rate_state = audioop.ratecv(
                        mono,
                        SAMPLE_WIDTH,
                        1,
                        native_rate,
                        SAMPLE_RATE,
                        rate_state,
                    )

                now = time.monotonic()
                with self.buffer_lock:
                    if generation != self.capture_generation:
                        return
                    self.audio_buffer.extend(mono)
                    if len(self.audio_buffer) > WINDOW_BYTES:
                        del self.audio_buffer[:-WINDOW_BYTES]
                    self.last_audio_monotonic = now

        except Exception as exc:
            self.debug_log(f"Windows capture error: {exc}")
            if generation == self.capture_generation and self.running:
                self.events.put(("error_key", "audio_error"))
        finally:
            if stream is not None:
                try:
                    stream.stop_stream()
                except Exception:
                    pass
                try:
                    stream.close()
                except Exception:
                    pass
            if audio is not None:
                try:
                    audio.terminate()
                except Exception:
                    pass

    # ---------------- Keys / resize ----------------

    def bind_keys(self):
        self.root.bind("<Escape>", lambda event: self.close())

        for key in ("<Right>", "<KeyPress-w>", "<KeyPress-W>"):
            self.root.bind(key, lambda event: self.adjust_lyrics_offset(+0.25))
        for key in ("<Left>", "<KeyPress-s>", "<KeyPress-S>"):
            self.root.bind(key, lambda event: self.adjust_lyrics_offset(-0.25))

        self.root.bind("<Up>", lambda event: self.adjust_lyrics_offset(+1.0))
        self.root.bind("<Down>", lambda event: self.adjust_lyrics_offset(-1.0))

        for key in ("<KeyPress-a>", "<KeyPress-A>"):
            self.root.bind(key, lambda event: self.change_language(-1))
        for key in ("<KeyPress-d>", "<KeyPress-D>"):
            self.root.bind(key, lambda event: self.change_language(+1))
        for key in ("<KeyPress-f>", "<KeyPress-F>"):
            self.root.bind(key, lambda event: self.cycle_audio_input())

        self.root.bind("<KeyPress-space>", lambda event: self.restart_listening())

    # ---------------- Spectrum analyzer ----------------

    @staticmethod
    def spectrum_group_for_frequency(frequency):
        for low, high, name, color in SPECTRUM_GROUPS:
            if low <= frequency < high:
                return name, color
        return "TREBLE", "#a875ff"

    @staticmethod
    def goertzel_magnitude(samples, frequency):
        """Return the magnitude around one frequency using Goertzel.

        This is deliberately standard-library only.  With 48 bars and a
        1024-sample window it is light enough for the target hardware while
        keeping the recognition audio path completely unchanged.
        """
        omega = 2.0 * math.pi * frequency / SAMPLE_RATE
        coeff = 2.0 * math.cos(omega)
        q1 = 0.0
        q2 = 0.0

        for value in samples:
            q0 = value + coeff * q1 - q2
            q2 = q1
            q1 = q0

        power = q1 * q1 + q2 * q2 - coeff * q1 * q2
        if power <= 0.0:
            return 0.0
        return math.sqrt(power) / len(samples)

    def spectrum_pcm_samples(self):
        """Copy only the newest short PCM window from the rolling buffer."""
        needed_bytes = SPECTRUM_SAMPLES * SAMPLE_WIDTH

        with self.buffer_lock:
            if len(self.audio_buffer) < needed_bytes:
                return None
            pcm = bytes(self.audio_buffer[-needed_bytes:])

        values = array.array("h")
        values.frombytes(pcm)

        # Shazampy runs on Arch/x86 in this project, which is little-endian.
        # Keep this defensive path for other machines.
        import sys
        if sys.byteorder != "little":
            values.byteswap()

        if len(values) < SPECTRUM_SAMPLES:
            return None

        # Remove DC and apply a Hann window before spectral analysis.
        mean = sum(values) / len(values)
        normalized = [
            ((sample - mean) / 32768.0) * self.spectrum_window[i]
            for i, sample in enumerate(values)
        ]
        return normalized

    def update_spectrum(self):
        now = time.monotonic()
        if now - self.spectrum_last_update < SPECTRUM_UPDATE_SECONDS:
            return
        self.spectrum_last_update = now

        samples = self.spectrum_pcm_samples()
        if not samples:
            # Smooth fade to black while the buffer is filling/restarting.
            self.spectrum_levels = [level * 0.82 for level in self.spectrum_levels]
            self.draw_spectrum()
            return

        rms = math.sqrt(sum(sample * sample for sample in samples) / len(samples))

        if rms < SPECTRUM_NOISE_GATE:
            targets = [0.0] * SPECTRUM_BARS
        else:
            db_values = []
            for frequency in self.spectrum_frequencies:
                magnitude = self.goertzel_magnitude(samples, frequency)
                db_values.append(20.0 * math.log10(max(magnitude, 1e-9)))

            # Adaptive reference keeps both the microphone and a clean digital
            # monitor lively without amplifying true silence into a fake show.
            peak_db = max(db_values)
            top_db = max(-24.0, min(-5.0, peak_db + 2.0))
            bottom_db = top_db - SPECTRUM_DB_RANGE
            targets = [
                max(0.0, min(1.0, (db - bottom_db) / SPECTRUM_DB_RANGE))
                for db in db_values
            ]

        smoothed = []
        for old, target in zip(self.spectrum_levels, targets):
            factor = SPECTRUM_ATTACK if target > old else SPECTRUM_RELEASE
            smoothed.append(old + (target - old) * factor)
        self.spectrum_levels = smoothed

        self.draw_spectrum()

    def draw_spectrum(self):
        if not hasattr(self, "spectrum_canvas"):
            return

        canvas = self.spectrum_canvas
        width = max(canvas.winfo_width(), 2)
        height = max(canvas.winfo_height(), SPECTRUM_HEIGHT)
        label_height = min(SPECTRUM_LABEL_HEIGHT, max(14, height // 4))
        graph_bottom = height - label_height - 3
        graph_top = 5
        graph_height = max(10, graph_bottom - graph_top)

        canvas.delete("all")

        # Subtle horizontal guides make the movement easier to read without
        # visually competing with the lyrics.
        for fraction in (0.25, 0.50, 0.75):
            y = graph_bottom - graph_height * fraction
            canvas.create_line(0, y, width, y, fill="#15181d", width=1)

        n = len(self.spectrum_levels)
        slot = width / n
        gap = max(1.0, min(4.0, slot * 0.18))

        for index, level in enumerate(self.spectrum_levels):
            frequency = self.spectrum_frequencies[index]
            _, color = self.spectrum_group_for_frequency(frequency)

            x0 = index * slot + gap / 2.0
            x1 = (index + 1) * slot - gap / 2.0
            bar_height = max(1.0, level * graph_height)
            y0 = graph_bottom - bar_height

            canvas.create_rectangle(
                x0,
                y0,
                x1,
                graph_bottom,
                fill=color,
                outline="",
            )

        # Colored group strip / legend.  On wide windows print the group names;
        # on compact windows the colors remain but labels are omitted to avoid
        # collisions.
        log_min = math.log(SPECTRUM_MIN_HZ)
        log_span = math.log(SPECTRUM_MAX_HZ) - log_min

        for low, high, name, color in SPECTRUM_GROUPS:
            clipped_low = max(low, SPECTRUM_MIN_HZ)
            clipped_high = min(high, SPECTRUM_MAX_HZ)
            if clipped_high <= clipped_low:
                continue

            x0 = width * (math.log(clipped_low) - log_min) / log_span
            x1 = width * (math.log(clipped_high) - log_min) / log_span
            canvas.create_rectangle(
                x0,
                height - 4,
                x1,
                height,
                fill=color,
                outline="",
            )

            if width >= 1000 and (x1 - x0) >= 70:
                if high >= 1000:
                    if low >= 1000:
                        range_text = f"{low/1000:g}–{min(high, SPECTRUM_MAX_HZ)/1000:g} kHz"
                    else:
                        range_text = f"{int(low)} Hz–{min(high, SPECTRUM_MAX_HZ)/1000:g} kHz"
                else:
                    range_text = f"{int(low)}–{int(high)} Hz"

                canvas.create_text(
                    (x0 + x1) / 2.0,
                    height - label_height / 2.0 - 1,
                    text=f"{name}  {range_text}",
                    fill=color,
                    font=("Sans", 8),
                    anchor="center",
                )

        # Thin baseline separating the analyzer from the rest of the UI.
        canvas.create_line(0, 0, width, 0, fill="#20242b", width=1)

    def layout_status_fields(self, width, scale=1.0):
        """Responsive layout for the information below the lyrics.

        The long audio-input description gets the most room.  At smaller
        widths the remaining fields move onto additional rows instead of
        being squeezed under the icon or clipped outside the window.
        """

        labels = (
            self.input_status_label,
            self.shazam_status_label,
            self.lrc_status_label,
            self.offset_status_label,
            self.language_status_label,
        )

        for label in labels:
            label.grid_forget()

        for column in range(5):
            self.status_fields_frame.columnconfigure(column, weight=0, uniform="")

        body_width = max(420, width - int(110 * scale))

        if width >= 1350:
            mode = "wide"
            weights = (6, 1, 1, 1, 1)
            for column, weight in enumerate(weights):
                self.status_fields_frame.columnconfigure(column, weight=weight)

            self.input_status_label.grid(row=0, column=0, sticky="ew", padx=(0, 8))
            self.shazam_status_label.grid(row=0, column=1, sticky="ew")
            self.lrc_status_label.grid(row=0, column=2, sticky="ew")
            self.offset_status_label.grid(row=0, column=3, sticky="ew")
            self.language_status_label.grid(row=0, column=4, sticky="ew")
            self.input_status_label.config(wraplength=max(420, int(body_width * 0.48)))

        elif width >= 900:
            mode = "medium"
            for column in range(4):
                self.status_fields_frame.columnconfigure(column, weight=1)

            self.input_status_label.grid(
                row=0, column=0, columnspan=3, sticky="ew", padx=(0, 8)
            )
            self.language_status_label.grid(row=0, column=3, sticky="ew")
            self.shazam_status_label.grid(row=1, column=0, sticky="ew", pady=(2, 0))
            self.lrc_status_label.grid(row=1, column=1, sticky="ew", pady=(2, 0))
            self.offset_status_label.grid(
                row=1, column=2, columnspan=2, sticky="ew", pady=(2, 0)
            )
            self.input_status_label.config(wraplength=max(420, int(body_width * 0.70)))

        else:
            mode = "compact"
            for column in range(2):
                self.status_fields_frame.columnconfigure(column, weight=1)

            self.input_status_label.grid(
                row=0, column=0, columnspan=2, sticky="ew"
            )
            self.shazam_status_label.grid(row=1, column=0, sticky="ew", pady=(2, 0))
            self.lrc_status_label.grid(row=1, column=1, sticky="ew", pady=(2, 0))
            self.offset_status_label.grid(row=2, column=0, sticky="ew", pady=(2, 0))
            self.language_status_label.grid(row=2, column=1, sticky="ew", pady=(2, 0))
            self.input_status_label.config(wraplength=max(320, body_width - 20))

        self.controls_label.config(wraplength=max(360, body_width - 10))
        self.donation_label.config(wraplength=max(360, body_width - 10))
        self.status_layout_mode = mode

    def on_resize(self, event):
        if event.widget is not self.root:
            return

        width = max(event.width, 1)
        height = max(event.height, 1)
        scale = max(
            MIN_SCALE,
            min(MAX_SCALE, min(width / BASE_WIDTH, height / BASE_HEIGHT)),
        )

        if self.last_scale is None or abs(scale - self.last_scale) >= 0.015:
            self.resize_multiscript_fonts("song", max(10, round(14 * scale)))
            self.resize_multiscript_fonts("outer", max(10, round(14 * scale)))
            self.resize_multiscript_fonts("near", max(11, round(17 * scale)))
            self.resize_multiscript_fonts("current", max(14, round(22 * scale)))

            # The status area also scales, but a modest cap keeps long device
            # names readable instead of turning the bottom area into giant text.
            self.resize_multiscript_fonts(
                "status",
                max(8, min(12, round(9 * scale))),
            )
            self.icon_font.configure(
                size=max(10, min(24, round((18 if self.use_emoji_icons else 10) * scale)))
            )

            icon_box_size = max(48, min(76, round(58 * scale)))
            self.input_icon_box.config(width=icon_box_size, height=icon_box_size)

            spectrum_height = max(82, min(132, round(SPECTRUM_HEIGHT * scale)))
            self.spectrum_canvas.config(height=spectrum_height)
            self.last_scale = scale

        if abs(width - self.last_window_width) >= 10:
            wrap = max(600, width - 90)
            for label in self.lyric_labels:
                label.config(wraplength=wrap)

            self.layout_status_fields(width, scale)
            self.draw_spectrum()
            self.last_window_width = width

    # ---------------- Snapshot / recognition ----------------

    def snapshot_loop(self):
        while self.running:
            generation = self.capture_generation
            with self.buffer_lock:
                ready = (
                    len(self.audio_buffer) >= WINDOW_BYTES
                    and self.last_audio_monotonic is not None
                )
                if ready:
                    pcm = bytes(self.audio_buffer[-WINDOW_BYTES:])
                    sample_end = self.last_audio_monotonic
                else:
                    pcm = None
                    sample_end = None

            if not ready:
                time.sleep(0.1)
                continue

            snapshot = {
                "pcm": pcm,
                "sample_end": sample_end,
                "duration": len(pcm) / BYTES_PER_SECOND,
                "generation": generation,
            }

            try:
                self.snapshot_queue.put_nowait(snapshot)
            except queue.Full:
                try:
                    self.snapshot_queue.get_nowait()
                except queue.Empty:
                    pass
                try:
                    self.snapshot_queue.put_nowait(snapshot)
                except queue.Full:
                    pass

            time.sleep(RECOGNIZE_EVERY_SECONDS)

    @staticmethod
    async def _shazamio_recognize(path):
        shazam = Shazam()
        return await asyncio.wait_for(shazam.recognize(path), timeout=15.0)

    def recognition_loop(self):
        while self.running:
            try:
                snapshot = self.snapshot_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            if snapshot["generation"] != self.capture_generation:
                continue

            path = None
            try:
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                    path = tmp.name

                with wave.open(path, "wb") as wav:
                    wav.setnchannels(CHANNELS)
                    wav.setsampwidth(SAMPLE_WIDTH)
                    wav.setframerate(SAMPLE_RATE)
                    wav.writeframes(snapshot["pcm"])

                data = asyncio.run(self._shazamio_recognize(path))

                if snapshot["generation"] != self.capture_generation:
                    continue

                received = time.monotonic()
                if not isinstance(data, dict) or not data:
                    continue

                recognition = self.parse_recognition(data, snapshot, received)
                if recognition:
                    self.events.put(("recognition", recognition))

            except (asyncio.TimeoutError, TimeoutError):
                continue
            except Exception as exc:
                self.debug_log(f"Windows recognition error: {exc}")
            finally:
                if path:
                    try:
                        Path(path).unlink(missing_ok=True)
                    except Exception:
                        pass

    @staticmethod
    def extract_json(stdout):
        stdout = (stdout or "").strip()
        if not stdout:
            return None
        for line in reversed(stdout.splitlines()):
            try:
                return json.loads(line.strip())
            except (json.JSONDecodeError, TypeError):
                pass
        try:
            return json.loads(stdout)
        except json.JSONDecodeError:
            return None

    # ---------------- Cluster logic ----------------

    @staticmethod
    def _cluster_to_dict(values):
        values = sorted(values)
        # The uppermost match in a tight cluster tracked Spotify most accurately
        # in the APT debug log, while median is used to describe cluster centre.
        return {
            "values": values,
            "center": statistics.median(values),
            "position": values[-1],
            "count": len(values),
            "spread": values[-1] - values[0] if len(values) > 1 else 0.0,
        }

    def cluster_positions(self, positions):
        values = sorted(float(x) for x in positions)
        if not values:
            return []

        groups = [[values[0]]]
        for value in values[1:]:
            if value - groups[-1][-1] <= CLUSTER_GAP_SECONDS:
                groups[-1].append(value)
            else:
                groups.append([value])

        clusters = [self._cluster_to_dict(group) for group in groups]
        clusters.sort(key=lambda c: c["position"])
        return clusters

    @staticmethod
    def cluster_score(cluster):
        # Density matters much more than absolute song position.
        # Tight, repeated matches beat a lonely match far away in the track.
        return cluster["count"] * 2.0 - min(cluster["spread"], 1.0) * 0.5

    def format_clusters(self, clusters):
        return [
            {
                "pos": round(c["position"], 3),
                "center": round(c["center"], 3),
                "n": c["count"],
                "spread": round(c["spread"], 3),
            }
            for c in clusters
        ]

    # ---------------- Parse Shazam ----------------

    def parse_recognition(self, data, snapshot, received):
        track = data.get("track")
        if not track:
            return None

        title = track.get("title")
        artist = track.get("subtitle")
        if not title or not artist:
            return None

        offsets = []
        for match in data.get("matches", []):
            try:
                offset = float(match.get("offset"))
            except (TypeError, ValueError):
                continue
            if offset >= 0:
                offsets.append(offset)

        if not offsets:
            return None

        post_capture = max(0.0, received - snapshot["sample_end"])
        positions = sorted(
            offset
            + snapshot["duration"]
            + post_capture
            + CAPTURE_LATENCY_COMPENSATION
            for offset in offsets
        )
        clusters = self.cluster_positions(positions)

        spotify_debug = self.get_spotify_debug_state()

        if DEBUG_SYNC:
            lines = [
                "",
                "========== SHAZAMPY DEBUG ==========" ,
                f"Input name: {self.current_audio_input['name']}",
                f"Input type: {self.current_audio_input['type_key']}",
                f"Input description: {self.current_audio_input['description']}",
                f"Song: {artist.strip()} - {title.strip()}",
                f"Sample duration: {snapshot['duration']:.3f}s",
                f"Post capture: {post_capture:.3f}s",
                f"Raw Shazam offsets: {[round(value, 3) for value in offsets]}",
                f"Calculated positions @ response: {[round(value, 3) for value in positions]}",
                f"Position clusters: {self.format_clusters(clusters)}",
            ]

            if spotify_debug:
                dt = spotify_debug["sample_time"] - received
                shazam_at_spotify_time = [value + dt for value in positions]
                cluster_positions_at_spotify = [c["position"] + dt for c in clusters]
                lines.extend(
                    [
                        f"Spotify player: {spotify_debug['player']}",
                        f"Spotify status: {spotify_debug['status']}",
                        f"Spotify metadata: {spotify_debug['artist']} - {spotify_debug['title']}",
                        f"Spotify position: {spotify_debug['position']:.3f}s",
                        f"Spotify query dt vs Shazam response: {dt:+.3f}s",
                        f"Shazam positions @ Spotify query time: {[round(value, 3) for value in shazam_at_spotify_time]}",
                        f"Cluster representatives @ Spotify time: {[round(value, 3) for value in cluster_positions_at_spotify]}",
                        f"Cluster differences vs Spotify: {[round(value - spotify_debug['position'], 3) for value in cluster_positions_at_spotify]}",
                    ]
                )
            else:
                lines.append("Spotify reference: unavailable (playerctl/Spotify MPRIS not found)")

            lines.append("====================================")
            self.debug_log(*lines)

        apple_track_id = None
        hub = track.get("hub") or {}
        for action in hub.get("actions") or []:
            if action.get("type") == "applemusicplay" and action.get("id"):
                apple_track_id = str(action["id"])
                break

        return {
            "artist": artist.strip(),
            "title": title.strip(),
            "isrc": str(track.get("isrc") or ""),
            "track_key": str(track.get("key") or ""),
            "apple_track_id": apple_track_id,
            "received": received,
            "sample_duration": snapshot["duration"],
            "post_capture": post_capture,
            "offsets": sorted(round(value, 3) for value in offsets),
            "positions": positions,
            "clusters": clusters,
            "spotify_debug": spotify_debug,
        }

    # ---------------- Song identity / clock ----------------

    @staticmethod
    def normalize(text):
        return re.sub(r"\s+", " ", (text or "").casefold()).strip()

    def song_id(self, song):
        if song.get("isrc"):
            return ("isrc", song["isrc"])
        if song.get("track_key"):
            return ("shazam", song["track_key"])
        return (
            "text",
            self.normalize(song["artist"]),
            self.normalize(song["title"]),
        )

    def storage_key(self, song):
        return "|".join(str(value) for value in self.song_id(song))

    def position_at(self, instant):
        if self.anchor_monotonic is None:
            return 0.0
        return self.anchor_position + (instant - self.anchor_monotonic)

    def current_position(self):
        return self.position_at(time.monotonic())

    def current_lyrics_position(self):
        return self.current_position() + self.lyrics_offset

    # ---------------- Initial branch selection ----------------

    def find_candidate_path(self, records):
        if not records:
            return None

        first_clusters = records[0].get("clusters") or self.cluster_positions(records[0]["positions"])
        paths = []
        for cluster in first_clusters:
            paths.append(
                {
                    "position": cluster["position"],
                    "score": self.cluster_score(cluster),
                    "support": cluster["count"],
                    "positions": [cluster["position"]],
                }
            )

        for index in range(1, len(records)):
            dt = records[index]["received"] - records[index - 1]["received"]
            clusters = records[index].get("clusters") or self.cluster_positions(records[index]["positions"])
            new_paths = []

            for path in paths:
                expected = path["position"] + dt
                for cluster in clusters:
                    error = abs(cluster["position"] - expected)
                    if error <= BRANCH_STEP_TOLERANCE:
                        new_paths.append(
                            {
                                "position": cluster["position"],
                                "score": path["score"] + self.cluster_score(cluster) - error,
                                "support": path["support"] + cluster["count"],
                                "positions": path["positions"] + [cluster["position"]],
                            }
                        )

            paths = new_paths
            if not paths:
                return None

        paths.sort(key=lambda p: (p["score"], p["support"]), reverse=True)
        best = paths[0]
        second_score = paths[1]["score"] if len(paths) > 1 else float("-inf")
        margin = best["score"] - second_score if len(paths) > 1 else float("inf")

        if DEBUG_SYNC:
            self.debug_log(
                "",
                "========== INITIAL BRANCH DEBUG =========",
                f"Records: {len(records)}",
                f"Best path: {[round(x, 3) for x in best['positions']]}",
                f"Best support: {best['support']}",
                f"Best score: {best['score']:.3f}",
                f"Score margin: {margin if margin != float('inf') else 'inf'}",
                "Top candidates: "
                + str(
                    [
                        {
                            "path": [round(x, 3) for x in p["positions"]],
                            "support": p["support"],
                            "score": round(p["score"], 3),
                        }
                        for p in paths[:5]
                    ]
                ),
                "=========================================",
            )

        return {
            "song": records[-1],
            "position": best["position"],
            "score": best["score"],
            "support": best["support"],
            "margin": margin,
        }

    def handle_recognition(self, song):
        if self.current_song is None:
            self.add_song_candidate(song)
            return

        if self.song_id(song) == self.song_id(self.current_song):
            self.candidate_id = None
            self.candidate_records = []
            self.apply_position_measurement(song)
        else:
            self.add_song_candidate(song)

    def add_song_candidate(self, song):
        sid = self.song_id(song)
        if sid != self.candidate_id:
            self.candidate_id = sid
            self.candidate_records = []

        self.candidate_records.append(song)
        self.candidate_records = self.candidate_records[-INITIAL_MAX_RECORDS:]

        if len(self.candidate_records) < INITIAL_MIN_RECORDS:
            return

        result = self.find_candidate_path(self.candidate_records)
        if not result:
            # Keep the newest record so a fresh coherent trajectory can start.
            if len(self.candidate_records) >= INITIAL_MAX_RECORDS:
                self.candidate_records = self.candidate_records[-1:]
            return

        if (
            len(self.candidate_records) < INITIAL_MAX_RECORDS
            and result["margin"] < INITIAL_SCORE_MARGIN
        ):
            # Ambiguous intro/refrain: wait one more recognition instead of
            # choosing the largest song position.
            return

        self.activate_song(result["song"], result["position"])
        self.candidate_id = None
        self.candidate_records = []

    # ---------------- Relocation / same-song seek tracker ----------------

    def clear_relocation_tracker(self):
        self.active_miss_count = 0
        self.relocation_hypotheses = []

    def update_relocation_hypotheses(self, clusters, received):
        previous = self.relocation_hypotheses
        updated = []

        for cluster in clusters:
            best_prev = None
            best_error = None

            for hypothesis in previous:
                dt = received - hypothesis["received"]
                predicted = hypothesis["position"] + dt
                error = abs(cluster["position"] - predicted)
                if error <= BRANCH_STEP_TOLERANCE and (
                    best_error is None or error < best_error
                ):
                    best_prev = hypothesis
                    best_error = error

            if best_prev is None:
                updated.append(
                    {
                        "position": cluster["position"],
                        "received": received,
                        "hits": 1,
                        "support": cluster["count"],
                        "score": self.cluster_score(cluster),
                        "last_count": cluster["count"],
                        "path": [cluster["position"]],
                    }
                )
            else:
                updated.append(
                    {
                        "position": cluster["position"],
                        "received": received,
                        "hits": best_prev["hits"] + 1,
                        "support": best_prev["support"] + cluster["count"],
                        "score": best_prev["score"]
                        + self.cluster_score(cluster)
                        - best_error,
                        "last_count": cluster["count"],
                        "path": (best_prev["path"] + [cluster["position"]])[-4:],
                    }
                )

        # De-duplicate hypotheses ending at practically the same place.
        updated.sort(key=lambda h: (h["score"], h["support"], h["hits"]), reverse=True)
        deduped = []
        for hypothesis in updated:
            if any(abs(hypothesis["position"] - kept["position"]) < 0.5 for kept in deduped):
                continue
            deduped.append(hypothesis)
            if len(deduped) >= RELOCATION_MAX_HYPOTHESES:
                break

        self.relocation_hypotheses = deduped
        return deduped[0] if deduped else None

    def relocate_to_hypothesis(self, hypothesis, song):
        old_position = self.position_at(song["received"])
        self.anchor_position = hypothesis["position"]
        self.anchor_monotonic = song["received"]
        self.error_history.clear()
        self.clear_relocation_tracker()

        self.debug_log(
            "",
            "========== AUTOMATIC RELOCATION =========",
            f"Song: {song['artist']} - {song['title']}",
            f"Old predicted position: {old_position:.3f}s",
            f"New position: {hypothesis['position']:.3f}s",
            f"Hypothesis hits: {hypothesis['hits']}",
            f"Hypothesis support: {hypothesis['support']}",
            f"Hypothesis path: {[round(x, 3) for x in hypothesis['path']]}",
            "Reason: coherent remote branch after active branch disappeared",
            "==========================================",
        )

    def apply_position_measurement(self, song):
        expected = self.position_at(song["received"])
        clusters = song.get("clusters") or self.cluster_positions(song["positions"])
        if not clusters:
            return

        nearest = min(clusters, key=lambda c: abs(c["position"] - expected))
        error = nearest["position"] - expected

        if DEBUG_SYNC:
            lines = [
                "",
                "========== POSITION DEBUG =========",
                f"Song: {song['artist']} - {song['title']}",
                f"Expected local: {expected:.3f}s",
                f"Clusters: {self.format_clusters(clusters)}",
                f"Nearest cluster: {nearest['position']:.3f}s (n={nearest['count']})",
                f"Error vs local: {error:+.3f}s",
            ]
            spotify = song.get("spotify_debug")
            if spotify:
                dt = spotify["sample_time"] - song["received"]
                nearest_at_spotify = nearest["position"] + dt
                local_at_spotify = expected + dt
                lines.extend(
                    [
                        f"Spotify position: {spotify['position']:.3f}s",
                        f"Nearest cluster @ Spotify query: {nearest_at_spotify:.3f}s",
                        f"Local @ Spotify query: {local_at_spotify:.3f}s",
                        f"Nearest cluster vs Spotify: {nearest_at_spotify - spotify['position']:+.3f}s",
                        f"Local vs Spotify: {local_at_spotify - spotify['position']:+.3f}s",
                    ]
                )
            lines.append("===================================")
            self.debug_log(*lines)

        # Normal tracking: if the active branch is still present, follow it.
        if abs(error) <= NORMAL_ERROR_WINDOW:
            self.clear_relocation_tracker()
            self.error_history.append(error)
            filtered = statistics.median(self.error_history)
            correction = max(
                -MAX_SOFT_CORRECTION,
                min(MAX_SOFT_CORRECTION, filtered * SYNC_STRENGTH),
            )
            self.anchor_position = expected + correction
            self.anchor_monotonic = song["received"]
            return

        # Active branch has disappeared. Build trajectories from every cluster,
        # including branches hundreds of seconds away. No fixed 20-second cap.
        self.active_miss_count += 1
        best = self.update_relocation_hypotheses(clusters, song["received"])

        if DEBUG_SYNC:
            self.debug_log(
                "Relocation miss count: " + str(self.active_miss_count),
                "Relocation hypotheses: "
                + str(
                    [
                        {
                            "pos": round(h["position"], 3),
                            "hits": h["hits"],
                            "support": h["support"],
                            "score": round(h["score"], 3),
                            "path": [round(x, 3) for x in h["path"]],
                        }
                        for h in self.relocation_hypotheses[:5]
                    ]
                ),
            )

        if (
            best
            and best["hits"] >= RELOCATION_CONFIRMATIONS
            and best["support"] >= RELOCATION_MIN_TOTAL_SUPPORT
        ):
            self.relocate_to_hypothesis(best, song)

    # ---------------- Activate song ----------------

    def activate_song(self, song, selected_position):
        self.current_song = song
        self.anchor_position = selected_position
        self.anchor_monotonic = song["received"]
        self.error_history.clear()
        self.clear_relocation_tracker()

        self.lyrics_offset = float(
            self.saved_offsets.get(self.storage_key(song), DEFAULT_LYRICS_OFFSET)
        )

        self.set_widget_text(
            self.song_label,
            "song",
            f"{song['artist']} — {song['title']}",
        )
        self.lyrics = []
        self.current_index = -999
        self.set_center_message("searching_lyrics")

        self.debug_log(
            "",
            "========== SONG ACTIVATED =========",
            f"Song: {song['artist']} - {song['title']}",
            f"Initial tracked position: {selected_position:.3f}s",
            "====================================",
        )

        self.lyrics_generation += 1
        generation = self.lyrics_generation
        threading.Thread(
            target=self.lyrics_worker,
            args=(song, generation),
            daemon=True,
        ).start()

    # ---------------- Lyrics ----------------

    def get_reference_duration(self, song):
        apple_id = song.get("apple_track_id")
        if not apple_id:
            return None
        try:
            response = requests.get(
                ITUNES_LOOKUP_URL,
                params={"id": apple_id, "country": "ES"},
                headers={"User-Agent": USER_AGENT},
                timeout=8,
            )
            response.raise_for_status()
            for result in response.json().get("results", []):
                duration_ms = result.get("trackTimeMillis")
                if duration_ms:
                    return float(duration_ms) / 1000.0
        except Exception:
            pass
        return None

    def lyrics_worker(self, song, generation):
        duration = self.get_reference_duration(song)
        lyrics, info = self.search_lyrics(song["artist"], song["title"], duration)
        self.events.put(
            (
                "lyrics",
                {
                    "generation": generation,
                    "lyrics": lyrics,
                    "info": info,
                },
            )
        )

    def search_lyrics(self, artist, title, target_duration):
        params = {"track_name": title, "artist_name": artist}
        for attempt in range(1, LRCLIB_RETRIES + 1):
            try:
                response = requests.get(
                    LRCLIB_URL,
                    params=params,
                    headers={"User-Agent": USER_AGENT},
                    timeout=10,
                )
                if response.status_code in (429, 500, 502, 503, 504):
                    raise requests.RequestException(f"HTTP {response.status_code}")
                response.raise_for_status()

                wanted_title = self.normalize(title)
                wanted_artist = self.normalize(artist)
                candidates = []

                for result in response.json():
                    synced = result.get("syncedLyrics")
                    if not synced:
                        continue
                    parsed = self.parse_lrc(synced)
                    if not parsed:
                        continue

                    score = 0.0
                    if self.normalize(result.get("trackName", "")) == wanted_title:
                        score += 100
                    if self.normalize(result.get("artistName", "")) == wanted_artist:
                        score += 100

                    try:
                        duration = float(result.get("duration"))
                    except (TypeError, ValueError):
                        duration = None

                    if target_duration is not None and duration is not None:
                        difference = abs(duration - target_duration)
                        score += max(0.0, 80.0 - difference * 4.0)
                        if difference > 20:
                            score -= 100

                    candidates.append((score, parsed, result))

                if not candidates:
                    return None, None

                candidates.sort(key=lambda item: item[0], reverse=True)
                return candidates[0][1], candidates[0][2]

            except Exception:
                if attempt < LRCLIB_RETRIES:
                    time.sleep(attempt * 2)

        return None, None

    @staticmethod
    def parse_lrc(lrc):
        pattern = re.compile(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)")
        lines = []
        for raw in lrc.splitlines():
            match = pattern.match(raw.strip())
            if not match:
                continue
            lines.append(
                (
                    int(match.group(1)) * 60 + float(match.group(2)),
                    unicodedata.normalize("NFC", match.group(3).strip()),
                )
            )
        lines.sort(key=lambda item: item[0])
        return lines

    # ---------------- Saved offsets ----------------

    def load_saved_offsets(self):
        try:
            if OFFSETS_FILE.exists():
                data = json.loads(OFFSETS_FILE.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    return data
        except Exception:
            pass
        return {}

    def save_offsets(self):
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            OFFSETS_FILE.write_text(
                json.dumps(self.saved_offsets, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception:
            pass

    def adjust_lyrics_offset(self, delta):
        self.lyrics_offset += delta
        self.current_index = -999
        if self.current_song:
            self.saved_offsets[self.storage_key(self.current_song)] = round(
                self.lyrics_offset, 3
            )
            self.save_offsets()

    # ---------------- Display ----------------

    def update_lyrics_display(self):
        if not self.lyrics:
            return

        position = self.current_lyrics_position()
        index = -1
        for i, (timestamp, _) in enumerate(self.lyrics):
            if timestamp <= position:
                index = i
            else:
                break

        if index == self.current_index:
            return
        self.current_index = index

        for row in range(7):
            lyric_index = index + row - 3
            text = ""
            if 0 <= lyric_index < len(self.lyrics):
                text = self.lyrics[lyric_index][1] or "♪"
            if row == 3:
                text = f"▶  {text}  ◀" if text else "♪"
            role = "current" if row == 3 else ("near" if row in (2, 4) else "outer")
            self.set_widget_text(self.lyric_labels[row], role, text)

    def update_status(self):
        language_name = LANGUAGE_NAMES[self.language]
        input_label = self.audio_input_label()

        self.input_icon_label.config(text=self.rendered_input_icon())
        self.set_widget_text(
            self.input_status_label,
            "status",
            f"{self.t('input')}: {input_label}",
        )
        self.set_widget_text(
            self.language_status_label,
            "status",
            f"{self.t('language')}: {language_name}",
        )
        self.set_widget_text(self.controls_label, "status", self.t("controls"))
        self.set_widget_text(self.donation_label, "status", self.t("donate"))

        if self.anchor_monotonic is not None:
            self.set_widget_text(
                self.shazam_status_label,
                "status",
                f"{self.t('shazam')} {self.current_position():.2f}s",
            )
            self.set_widget_text(
                self.lrc_status_label,
                "status",
                f"{self.t('lrc')} {self.current_lyrics_position():.2f}s",
            )
            self.set_widget_text(
                self.offset_status_label,
                "status",
                f"{self.t('lrc_offset')} {self.lyrics_offset:+.2f}s",
            )
        else:
            with self.buffer_lock:
                buffered = len(self.audio_buffer) / BYTES_PER_SECOND

            self.set_widget_text(
                self.shazam_status_label,
                "status",
                (
                    f"{self.t('buffer')} "
                    f"{min(buffered, WINDOW_SECONDS):.1f}/{WINDOW_SECONDS:.0f}s"
                ),
            )
            self.set_widget_text(self.lrc_status_label, "status", "")
            self.set_widget_text(self.offset_status_label, "status", "")

        # Ensure the correct responsive arrangement is already active even
        # before the first Configure event reaches Tk.
        if self.status_layout_mode is None:
            self.layout_status_fields(self.root.winfo_width() or BASE_WIDTH, 1.0)

    def update(self):
        while True:
            try:
                event_type, data = self.events.get_nowait()
            except queue.Empty:
                break

            if event_type == "recognition":
                self.handle_recognition(data)
            elif event_type == "lyrics":
                if data["generation"] != self.lyrics_generation:
                    continue
                if data["lyrics"]:
                    self.lyrics = data["lyrics"]
                    self.selected_lrc_info = data.get("info")
                    self.current_index = -999
                    self.center_message_key = None
                else:
                    self.lyrics = []
                    self.set_center_message("no_lyrics")
            elif event_type == "error_key":
                self.lyrics = []
                self.set_center_message(data)

        self.update_lyrics_display()
        self.update_status()
        self.update_spectrum()
        if self.running:
            self.root.after(UI_UPDATE_MS, self.update)

    def close(self):
        self.running = False
        self.capture_generation += 1
        self.lyrics_generation += 1
        for process in (self.songrec_process, self.ffmpeg_process):
            try:
                if process and process.poll() is None:
                    process.terminate()
            except Exception:
                pass
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    ShazamPy().run()
