"""
Page de compte à rebours avant le début de la partie
"""

import tkinter as tk
import config


class CountdownPage:
    """Page affichant le compte à rebours de 3 secondes"""

    def __init__(self, root, parent_frame, start_game_callback,
                 pseudo1, pseudo2, rounds, map_id):
        """
        Args:
            root: Fenêtre Tkinter principale
            parent_frame: Frame parent
            start_game_callback: Fonction pour lancer le jeu
            pseudo1: Pseudo du joueur 1
            pseudo2: Pseudo du joueur 2
            rounds: Nombre de rounds
            map_id: ID de la map sélectionnée
        """
        self.root = root
        self.parent_frame = parent_frame
        self.start_game_callback = start_game_callback
        self.pseudo1 = pseudo1
        self.pseudo2 = pseudo2
        self.rounds = rounds
        self.map_id = map_id

        # Nettoyer le parent_frame
        for widget in parent_frame.winfo_children():
            widget.destroy()

        # Obtenir les dimensions
        screen_width = root.winfo_width() if root.winfo_width() > 1 else 900
        screen_height = root.winfo_height() if root.winfo_height() > 1 else 900

        # Texte "Bonne partie"
        good_luck_size = max(20, min(int(screen_height * 0.06), 80))
        good_luck_label = tk.Label(
            parent_frame,
            text="Bonne partie !",
            font=("Segoe UI", good_luck_size, "bold"),
            bg=config.COLOR_BG,
            fg=config.COLOR_TEXT
        )
        good_luck_label.pack(expand=True)

        # Label pour le compte à rebours
        countdown_size = max(40, min(int(screen_height * 0.15), 150))
        countdown_label = tk.Label(
            parent_frame,
            text="3",
            font=("Segoe UI", countdown_size, "bold"),
            bg=config.COLOR_BG,
            fg=config.COLOR_HEALTH_BAR
        )
        countdown_label.pack(expand=True)

        # Fonction pour mettre à jour le compte à rebours
        def update_countdown(count):
            if count > 0:
                countdown_label.config(text=str(count))
                root.after(1000, update_countdown, count - 1)
            else:
                # Lancer le jeu après le compte à rebours
                start_game_callback(pseudo1, pseudo2, rounds, map_id)

        # Démarrer le compte à rebours
        update_countdown(3)
