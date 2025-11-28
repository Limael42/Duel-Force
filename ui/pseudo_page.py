"""
Page de saisie des pseudos
Permet aux joueurs d'entrer leurs pseudos avant de commencer
"""

import tkinter as tk
from tkinter import font, messagebox
import config
import database

class PseudoPage:
    """Classe gérant la page de saisie des pseudos"""

    def __init__(self, root, parent_frame, return_callback, start_game_callback, screen_width=None, screen_height=None):
        """Initialise la page de saisie des pseudos

        Args:
            root: Fenêtre Tkinter principale
            parent_frame: Frame parent
            return_callback: Fonction pour retourner au menu
            start_game_callback: Fonction pour lancer le jeu avec les pseudos
            screen_width: Largeur de l'écran (optionnel)
            screen_height: Hauteur de l'écran (optionnel)
        """
        self.root = root
        self.parent_frame = parent_frame
        self.return_callback = return_callback
        self.start_game_callback = start_game_callback

        # Utiliser les dimensions passées en paramètre ou récupérer depuis la fenêtre
        if screen_width is None or screen_height is None:
            screen_width = root.winfo_width() if root.winfo_width() > 1 else 900
            screen_height = root.winfo_height() if root.winfo_height() > 1 else 900

        # Polices adaptatives avec limites min/max
        title_size = max(18, min(int(screen_height * 0.055), 70))  # Entre 18 et 70px
        subtitle_size = max(12, min(int(screen_height * 0.022), 32))  # Entre 12 et 32px
        label_size = max(11, min(int(screen_height * 0.02), 28))  # Entre 11 et 28px
        button_size = max(11, min(int(screen_height * 0.02), 28))  # Entre 11 et 28px

        # Espacements adaptatifs
        title_pady = int(screen_height * 0.04)  # 4% de la hauteur
        subtitle_pady = int(screen_height * 0.015)  # 1.5% de la hauteur
        player_pady = int(screen_height * 0.02)  # 2% de la hauteur

        # Bouton retour en haut à gauche
        back_icon_btn = tk.Button(
            parent_frame,
            text="← MENU",
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
            text="🎮 SAISIE DES PSEUDOS",
            font=title_font,
            bg=config.COLOR_BG,
            fg=config.COLOR_TEXT
        )
        title.pack(pady=title_pady)

        # Sous-titre
        subtitle = tk.Label(
            parent_frame,
            text="Veuillez entrer les pseudos des joueurs",
            font=("Segoe UI", subtitle_size),
            bg=config.COLOR_BG,
            fg=config.COLOR_TEXT
        )
        subtitle.pack(pady=subtitle_pady)

        # Container principal
        input_container = tk.Frame(parent_frame, bg=config.COLOR_BG)
        input_container.pack(expand=True)

        # --- JOUEUR 1 ---
        player1_frame = tk.Frame(input_container, bg=config.COLOR_BG)
        player1_frame.pack(pady=player_pady)

        tk.Label(
            player1_frame,
            text="JOUEUR 1 (Rouge)",
            font=("Segoe UI", label_size, "bold"),
            bg=config.COLOR_BG,
            fg=config.COLOR_PLAYER1
        ).pack(pady=10)

        # Entry pour le pseudo du joueur 1
        self.pseudo1_entry = tk.Entry(
            player1_frame,
            font=("Segoe UI", label_size),
            width=25,
            justify=tk.CENTER,
            relief=tk.SOLID,
            bd=2
        )
        self.pseudo1_entry.pack(pady=10)
        self.pseudo1_entry.insert(0, "Joueur 1")  # Valeur par défaut

        # --- JOUEUR 2 ---
        player2_frame = tk.Frame(input_container, bg=config.COLOR_BG)
        player2_frame.pack(pady=player_pady)

        tk.Label(
            player2_frame,
            text="JOUEUR 2 (Orange)",
            font=("Segoe UI", label_size, "bold"),
            bg=config.COLOR_BG,
            fg=config.COLOR_PLAYER2
        ).pack(pady=10)

        # Entry pour le pseudo du joueur 2
        self.pseudo2_entry = tk.Entry(
            player2_frame,
            font=("Segoe UI", label_size),
            width=25,
            justify=tk.CENTER,
            relief=tk.SOLID,
            bd=2
        )
        self.pseudo2_entry.pack(pady=10)
        self.pseudo2_entry.insert(0, "Joueur 2")  # Valeur par défaut

        # Charger les derniers pseudos utilisés
        last_pseudo1, last_pseudo2 = database.get_last_pseudos()
        if last_pseudo1 and last_pseudo2:
            self.pseudo1_entry.delete(0, tk.END)
            self.pseudo1_entry.insert(0, last_pseudo1)
            self.pseudo2_entry.delete(0, tk.END)
            self.pseudo2_entry.insert(0, last_pseudo2)

        # Info sur le nombre de parties
        games_count = database.count_games()
        info_text = f"Nombre de parties jouées : {games_count}"
        info_size = max(8, min(int(label_size * 0.8), 14))  # Taille adaptative
        info_pady = int(screen_height * 0.015)  # 1.5% de la hauteur
        info_label = tk.Label(
            input_container,
            text=info_text,
            font=("Segoe UI", info_size),
            bg=config.COLOR_BG,
            fg="#FFFFFF"
        )
        info_label.pack(pady=info_pady)

        # Container pour les boutons
        button_container = tk.Frame(parent_frame, bg=config.COLOR_BG)
        button_bottom_pady = int(screen_height * 0.04)  # 4% de la hauteur
        button_container.pack(side=tk.BOTTOM, pady=button_bottom_pady)

        # Bouton Commencer
        btn_width = int(screen_width * 0.015)
        btn_height = int(screen_height * 0.003)

        start_btn = tk.Button(
            button_container,
            text="▶ COMMENCER LA PARTIE",
            command=self.validate_and_start,
            font=("Segoe UI", button_size, "bold"),
            bg=config.COLOR_BUTTON,
            fg="white",
            width=btn_width,
            height=btn_height,
            relief=tk.FLAT,
            cursor="hand2"
        )
        start_btn.pack()
        start_btn.bind("<Enter>", lambda e: start_btn.config(bg=config.COLOR_BUTTON_HOVER))
        start_btn.bind("<Leave>", lambda e: start_btn.config(bg=config.COLOR_BUTTON))

        # Focus sur le premier champ
        self.pseudo1_entry.focus()

        # Bind de la touche Entrée pour valider
        self.root.bind('<Return>', lambda e: self.validate_and_start())

    def validate_and_start(self):
        """Valide les pseudos et lance le jeu"""
        pseudo1 = self.pseudo1_entry.get().strip()
        pseudo2 = self.pseudo2_entry.get().strip()

        # Vérifier que les pseudos ne sont pas vides
        if not pseudo1 or not pseudo2:
            messagebox.showerror("Erreur", "Veuillez entrer un pseudo pour chaque joueur !")
            return

        # Vérifier que les pseudos sont différents
        if pseudo1.lower() == pseudo2.lower():
            messagebox.showerror("Erreur", "Les deux joueurs doivent avoir des pseudos différents !")
            return

        # Vérifier la longueur des pseudos
        if len(pseudo1) > 20 or len(pseudo2) > 20:
            messagebox.showerror("Erreur", "Les pseudos ne doivent pas dépasser 20 caractères !")
            return

        # Sauvegarder dans la base de données
        database.save_pseudos(pseudo1, pseudo2)

        # Unbind la touche Entrée
        self.root.unbind('<Return>')

        # Lancer le jeu avec les pseudos
        self.start_game_callback(pseudo1, pseudo2)
