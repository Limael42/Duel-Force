# Page paramètres

import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import config
import keybindings

class SettingsPage:
    def __init__(self, parent_frame, return_callback, screen_width=None, screen_height=None, show_keybindings_callback=None):
        self.parent_frame = parent_frame
        self.return_callback = return_callback
        self.show_keybindings_callback = show_keybindings_callback
        if screen_width is None or screen_height is None:
            screen_width = parent_frame.winfo_width() if parent_frame.winfo_width() > 1 else 900
            screen_height = parent_frame.winfo_height() if parent_frame.winfo_height() > 1 else 900

        title_size = max(18, min(int(screen_height * 0.05), 60))
        section_size = max(14, min(int(screen_height * 0.03), 40))
        player_size = max(12, min(int(screen_height * 0.022), 30))
        text_size = max(10, min(int(screen_height * 0.018), 24))
        button_size = max(11, min(int(screen_height * 0.02), 28))

        title_font = font.Font(family="Segoe UI", size=title_size, weight="bold")

        # Espacements adaptatifs
        header_pady = int(screen_height * 0.02)  # 2% de la hauteur 
        section_pady = int(screen_height * 0.03)  # 3% de la hauteur

        # Header avec titre et bouton retour
        header_frame = tk.Frame(parent_frame, bg=config.COLOR_BG)
        header_frame.pack(fill=tk.X, pady=header_pady)

        back_btn_padx = int(screen_width * 0.01)
        back_btn_pady = int(screen_height * 0.008)
        back_icon_btn = tk.Button(
            header_frame,
            text="← MENU",
            command=self.return_callback,
            font=("Segoe UI", button_size, "bold"),
            bg=config.COLOR_BUTTON,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=back_btn_padx,
            pady=back_btn_pady
        )
        back_icon_btn.pack(side=tk.LEFT, padx=int(screen_width * 0.02))
        back_icon_btn.bind("<Enter>", lambda e: back_icon_btn.config(bg=config.COLOR_BUTTON_HOVER))
        back_icon_btn.bind("<Leave>", lambda e: back_icon_btn.config(bg=config.COLOR_BUTTON))
        title = tk.Label(
            header_frame,
            text="⚙ PARAMÈTRES",
            font=title_font,
            bg=config.COLOR_BG,
            fg=config.COLOR_TEXT
        )
        title.pack(side=tk.LEFT, expand=True)

        settings_container = tk.Frame(parent_frame, bg=config.COLOR_BG)
        settings_container.pack(expand=True)

        controls_title = tk.Label(
            settings_container,
            text="CONTRÔLES ACTUELS",
            font=("Segoe UI", section_size, "bold"),
            bg=config.COLOR_BG,
            fg=config.COLOR_TEXT
        )
        controls_title.pack(pady=section_pady)

        player1_frame = tk.Frame(settings_container, bg=config.COLOR_BG)
        player1_pady = int(screen_height * 0.015)
        player1_frame.pack(pady=player1_pady)

        tk.Label(
            player1_frame,
            text="JOUEUR 1 (Rouge) - À GAUCHE",
            font=("Segoe UI", player_size, "bold"),
            bg=config.COLOR_BG,
            fg=config.COLOR_PLAYER1
        ).pack(pady=10)

        # Charger les touches actuelles
        current_bindings = keybindings.load_keybindings()
        p1_bindings = current_bindings['player1']

        controls1_text = (
            f"{keybindings.get_key_display_name(p1_bindings['left'])} / {keybindings.get_key_display_name(p1_bindings['right'])} : Déplacement gauche/droite\n"
            f"{keybindings.get_key_display_name(p1_bindings['jump'])} : Saut (double saut possible)\n"
            f"{keybindings.get_key_display_name(p1_bindings['attack'])} : Attaque normale\n"
            f"{keybindings.get_key_display_name(p1_bindings['special'])} : Attaque spéciale"
        )

        tk.Label(
            player1_frame,
            text=controls1_text,
            font=("Segoe UI", text_size),
            bg=config.COLOR_BG,
            fg=config.COLOR_TEXT,
            justify=tk.LEFT
        ).pack()

        separator_padx = int(screen_width * 0.1)
        separator_pady = int(screen_height * 0.02)
        separator = tk.Frame(settings_container, height=3, bg="#335C81")
        separator.pack(fill=tk.X, padx=separator_padx, pady=separator_pady)

        player2_frame = tk.Frame(settings_container, bg=config.COLOR_BG)
        player2_frame.pack(pady=player1_pady)

        tk.Label(
            player2_frame,
            text="JOUEUR 2 (Orange) - À DROITE",
            font=("Segoe UI", player_size, "bold"),
            bg=config.COLOR_BG,
            fg=config.COLOR_PLAYER2
        ).pack(pady=10)

        p2_bindings = current_bindings['player2']

        controls2_text = (
            f"{keybindings.get_key_display_name(p2_bindings['left'])} / {keybindings.get_key_display_name(p2_bindings['right'])} : Déplacement gauche/droite\n"
            f"{keybindings.get_key_display_name(p2_bindings['jump'])} : Saut (double saut possible)\n"
            f"{keybindings.get_key_display_name(p2_bindings['attack'])} : Attaque normale\n"
            f"{keybindings.get_key_display_name(p2_bindings['special'])} : Attaque spéciale"
        )

        tk.Label(
            player2_frame,
            text=controls2_text,
            font=("Segoe UI", text_size),
            bg=config.COLOR_BG,
            fg=config.COLOR_TEXT,
            justify=tk.LEFT
        ).pack()
