"""
PIXELTOWN - This is the PIXELTOWN's terminal, in its early developement.
Copyright (C) 2026  Raúl Salas Sahuquillo, ENEI PROJECT

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
        return False


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
                 fg="white", width=22, font_size=12, pady=8):
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

        # Try to set the window icon
        try:
            icon_path = _asset_path("imagenes", "pixeltown_logo.png")
            icon = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(True, icon)
        except Exception:
            pass

        self.accounts = load_accounts()
        self.logged_in_user = None  # will be set after auth

        # Container frame (for screen-swapping)
        self.container = tk.Frame(self.root, bg=BG_DARK)
        self.container.pack(fill="both", expand=True)

        # Start on the language-selection screen
        self._show_language_screen()

    # Language Selection 
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
        banner_lbl.pack(pady=(30, 5))

        subtitle = tk.Label(
            self.container,
            text="PIXELTOWN OFFICIAL TERMINAL",
            font=("Segoe UI", 14, "bold"),
            fg=FG_TEXT,
            bg=BG_DARK,
        )
        subtitle.pack(pady=(0, 5))

        welcome = tk.Label(
            self.container,
            text="Welcome to the PIXELTOWN terminal!",
            font=("Segoe UI", 11),
            fg=FG_DIM,
            bg=BG_DARK,
        )
        welcome.pack(pady=(0, 30))

        # Separator
        sep = tk.Frame(self.container, bg=BORDER_COLOR, height=1)
        sep.pack(fill="x", padx=60, pady=5)

        lang_label = tk.Label(
            self.container,
            text="Select your language / Selecciona tu idioma",
            font=("Segoe UI", 12),
            fg=FG_TEXT,
            bg=BG_DARK,
        )
        lang_label.pack(pady=(20, 15))

        btn_frame = tk.Frame(self.container, bg=BG_DARK)
        btn_frame.pack()

        btn_es = _make_button(
            btn_frame, "🇪🇸  Español", lambda: self._select_language("es"),
            bg="#e67e22", hover="#f0932b", width=18, font_size=13, pady=10,
        )
        btn_es.pack(side="left", padx=12)

        btn_en = _make_button(
            btn_frame, "🇬🇧  English", lambda: self._select_language("en"),
            bg="#3498db", hover="#5dade2", width=18, font_size=13, pady=10,
        )
        btn_en.pack(side="left", padx=12)

        # Footer
        footer = tk.Label(
            self.container,
            text="© 2026 Raúl Salas Sahuquillo — ENEI PROJECT",
            font=("Segoe UI", 9),
            fg=FG_DIM,
            bg=BG_DARK,
        )
        footer.pack(side="bottom", pady=15)

    def _select_language(self, code):
        load_language(code)
        self._show_auth_screen()

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
        btn_login = _make_button(
            card,
            _("terminal_option_login").lstrip("1. ").lstrip("1.").strip(),
            self._show_login_screen,
            bg=BTN_PRIMARY, hover=BTN_PRIMARY_H, width=26, font_size=13, pady=10,
        )
        btn_login.pack(pady=6)

        btn_register = _make_button(
            card,
            _("terminal_option_register").lstrip("2. ").lstrip("2.").strip(),
            self._show_register_screen,
            bg=BTN_SUCCESS, hover=BTN_SUCCESS_H, width=26, font_size=13, pady=10,
        )
        btn_register.pack(pady=6)

        btn_guest = _make_button(
            card,
            _("terminal_option_guest").lstrip("3. ").lstrip("3.").strip(),
            self._play_as_guest,
            bg=BTN_GUEST, hover=BTN_GUEST_H, width=26, font_size=13, pady=10,
        )
        btn_guest.pack(pady=6)

        btn_exit = _make_button(
            card,
            _("terminal_option_exit").lstrip("4. ").lstrip("4.").strip(),
            self._exit,
            bg=BTN_DANGER, hover=BTN_DANGER_H, width=26, font_size=13, pady=10,
        )
        btn_exit.pack(pady=(6, 0))

        # Footer
        footer = tk.Label(
            self.container,
            text="© 2026 Raúl Salas Sahuquillo — ENEI PROJECT",
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
        ent_user, var_user = _make_entry(card)
        ent_user.pack(fill="x", ipady=6, pady=(0, 12))

        # Password
        lbl_pass = tk.Label(card, text=_("terminal_enter_password").rstrip(": ").strip(),
                            font=("Segoe UI", 11), fg=FG_TEXT, bg=BG_CARD, anchor="w")
        lbl_pass.pack(fill="x", pady=(0, 3))
        ent_pass, var_pass = _make_entry(card, show="●")
        ent_pass.pack(fill="x", ipady=6, pady=(0, 18))

        # Status label
        status = tk.Label(card, text="", font=("Segoe UI", 10), fg=BTN_DANGER, bg=BG_CARD)
        status.pack(pady=(0, 8))

        def do_login(_event=None):
            username = var_user.get().strip()
            password = var_pass.get().strip()
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

        btn_login = _make_button(card, _("terminal_option_login").lstrip("1. ").lstrip("1.").strip(),
                                 do_login, bg=BTN_PRIMARY, hover=BTN_PRIMARY_H, width=24)
        btn_login.pack(pady=4)

        # Bind Enter key
        ent_pass.bind("<Return>", do_login)
        ent_user.bind("<Return>", lambda _e: ent_pass.focus_set())

        # Back button
        btn_back = _make_button(card, _("back"),
                                self._show_auth_screen,
                                bg="#555", hover="#777", width=24, font_size=10)
        btn_back.pack(pady=(4, 0))

        ent_user.focus_set()

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
        ent_user, var_user = _make_entry(card)
        ent_user.pack(fill="x", ipady=6, pady=(0, 12))

        # Password
        lbl_pass = tk.Label(card, text=_("terminal_enter_password").rstrip(": ").strip(),
                            font=("Segoe UI", 11), fg=FG_TEXT, bg=BG_CARD, anchor="w")
        lbl_pass.pack(fill="x", pady=(0, 3))
        ent_pass, var_pass = _make_entry(card, show="●")
        ent_pass.pack(fill="x", ipady=6, pady=(0, 18))

        # Status label
        status = tk.Label(card, text="", font=("Segoe UI", 10), fg=BTN_DANGER, bg=BG_CARD)
        status.pack(pady=(0, 8))

        def do_register(_event=None):
            username = var_user.get().strip()
            password = var_pass.get().strip()
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

        btn_register = _make_button(card, _("terminal_option_register").lstrip("2. ").lstrip("2.").strip(),
                                    do_register, bg=BTN_SUCCESS, hover=BTN_SUCCESS_H, width=24)
        btn_register.pack(pady=4)

        ent_pass.bind("<Return>", do_register)
        ent_user.bind("<Return>", lambda _e: ent_pass.focus_set())

        # Back button
        btn_back = _make_button(card, _("back"),
                                self._show_auth_screen,
                                bg="#555", hover="#777", width=24, font_size=10)
        btn_back.pack(pady=(4, 0))

        ent_user.focus_set()

    # Actions
    def _play_as_guest(self):
        self.logged_in_user = None
        self._launch_game()

    def _exit(self):
        self.root.destroy()
        sys.exit(0)

    def _launch_game(self):
        """Destroy the tkinter window and hand control to the pygame game."""
        username = self.logged_in_user
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
def terminalbeggining():
    app = TerminalApp()
    app.run()