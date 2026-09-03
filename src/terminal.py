"""
PIXELTOWN - This is the PIXELTOWN's terminal, in its early developement.
Copyright (C) 2026  Raúl Salas Sahuquillo

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import json
import os
import sys
import hashlib
import socket
import subprocess
import threading
import webbrowser
import tkinter as tk
from tkinter import messagebox
from localization import load_language, _

# Colour palette
BG_DARK      = "#0f0f1a"
BG_CARD      = "#1a1a2e"
BG_INPUT     = "#16213e"
FG_TEXT       = "#e0e0e0"
FG_DIM        = "#8888aa"
FG_ACCENT     = "#00d4ff"
FG_ACCENT_HVR = "#66e8ff"
BTN_PRIMARY   = "#0a84ff"
BTN_PRIMARY_H = "#339dff"
BTN_DANGER    = "#ff4757"
BTN_DANGER_H  = "#ff6b7a"
BTN_SUCCESS   = "#2ed573"
BTN_SUCCESS_H = "#5af09a"
BTN_GUEST     = "#a55eea"
BTN_GUEST_H   = "#c28df0"
BORDER_COLOR  = "#2a2a4a"

PIXELTOWN_BANNER = (
    "██████╗ ██╗██╗  ██╗███████╗██╗  ████████╗ ██████╗ ██╗    ██╗███╗   ██╗\n"
    "██╔══██╗██║╚██╗██╔╝██╔════╝██║  ╚══██╔══╝██╔═══██╗██║    ██║████╗  ██║\n"
    "██████╔╝██║ ╚███╔╝ █████╗  ██║     ██║   ██║   ██║██║ █╗ ██║██╔██╗ ██║\n"
    "██╔═══╝ ██║ ██╔██╗ ██╔══╝  ██║     ██║   ██║   ██║██║███╗██║██║╚██╗██║\n"
    "██║     ██║██╔╝ ██╗███████╗███████╗██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║\n"
    "╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝"
)

# Helpers (unchanged logic)

def get_save_dir():
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_path = os.path.join(base, "saves")
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    return save_path

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def load_accounts():
    save_dir = get_save_dir()
    accounts_file = os.path.join(save_dir, "accounts.json")
    if not os.path.exists(accounts_file):
        return {}
    try:
        with open(accounts_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading accounts: {e}")
        return {}

def save_accounts(accounts):
    save_dir = get_save_dir()
    accounts_file = os.path.join(save_dir, "accounts.json")
    try:
        with open(accounts_file, "w", encoding="utf-8") as f:
            json.dump(accounts, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving accounts: {e}")
def find_available_port(preferred_port=8000, max_tries=50):
    """Find the next available localhost port starting from preferred_port."""
    for p in range(preferred_port, preferred_port + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', p))
                return p
            except OSError:
                continue
    return preferred_port


# Resolve asset path 
def _asset_path(*parts):
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "assets", *parts)


# Reusable widget helpers 
def _make_entry(parent, *, show=None, placeholder=""):
    """Create a styled Entry with an optional placeholder."""
    var = tk.StringVar()
    entry = tk.Entry(
        parent,
        textvariable=var,
        font=("Consolas", 13),
        bg=BG_INPUT,
        fg=FG_TEXT,
        insertbackground=FG_ACCENT,
        relief="flat",
        highlightthickness=1,
        highlightcolor=FG_ACCENT,
        highlightbackground=BORDER_COLOR,
        show=show,
    )
    # Placeholder behaviour
    if placeholder:
        _ph_fg = FG_DIM
        _normal_fg = FG_TEXT

        def _on_focus_in(_e):
            if var.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=_normal_fg)
                if show:
                    entry.config(show=show)

        def _on_focus_out(_e):
            if not var.get():
                entry.insert(0, placeholder)
                entry.config(fg=_ph_fg, show="")

        entry.insert(0, placeholder)
        entry.config(fg=_ph_fg, show="")
        entry.bind("<FocusIn>", _on_focus_in)
        entry.bind("<FocusOut>", _on_focus_out)

    return entry, var


def _make_button(parent, text, command, bg=BTN_PRIMARY, hover=BTN_PRIMARY_H,
                 fg="black", width=22, font_size=12, pady=8):
    """Create a flat button with hover colour change."""
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", font_size, "bold"),
        bg=bg,
        fg=fg,
        activebackground=hover,
        activeforeground=fg,
        relief="flat",
        cursor="hand2",
        width=width,
        pady=pady,
        bd=0,
    )
    btn.bind("<Enter>", lambda _e: btn.config(bg=hover))
    btn.bind("<Leave>", lambda _e: btn.config(bg=bg))
    return btn

#  Main Terminal Application
class TerminalApp:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PIXELTOWN — Terminal")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)

        # Centre the window
        win_w, win_h = 700, 600
        sx = self.root.winfo_screenwidth() // 2 - win_w // 2
        sy = self.root.winfo_screenheight() // 2 - win_h // 2
        self.root.geometry(f"{win_w}x{win_h}+{sx}+{sy}")

        # Clean shutdown on close
        self.root.protocol("WM_DELETE_WINDOW", self._on_window_close)

        # Try to set the window icon
        try:
            icon_path = _asset_path("images", "pixeltown_logo.png")
            icon = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(True, icon)
        except Exception:
            pass

        self.accounts = load_accounts()
        self.logged_in_user = None  # will be set after auth

        # Pygbag web server management state
        self.pygbag_proc = None
        self.pygbag_thread = None
        self.web_port = 8000
        self.web_url = f"http://localhost:{self.web_port}"
        self.web_status_label = None
        self.web_log_text = None
        self._browser_opened = False

        # Container frame (for screen-swapping)
        self.container = tk.Frame(self.root, bg=BG_DARK)
        self.container.pack(fill="both", expand=True)

        self.selected_language = "es"

        # Start on the language-selection screen (Step 1: Language)
        self._show_language_screen()

    # Initial Language Selection (Step 1)
    def _show_language_screen(self):
        self._clear()

        # Banner
        banner_lbl = tk.Label(
            self.container,
            text=PIXELTOWN_BANNER,
            font=("Courier", 7, "bold"),
            fg=FG_ACCENT,
            bg=BG_DARK,
            justify="left",
        )
        banner_lbl.pack(pady=(20, 5))

        subtitle = tk.Label(
            self.container,
            text="PIXELTOWN OFFICIAL LAUNCHER",
            font=("Segoe UI", 14, "bold"),
            fg=FG_TEXT,
            bg=BG_DARK,
        )
        subtitle.pack(pady=(0, 3))

        welcome = tk.Label(
            self.container,
            text="Welcome to PIXELTOWN! / ¡Bienvenido a PIXELTOWN!",
            font=("Segoe UI", 11),
            fg=FG_DIM,
            bg=BG_DARK,
        )
        welcome.pack(pady=(0, 15))

        # Separator
        sep = tk.Frame(self.container, bg=BORDER_COLOR, height=1)
        sep.pack(fill="x", padx=60, pady=5)

        # Card container for language options
        card = tk.Frame(self.container, bg=BG_CARD, padx=40, pady=25,
                        highlightthickness=1, highlightbackground=BORDER_COLOR)
        card.pack(pady=15)

        lang_label = tk.Label(
            card,
            text="Selecciona tu idioma / Select your language",
            font=("Segoe UI", 12, "bold"),
            fg=FG_TEXT,
            bg=BG_CARD,
        )
        lang_label.pack(pady=(0, 15))

        btn_frame = tk.Frame(card, bg=BG_CARD)
        btn_frame.pack(pady=5)

        es_button = _make_button(
            btn_frame, "🇪🇸  Español", lambda: self._select_language("es"),
            bg="#e67e22", hover="#f0932b", width=16, font_size=12, pady=8,
        )
        es_button.pack(side="left", padx=10)

        en_button = _make_button(
            btn_frame, "🇬🇧  English", lambda: self._select_language("en"),
            bg="#3498db", hover="#5dade2", width=16, font_size=12, pady=8,
        )
        en_button.pack(side="left", padx=10)

        exit_btn = _make_button(
            card, "❌  Salir / Exit",
            self._exit,
            bg=BTN_DANGER, hover=BTN_DANGER_H, width=34, font_size=10, pady=6,
        )
        exit_btn.pack(pady=(20, 0))

        # Footer
        footer = tk.Label(
            self.container,
            text="© 2026 Raúl Salas Sahuquillo",
            font=("Segoe UI", 9),
            fg=FG_DIM,
            bg=BG_DARK,
        )
        footer.pack(side="bottom", pady=10)

    def _select_language(self, code):
        self.selected_language = code
        load_language(code)
        self._show_mode_selection_screen()

    # Platform / Mode Selection (Step 2)
    def _show_mode_selection_screen(self):
        self._clear()
        is_en = (self.selected_language == "en")

        # Banner
        banner_lbl = tk.Label(
            self.container,
            text=PIXELTOWN_BANNER,
            font=("Courier", 7, "bold"),
            fg=FG_ACCENT,
            bg=BG_DARK,
            justify="left",
        )
        banner_lbl.pack(pady=(15, 5))

        subtitle = tk.Label(
            self.container,
            text="PIXELTOWN OFFICIAL LAUNCHER",
            font=("Segoe UI", 14, "bold"),
            fg=FG_TEXT,
            bg=BG_DARK,
        )
        subtitle.pack(pady=(0, 3))

        welcome = tk.Label(
            self.container,
            text="Choose execution platform / Selecciona la plataforma" if is_en else "¿Cómo deseas ejecutar el juego?",
            font=("Segoe UI", 11),
            fg=FG_DIM,
            bg=BG_DARK,
        )
        welcome.pack(pady=(0, 10))

        # Separator
        sep = tk.Frame(self.container, bg=BORDER_COLOR, height=1)
        sep.pack(fill="x", padx=60, pady=5)

        # Card container for options
        card = tk.Frame(self.container, bg=BG_CARD, padx=40, pady=20,
                        highlightthickness=1, highlightbackground=BORDER_COLOR)
        card.pack(pady=10)

        # Option 1: Pygame Window (Desktop)
        pygame_label = "🖥️  Classic Pygame Window" if is_en else "🖥️  Ventana de Pygame clásica"
        pygame_desc_text = "Native desktop mode with standalone window" if is_en else "Modo clásico de escritorio con ventana independiente"
        pygame_btn = _make_button(
            card, pygame_label,
            self._show_auth_screen,
            bg=BTN_PRIMARY, hover=BTN_PRIMARY_H, width=34, font_size=12, pady=8,
        )
        pygame_btn.pack(pady=(4, 2))

        pygame_desc = tk.Label(
            card,
            text=pygame_desc_text,
            font=("Segoe UI", 9),
            fg=FG_DIM,
            bg=BG_CARD,
        )
        pygame_desc.pack(pady=(0, 10))

        # Option 2: Web Localhost (pygbag)
        web_label = "🌐  Web Localhost Format (pygbag)" if is_en else "🌐  Formato Web Localhost (pygbag)"
        web_desc_text = "Local WebAssembly browser server (HTML5 / canvas)" if is_en else "Servidor local WebAssembly en tu navegador (HTML5 / canvas)"
        web_btn = _make_button(
            card, web_label,
            self._show_web_mode_screen,
            bg=BTN_SUCCESS, hover=BTN_SUCCESS_H, width=34, font_size=12, pady=8,
        )
        web_btn.pack(pady=(2, 2))

        web_desc = tk.Label(
            card,
            text=web_desc_text,
            font=("Segoe UI", 9),
            fg=FG_DIM,
            bg=BG_CARD,
        )
        web_desc.pack(pady=(0, 10))

        # Back to language selection
        back_lang_btn = _make_button(
            card, "⬅️  Change Language" if is_en else "⬅️  Cambiar idioma",
            self._show_language_screen,
            bg="#555", hover="#777", width=34, font_size=10, pady=6,
        )
        back_lang_btn.pack(pady=(2, 2))

        # Option 3: Exit
        exit_btn = _make_button(
            card, "❌  Exit" if is_en else "❌  Salir",
            self._exit,
            bg=BTN_DANGER, hover=BTN_DANGER_H, width=34, font_size=10, pady=6,
        )
        exit_btn.pack(pady=(4, 4))

        # Footer
        footer = tk.Label(
            self.container,
            text="© 2026 Raúl Salas Sahuquillo",
            font=("Segoe UI", 9),
            fg=FG_DIM,
            bg=BG_DARK,
        )
        footer.pack(side="bottom", pady=10)

    # Web Localhost (Pygbag) Screen
    def _show_web_mode_screen(self):
        self._clear()
        is_en = (self.selected_language == "en")

        # Find an available port starting at 8000
        self.web_port = find_available_port(8000)
        self.web_url = f"http://localhost:{self.web_port}/?lang={self.selected_language}"

        # Title
        title_text = "🌐 PIXELTOWN — WEB MODE (PYGBAG)" if is_en else "🌐 PIXELTOWN — MODO WEB (PYGBAG)"
        title = tk.Label(
            self.container,
            text=title_text,
            font=("Segoe UI", 16, "bold"),
            fg=FG_ACCENT,
            bg=BG_DARK,
        )
        title.pack(pady=(15, 3))

        subtitle_text = f"Localhost WebAssembly Server — {self.web_url}" if is_en else f"Servidor WebAssembly Localhost — {self.web_url}"
        subtitle = tk.Label(
            self.container,
            text=subtitle_text,
            font=("Segoe UI", 10),
            fg=FG_DIM,
            bg=BG_DARK,
        )
        subtitle.pack(pady=(0, 10))

        # Control Card
        card = tk.Frame(self.container, bg=BG_CARD, padx=20, pady=12,
                        highlightthickness=1, highlightbackground=BORDER_COLOR)
        card.pack(fill="x", padx=40)

        # Status label
        status_init = "🟡 Starting pygbag server..." if is_en else "🟡 Iniciando servidor pygbag..."
        self.web_status_label = tk.Label(
            card,
            text=status_init,
            font=("Segoe UI", 11, "bold"),
            fg="#f1c40f",
            bg=BG_CARD,
        )
        self.web_status_label.pack(pady=(0, 8))

        # Action buttons
        btn_box = tk.Frame(card, bg=BG_CARD)
        btn_box.pack()

        open_btn_text = "🚀  Open in Browser" if is_en else "🚀  Abrir en Navegador"
        open_browser_btn = _make_button(
            btn_box, open_btn_text,
            lambda: webbrowser.open(self.web_url),
            bg=BTN_PRIMARY, hover=BTN_PRIMARY_H, width=20, font_size=11, pady=6,
        )
        open_browser_btn.pack(side="left", padx=6)

        stop_btn_text = "⏹️  Stop and Return" if is_en else "⏹️  Detener y Volver"
        stop_btn = _make_button(
            btn_box, stop_btn_text,
            self._on_stop_web_mode,
            bg=BTN_DANGER, hover=BTN_DANGER_H, width=20, font_size=11, pady=6,
        )
        stop_btn.pack(side="left", padx=6)

        # Pygbag terminal log frame
        log_frame = tk.Frame(self.container, bg=BG_DARK)
        log_frame.pack(fill="both", expand=True, padx=40, pady=(10, 5))

        lbl_log = tk.Label(
            log_frame,
            text="Pygbag Terminal Output:" if is_en else "Terminal / Salida de pygbag:",
            font=("Segoe UI", 9, "bold"),
            fg=FG_TEXT,
            bg=BG_DARK,
            anchor="w",
        )
        lbl_log.pack(fill="x", pady=(0, 2))


        # Text area with dark scrollbar
        text_container = tk.Frame(log_frame, bg=BG_INPUT,
                                  highlightthickness=1, highlightbackground=BORDER_COLOR)
        text_container.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(text_container)
        scrollbar.pack(side="right", fill="y")

        self.web_log_text = tk.Text(
            text_container,
            bg=BG_INPUT,
            fg="#a8d0e6",
            font=("Consolas", 9),
            relief="flat",
            wrap="word",
            yscrollcommand=scrollbar.set,
        )
        self.web_log_text.pack(fill="both", expand=True)
        scrollbar.config(command=self.web_log_text.yview)

        # Footer
        footer = tk.Label(
            self.container,
            text="© 2026 Raúl Salas Sahuquillo",
            font=("Segoe UI", 9),
            fg=FG_DIM,
            bg=BG_DARK,
        )
        footer.pack(side="bottom", pady=5)

        # Launch the pygbag server process
        self._start_pygbag_server()

    def _start_pygbag_server(self):
        if self.pygbag_proc is not None and self.pygbag_proc.poll() is None:
            if self.web_status_label:
                self.web_status_label.config(
                    text=f"🟢 Servidor activo en {self.web_url}",
                    fg=BTN_SUCCESS
                )
            return

        self._browser_opened = False

        if getattr(sys, 'frozen', False):
            project_dir = os.path.dirname(sys.executable)
        else:
            project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        if self.web_port != 8000:
            self._append_pygbag_log(
                f"[INFO] El puerto 8000 está ocupado (ej. por FastAPI u otro proceso).\n"
                f"[INFO] Asignando automáticamente el puerto libre {self.web_port}.\n\n"
            )

        cmd = [
            sys.executable, "-m", "pygbag",
            "--bind", "localhost",
            "--port", str(self.web_port),
        ]

        template_path = os.path.join(project_dir, "web_template.tmpl")
        if os.path.exists(template_path):
            cmd.extend(["--template", template_path])

        cmd.extend([
            "--no_opt",
            "--disable-sound-format-error",
            project_dir,
        ])

        self._append_pygbag_log(f"$ {' '.join(cmd)}\nIniciando servidor pygbag...\n")

        try:
            self.pygbag_proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                cwd=project_dir,
            )
        except Exception as e:
            self._append_pygbag_log(f"Error al iniciar pygbag: {e}\n")
            if self.web_status_label:
                self.web_status_label.config(text=f"❌ Error al iniciar: {e}", fg=BTN_DANGER)
            return

        def reader_thread():
            ready_detected = False
            try:
                for line in iter(self.pygbag_proc.stdout.readline, ''):
                    if not line:
                        break
                    self.root.after(0, self._append_pygbag_log, line)
                    line_lower = line.lower()
                    if not ready_detected and ("serving python files" in line_lower or "http://" in line_lower or "test server" in line_lower or "ready" in line_lower):
                        ready_detected = True
                        self.root.after(0, self._on_pygbag_ready)
            except Exception:
                pass
            finally:
                if self.pygbag_proc and self.pygbag_proc.stdout:
                    try:
                        self.pygbag_proc.stdout.close()
                    except Exception:
                        pass
                self.root.after(0, self._on_pygbag_exited)

        self.pygbag_thread = threading.Thread(target=reader_thread, daemon=True)
        self.pygbag_thread.start()

        # Automatic fallback timer to open browser and confirm readiness
        self.root.after(3500, self._on_pygbag_ready)

    def _on_pygbag_ready(self):
        is_en = (self.selected_language == "en")
        if self.pygbag_proc and self.pygbag_proc.poll() is None:
            if self.web_status_label and self.web_status_label.winfo_exists():
                status_text = f"🟢 Pygbag server active at {self.web_url}" if is_en else f"🟢 Servidor pygbag activo en {self.web_url}"
                self.web_status_label.config(
                    text=status_text,
                    fg=BTN_SUCCESS
                )
            if not self._browser_opened:
                self._browser_opened = True
                try:
                    webbrowser.open(self.web_url)
                except Exception as e:
                    err_msg = f"Could not open browser automatically: {e}\n" if is_en else f"No se pudo abrir el navegador automáticamente: {e}\n"
                    self._append_pygbag_log(err_msg)

    def _on_pygbag_exited(self):
        is_en = (self.selected_language == "en")
        code = self.pygbag_proc.poll() if self.pygbag_proc else None
        if self.web_status_label and self.web_status_label.winfo_exists():
            if code is not None and code != 0 and code != -15 and code != -9:
                status_text = f"🔴 Server terminated (code {code})" if is_en else f"🔴 Servidor finalizado (código {code})"
                self.web_status_label.config(text=status_text, fg=BTN_DANGER)
            else:
                status_text = "⚪ Server stopped" if is_en else "⚪ Servidor detenido"
                self.web_status_label.config(text=status_text, fg=FG_DIM)

    def _append_pygbag_log(self, text):
        if self.web_log_text and self.web_log_text.winfo_exists():
            self.web_log_text.insert(tk.END, text)
            self.web_log_text.see(tk.END)

    def _stop_pygbag_server(self):
        self._browser_opened = False
        if self.pygbag_proc is not None:
            try:
                self.pygbag_proc.terminate()
                self.pygbag_proc.wait(timeout=2)
            except Exception:
                try:
                    self.pygbag_proc.kill()
                except Exception:
                    pass
            self.pygbag_proc = None

    def _on_stop_web_mode(self):
        self._stop_pygbag_server()
        self._show_mode_selection_screen()

    def _on_window_close(self):
        self._stop_pygbag_server()
        self.root.destroy()
        sys.exit(0)

    # Auth (Login / Register / Guest / Exit) 

    def _show_auth_screen(self):
        self._clear()

        # Title
        title = tk.Label(
            self.container,
            text=_("terminal_menu_title").strip().strip("-").strip(),
            font=("Segoe UI", 18, "bold"),
            fg=FG_ACCENT,
            bg=BG_DARK,
        )
        title.pack(pady=(40, 25))

        # Card frame
        card = tk.Frame(self.container, bg=BG_CARD, padx=40, pady=30,
                        highlightthickness=1, highlightbackground=BORDER_COLOR)
        card.pack()

        # Buttons
        login_button = _make_button(
            card,
            _("terminal_option_login").lstrip("1. ").lstrip("1.").strip(),
            self._show_login_screen,
            bg=BTN_PRIMARY, hover=BTN_PRIMARY_H, width=26, font_size=13, pady=10,
        )
        login_button.pack(pady=6)

        register_button = _make_button(
            card,
            _("terminal_option_register").lstrip("2. ").lstrip("2.").strip(),
            self._show_register_screen,
            bg=BTN_SUCCESS, hover=BTN_SUCCESS_H, width=26, font_size=13, pady=10,
        )
        register_button.pack(pady=6)

        guest_button = _make_button(
            card,
            _("terminal_option_guest").lstrip("3. ").lstrip("3.").strip(),
            self._play_as_guest,
            bg=BTN_GUEST, hover=BTN_GUEST_H, width=26, font_size=13, pady=10,
        )
        guest_button.pack(pady=6)

        back_button = _make_button(
            card,
            "⬅️  Back to Modes" if self.selected_language == "en" else "⬅️  Volver a Selección de Modo",
            self._show_mode_selection_screen,
            bg="#555", hover="#777", width=26, font_size=11, pady=8,
        )
        back_button.pack(pady=6)

        exit_button = _make_button(

            card,
            _("terminal_option_exit").lstrip("4. ").lstrip("4.").strip(),
            self._exit,
            bg=BTN_DANGER, hover=BTN_DANGER_H, width=26, font_size=13, pady=10,
        )
        exit_button.pack(pady=(6, 0))

        # Footer
        footer = tk.Label(
            self.container,
            text="© 2026 Raúl Salas Sahuquillo",
            font=("Segoe UI", 9),
            fg=FG_DIM,
            bg=BG_DARK,
        )
        footer.pack(side="bottom", pady=15)

    # Screen: Login
    def _show_login_screen(self):
        self._clear()

        title = tk.Label(
            self.container,
            text=_("terminal_option_login").lstrip("1. ").lstrip("1.").strip(),
            font=("Segoe UI", 18, "bold"),
            fg=FG_ACCENT,
            bg=BG_DARK,
        )
        title.pack(pady=(50, 25))

        card = tk.Frame(self.container, bg=BG_CARD, padx=40, pady=30,
                        highlightthickness=1, highlightbackground=BORDER_COLOR)
        card.pack()

        # Username
        lbl_user = tk.Label(card, text=_("terminal_enter_username").rstrip(": ").strip(),
                            font=("Segoe UI", 11), fg=FG_TEXT, bg=BG_CARD, anchor="w")
        lbl_user.pack(fill="x", pady=(0, 3))
        user_entry, user_var = _make_entry(card)
        user_entry.pack(fill="x", ipady=6, pady=(0, 12))

        # Password
        lbl_pass = tk.Label(card, text=_("terminal_enter_password").rstrip(": ").strip(),
                            font=("Segoe UI", 11), fg=FG_TEXT, bg=BG_CARD, anchor="w")
        lbl_pass.pack(fill="x", pady=(0, 3))
        pass_entry, pass_var = _make_entry(card, show="●")
        pass_entry.pack(fill="x", ipady=6, pady=(0, 18))

        # Status label
        status = tk.Label(card, text="", font=("Segoe UI", 10), fg=BTN_DANGER, bg=BG_CARD)
        status.pack(pady=(0, 8))

        def do_login(_event=None):
            username = user_var.get().strip()
            password = pass_var.get().strip()
            if not username:
                status.config(text=_("terminal_username_empty"), fg=BTN_DANGER)
                return
            if not password:
                status.config(text=_("terminal_password_empty"), fg=BTN_DANGER)
                return
            hashed = hash_password(password)
            if username in self.accounts and self.accounts[username] == hashed:
                self.logged_in_user = username
                self._launch_game()
            else:
                status.config(text=_("terminal_login_fail"), fg=BTN_DANGER)

        login_button = _make_button(card, _("terminal_option_login").lstrip("1. ").lstrip("1.").strip(),
                                 do_login, bg=BTN_PRIMARY, hover=BTN_PRIMARY_H, width=24)
        login_button.pack(pady=4)

        # Bind Enter key
        pass_entry.bind("<Return>", do_login)
        user_entry.bind("<Return>", lambda _e: pass_entry.focus_set())

        # Back button
        back_button = _make_button(card, _("back"),
                                self._show_auth_screen,
                                bg="#555", hover="#777", width=24, font_size=10)
        back_button.pack(pady=(4, 0))

        user_entry.focus_set()

    # Register
    def _show_register_screen(self):
        self._clear()

        title = tk.Label(
            self.container,
            text=_("terminal_option_register").lstrip("2. ").lstrip("2.").strip(),
            font=("Segoe UI", 18, "bold"),
            fg=FG_ACCENT,
            bg=BG_DARK,
        )
        title.pack(pady=(50, 25))

        card = tk.Frame(self.container, bg=BG_CARD, padx=40, pady=30,
                        highlightthickness=1, highlightbackground=BORDER_COLOR)
        card.pack()

        # Username
        lbl_user = tk.Label(card, text=_("terminal_enter_username").rstrip(": ").strip(),
                            font=("Segoe UI", 11), fg=FG_TEXT, bg=BG_CARD, anchor="w")
        lbl_user.pack(fill="x", pady=(0, 3))
        user_entry, user_var = _make_entry(card)
        user_entry.pack(fill="x", ipady=6, pady=(0, 12))

        # Password
        lbl_pass = tk.Label(card, text=_("terminal_enter_password").rstrip(": ").strip(),
                            font=("Segoe UI", 11), fg=FG_TEXT, bg=BG_CARD, anchor="w")
        lbl_pass.pack(fill="x", pady=(0, 3))
        pass_entry, pass_var = _make_entry(card, show="●")
        pass_entry.pack(fill="x", ipady=6, pady=(0, 18))

        # Status label
        status = tk.Label(card, text="", font=("Segoe UI", 10), fg=BTN_DANGER, bg=BG_CARD)
        status.pack(pady=(0, 8))

        def do_register(_event=None):
            username = user_var.get().strip()
            password = pass_var.get().strip()
            if not username:
                status.config(text=_("terminal_username_empty"), fg=BTN_DANGER)
                return
            if username in self.accounts:
                status.config(text=_("terminal_register_exists").format(username=username),
                              fg=BTN_DANGER)
                return
            if not password:
                status.config(text=_("terminal_password_empty"), fg=BTN_DANGER)
                return
            self.accounts[username] = hash_password(password)
            if save_accounts(self.accounts):
                self.logged_in_user = username
                self._launch_game()
            else:
                status.config(text=_("error_saving_account"), fg=BTN_DANGER)

        register_button = _make_button(card, _("terminal_option_register").lstrip("2. ").lstrip("2.").strip(),
                                    do_register, bg=BTN_SUCCESS, hover=BTN_SUCCESS_H, width=24)
        register_button.pack(pady=4)

        pass_entry.bind("<Return>", do_register)
        user_entry.bind("<Return>", lambda _e: pass_entry.focus_set())

        # Back button
        back_button = _make_button(card, _("back"),
                                self._show_auth_screen,
                                bg="#555", hover="#777", width=24, font_size=10)
        back_button.pack(pady=(4, 0))

        user_entry.focus_set()

    # Actions
    def _play_as_guest(self):
        self.logged_in_user = None
        self._launch_game()

    def _exit(self):
        self._stop_pygbag_server()
        self.root.destroy()
        sys.exit(0)

    def _launch_game(self):
        """Destroy the tkinter window and hand control to the pygame game."""
        username = self.logged_in_user
        self._stop_pygbag_server()
        self.root.destroy()
        # Import here to avoid circular / early-pygame-init issues
        from game import main
        main(username=username)

    # Utilities
    def _clear(self):
        """Remove every widget from the container."""
        for w in self.container.winfo_children():
            w.destroy()

    def run(self):
        self.root.mainloop()

#  Public entry point — kept backward-compatible
def terminal_beginning():
    app = TerminalApp()
    app.run()

terminalbeggining = terminal_beginning