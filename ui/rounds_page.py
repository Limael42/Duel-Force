# Page sélection rounds

import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import config


class RoundsPage:
    def __init__(self, root, parent_frame, return_callback, map_selection_callback,
                 pseudo1, pseudo2, screen_width=None, screen_height=None):
        self.root = root
        self.parent_frame = parent_frame
        self.return_callback = return_callback
        self.map_selection_callback = map_selection_callback
        self.pseudo1 = pseudo1
        self.pseudo2 = pseudo2
        if screen_width is None or screen_height is None:
            screen_width = root.winfo_width() if root.winfo_width() > 1 else 900
            screen_height = root.winfo_height() if root.winfo_height() > 1 else 900
        title_size = max(18, min(int(screen_height * 0.055), 70))
        subtitle_size = max(12, min(int(screen_height * 0.022), 32))
        button_size = max(14, min(int(screen_height * 0.025), 35))
        info_size = max(11, min(int(screen_height * 0.018), 26))
        title_pady = int(screen_height * 0.04)
        subtitle_pady = int(screen_height * 0.015)
        button_pady = int(screen_height * 0.02)

        # Bouton retour en haut à gauche
        back_icon_btn = tk.Button(
            parent_frame,
            text="← RETOUR",
            command=return_callback,
            font=("Segoe UI", max(10, min(int(screen_height * 0.018), 20)), "bold"),
            bg=config.COLOR_BUTTON,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8
        )
        back_icon_btn.place(x=20, y=20)
        back_icon_btn.bind("<Enter>", lambda e: back_icon_btn.config(bg=config.COLOR_BUTTON_HOVER))
        back_icon_btn.bind("<Leave>", lambda e: back_icon_btn.config(bg=config.COLOR_BUTTON))

        title_font = font.Font(family="Segoe UI", size=title_size, weight="bold")
        title = tk.Label(
            parent_frame,
            text="⚔️ SÉLECTION DU MODE DE JEU",
            font=title_font,
            bg=config.COLOR_BG,
            fg=config.COLOR_TEXT
        )
        title.pack(pady=title_pady)
        subtitle_text = f"{pseudo1} VS {pseudo2}"
        subtitle = tk.Label(
            parent_frame,
            text=subtitle_text,
            font=("Segoe UI", subtitle_size, "bold"),
            bg=config.COLOR_BG,
            fg="#FFFFFF"
        )
        subtitle.pack(pady=subtitle_pady)

        info = tk.Label(
            parent_frame,
            text="Choisissez le nombre de rounds à jouer",
            font=("Segoe UI", info_size),
            bg=config.COLOR_BG,
            fg=config.COLOR_TEXT
        )
        info.pack(pady=int(screen_height * 0.01))

        buttons_container = tk.Frame(parent_frame, bg=config.COLOR_BG)
        buttons_container.pack(expand=True, pady=int(screen_height * 0.03))

        btn_width = int(screen_width * 0.018)
        btn_height = int(screen_height * 0.005)
        row1_frame = tk.Frame(buttons_container, bg=config.COLOR_BG)
        row1_frame.pack(pady=button_pady)

        btn_1 = self.create_round_button(
            row1_frame,
            "1 PARTIE",
            "Partie unique",
            1,
            "#DC143C",  # Rouge crimson
            button_size,
            btn_width,
            btn_height
        )
        btn_1.pack(side=tk.LEFT, padx=int(screen_width * 0.02))

        btn_3 = self.create_round_button(
            row1_frame,
            "3 PARTIES",
            "Premier à 2 victoires",
            3,
            "#C41E3A",  # Rouge cardinal
            button_size,
            btn_width,
            btn_height
        )
        btn_3.pack(side=tk.LEFT, padx=int(screen_width * 0.02))

        row2_frame = tk.Frame(buttons_container, bg=config.COLOR_BG)
        row2_frame.pack(pady=button_pady)

        btn_5 = self.create_round_button(
            row2_frame,
            "5 PARTIES",
            "Premier à 3 victoires",
            5,
            "#B01030",  # Rouge moyen
            button_size,
            btn_width,
            btn_height
        )
        btn_5.pack(side=tk.LEFT, padx=int(screen_width * 0.02))

        btn_10 = self.create_round_button(
            row2_frame,
            "10 PARTIES",
            "Premier à 6 victoires",
            10,
            "#8B0000",  # Rouge foncé
            button_size,
            btn_width,
            btn_height
        )
        btn_10.pack(side=tk.LEFT, padx=int(screen_width * 0.02))

    def create_round_button(self, parent, text, description, rounds, color, font_size, width, height):
        frame = tk.Frame(parent, bg=config.COLOR_BG)

        button = tk.Button(
            frame,
            text=text,
            command=lambda: self.select_rounds(rounds),
            font=("Segoe UI", font_size, "bold"),
            bg=color,
            fg="white",
            width=width,
            height=height,
            relief=tk.FLAT,
            cursor="hand2"
        )
        button.pack(pady=(0, 5))

        desc_size = max(9, min(int(font_size * 0.6), 16))
        desc_label = tk.Label(
            frame,
            text=description,
            font=("Segoe UI", desc_size, "italic"),
            bg=config.COLOR_BG,
            fg="#FFFFFF"
        )
        desc_label.pack()

        darker_color = self.darken_color(color)
        button.bind("<Enter>", lambda e: button.config(bg=darker_color))
        button.bind("<Leave>", lambda e: button.config(bg=color))

        return frame

    def darken_color(self, color):
        dark_colors = {
            "#DC143C": "#B01030",  # Rouge crimson -> rouge moyen
            "#C41E3A": "#A01828",  # Rouge cardinal -> rouge plus foncé
            "#B01030": "#8B0000",  # Rouge moyen -> rouge foncé
            "#8B0000": "#6B0000",  # Rouge foncé -> rouge très foncé
        }
        return dark_colors.get(color, color)

    def select_rounds(self, rounds):
        # Aller à la sélection de map
        self.map_selection_callback(self.pseudo1, self.pseudo2, rounds)
