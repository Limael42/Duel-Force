"""
Page de sélection de map
Permet aux joueurs de choisir la map avant de commencer
"""

import tkinter as tk
from tkinter import font
import config
from game.maps import AVAILABLE_MAPS


class MapSelectionPage:
    """Classe gérant la page de sélection de map"""

    def __init__(self, root, parent_frame, return_callback, start_game_callback,
                 pseudo1, pseudo2, rounds, screen_width=None, screen_height=None):
        """Initialise la page de sélection de map

        Args:
            root: Fenêtre Tkinter principale
            parent_frame: Frame parent
            return_callback: Fonction pour retourner en arrière
            start_game_callback: Fonction pour lancer le jeu avec la map choisie
            pseudo1: Pseudo du joueur 1
            pseudo2: Pseudo du joueur 2
            rounds: Nombre de rounds
            screen_width: Largeur de l'écran
            screen_height: Hauteur de l'écran
        """
        self.root = root
        self.parent_frame = parent_frame
        self.return_callback = return_callback
        self.start_game_callback = start_game_callback
        self.pseudo1 = pseudo1
        self.pseudo2 = pseudo2
        self.rounds = rounds

        if screen_width is None or screen_height is None:
            screen_width = root.winfo_width() if root.winfo_width() > 1 else 900
            screen_height = root.winfo_height() if root.winfo_height() > 1 else 900

        # Polices adaptatives
        title_size = max(18, min(int(screen_height * 0.055), 70))
        subtitle_size = max(12, min(int(screen_height * 0.022), 32))
        button_size = max(14, min(int(screen_height * 0.025), 35))
        preview_size = max(8, min(int(screen_height * 0.015), 20))

        # Espacements
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

        # Titre
        title_font = font.Font(family="Segoe UI", size=title_size, weight="bold")
        title = tk.Label(
            parent_frame,
            text="🗺️ SÉLECTION DE LA MAP",
            font=title_font,
            bg=config.COLOR_BG,
            fg=config.COLOR_TEXT
        )
        title.pack(pady=title_pady)

        # Sous-titre avec infos match
        subtitle_text = f"{pseudo1} VS {pseudo2} • {rounds} round{'s' if rounds > 1 else ''}"
        subtitle = tk.Label(
            parent_frame,
            text=subtitle_text,
            font=("Segoe UI", subtitle_size, "bold"),
            bg=config.COLOR_BG,
            fg="#FFFFFF"
        )
        subtitle.pack(pady=subtitle_pady)

        # Container pour les maps (grid 2x3)
        maps_container = tk.Frame(parent_frame, bg=config.COLOR_BG)
        maps_container.pack(expand=True, pady=int(screen_height * 0.03))

        # Créer les boutons pour chaque map
        maps_list = list(AVAILABLE_MAPS.items())
        btn_width = int(screen_width * 0.015)
        btn_height = int(screen_height * 0.002)

        for idx, (map_id, map_config) in enumerate(maps_list):
            row = idx // 3
            col = idx % 3

            map_frame = self.create_map_button(
                maps_container,
                map_id,
                map_config,
                button_size,
                preview_size,
                btn_width,
                btn_height,
                screen_width,
                screen_height
            )
            map_frame.grid(row=row, column=col, padx=int(screen_width * 0.02),
                          pady=button_pady)

    def create_map_button(self, parent, map_id, map_config, font_size, preview_size,
                         width, height, screen_width, screen_height):
        """Crée un bouton de sélection de map avec prévisualisation"""
        frame = tk.Frame(parent, bg=config.COLOR_BG)

        # Container avec bordure
        card = tk.Frame(
            frame,
            bg="#8B0000",  # Rouge foncé pour les cartes
            relief=tk.SOLID,
            bd=2
        )
        card.pack(padx=5, pady=5)

        # Nom de la map
        name_label = tk.Label(
            card,
            text=map_config.name,
            font=("Segoe UI", font_size, "bold"),
            bg="#8B0000",
            fg="#FFFFFF"
        )
        name_label.pack(pady=(10, 5))

        # Prévisualisation visuelle avec canvas
        preview_canvas = tk.Canvas(
            card,
            width=200,
            height=120,
            bg="#001F3F",  # Fond bleu foncé pour le canvas de prévisualisation
            highlightthickness=0
        )
        preview_canvas.pack(pady=5)

        # Dessiner la prévisualisation de la map
        self.draw_map_preview(preview_canvas, map_config)

        # Description
        desc_label = tk.Label(
            card,
            text=map_config.description,
            font=("Segoe UI", max(8, min(int(font_size * 0.6), 14)), "italic"),
            bg="#8B0000",
            fg="#FFFFFF"
        )
        desc_label.pack(pady=5)

        # Bouton de sélection
        select_btn = tk.Button(
            card,
            text="CHOISIR",
            command=lambda: self.select_map(map_id),
            font=("Segoe UI", max(10, min(int(font_size * 0.7), 18)), "bold"),
            bg=config.COLOR_BUTTON,
            fg="white",
            width=12,
            height=1,
            relief=tk.FLAT,
            cursor="hand2"
        )
        select_btn.pack(pady=(5, 10))
        select_btn.bind("<Enter>", lambda e: select_btn.config(bg=config.COLOR_BUTTON_HOVER))
        select_btn.bind("<Leave>", lambda e: select_btn.config(bg=config.COLOR_BUTTON))

        return frame

    def draw_map_preview(self, canvas, map_config):
        """Dessine une prévisualisation miniature de la map sur le canvas"""
        # Dimensions du canvas de prévisualisation
        preview_width = 200
        preview_height = 120

        # Générer les plateformes de la map avec des dimensions fictives pour la prévisualisation
        platforms = map_config.platforms_func(preview_width, preview_height)

        # Dessiner chaque plateforme
        for platform in platforms:
            x, y, w, h = platform
            # Dessiner la plateforme
            canvas.create_rectangle(
                x, y, x + w, y + h,
                fill=config.PLATFORM_COLOR,
                outline=""
            )
            # Ligne plus claire sur le dessus
            canvas.create_rectangle(
                x, y, x + w, y + 2,
                fill=config.COLOR_BUTTON_HOVER,
                outline=""
            )

    def select_map(self, map_id):
        """Lance le jeu avec la map sélectionnée"""
        self.start_game_callback(self.pseudo1, self.pseudo2, self.rounds, map_id)
