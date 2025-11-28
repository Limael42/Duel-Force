"""
Page de configuration des touches
Permet aux joueurs de personnaliser leurs contrôles
"""

import tkinter as tk
from tkinter import font, messagebox
import config
import keybindings


class KeybindingsPage:
    """Classe gérant la page de configuration des touches"""

    def __init__(self, parent_frame, return_callback, screen_width=None, screen_height=None):
        """Initialise la page de configuration des touches

        Args:
            parent_frame: Frame parent
            return_callback: Fonction pour retourner aux paramètres
            screen_width: Largeur de l'écran
            screen_height: Hauteur de l'écran
        """
        self.parent_frame = parent_frame
        self.return_callback = return_callback

        if screen_width is None or screen_height is None:
            screen_width = parent_frame.winfo_width() if parent_frame.winfo_width() > 1 else 900
            screen_height = parent_frame.winfo_height() if parent_frame.winfo_height() > 1 else 900

        # Charger les touches actuelles
        self.keybindings = keybindings.load_keybindings()

        # Variable pour capturer une touche
        self.capturing = False
        self.capture_player = None
        self.capture_action = None
        self.capture_button = None

        # Polices adaptatives
        title_size = max(18, min(int(screen_height * 0.05), 60))
        section_size = max(14, min(int(screen_height * 0.03), 40))
        text_size = max(10, min(int(screen_height * 0.018), 24))
        button_size = max(11, min(int(screen_height * 0.02), 28))

        # Espacements
        header_pady = int(screen_height * 0.02)
        section_pady = int(screen_height * 0.025)

        # Header avec titre et bouton retour
        header_frame = tk.Frame(parent_frame, bg=config.COLOR_BG)
        header_frame.pack(fill=tk.X, pady=header_pady)

        back_btn = tk.Button(
            header_frame,
            text="← RETOUR",
            command=self.save_and_return,
            font=("Segoe UI", button_size, "bold"),
            bg=config.COLOR_BUTTON,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=int(screen_width * 0.01),
            pady=int(screen_height * 0.008)
        )
        back_btn.pack(side=tk.LEFT, padx=int(screen_width * 0.02))
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg=config.COLOR_BUTTON_HOVER))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg=config.COLOR_BUTTON))

        title = tk.Label(
            header_frame,
            text="⌨️ CONFIGURATION DES TOUCHES",
            font=("Segoe UI", title_size, "bold"),
            bg=config.COLOR_BG,
            fg=config.COLOR_TEXT
        )
        title.pack(side=tk.LEFT, expand=True)

        # Container principal avec scrollbar
        main_container = tk.Frame(parent_frame, bg=config.COLOR_BG)
        main_container.pack(fill=tk.BOTH, expand=True, padx=int(screen_width * 0.05))

        # Container pour les deux joueurs côte à côte
        players_container = tk.Frame(main_container, bg=config.COLOR_BG)
        players_container.pack(expand=True, pady=section_pady)

        # Joueur 1
        self.create_player_controls(
            players_container,
            "JOUEUR 1 (Rouge)",
            config.COLOR_PLAYER1,
            'player1',
            section_size,
            text_size,
            0
        )

        # Joueur 2
        self.create_player_controls(
            players_container,
            "JOUEUR 2 (Orange)",
            config.COLOR_PLAYER2,
            'player2',
            section_size,
            text_size,
            1
        )

        # Boutons d'action en bas
        actions_frame = tk.Frame(parent_frame, bg=config.COLOR_BG)
        actions_frame.pack(side=tk.BOTTOM, pady=int(screen_height * 0.03))

        reset_btn = tk.Button(
            actions_frame,
            text="🔄 RÉINITIALISER PAR DÉFAUT",
            command=self.reset_defaults,
            font=("Segoe UI", button_size, "bold"),
            bg="#1E3D59",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        )
        reset_btn.pack(side=tk.LEFT, padx=10)
        reset_btn.bind("<Enter>", lambda e: reset_btn.config(bg="#001F3F"))
        reset_btn.bind("<Leave>", lambda e: reset_btn.config(bg="#1E3D59"))

        save_btn = tk.Button(
            actions_frame,
            text="✓ APPLIQUER",
            command=self.save_and_return,
            font=("Segoe UI", button_size, "bold"),
            bg=config.COLOR_BUTTON,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        )
        save_btn.pack(side=tk.LEFT, padx=10)
        save_btn.bind("<Enter>", lambda e: save_btn.config(bg=config.COLOR_BUTTON_HOVER))
        save_btn.bind("<Leave>", lambda e: save_btn.config(bg=config.COLOR_BUTTON))

        # Instructions en bas
        instruction = tk.Label(
            parent_frame,
            text="Cliquez sur un bouton et appuyez sur la touche désirée pour la configurer",
            font=("Segoe UI", max(8, min(int(text_size * 0.8), 14)), "italic"),
            bg=config.COLOR_BG,
            fg="#7EA8BE"
        )
        instruction.pack(side=tk.BOTTOM, pady=int(screen_height * 0.005))

        # Avertissement sur la temporalité
        temp_warning = tk.Label(
            parent_frame,
            text="⚠️ Les modifications sont temporaires et valides uniquement pour cette session",
            font=("Segoe UI", max(8, min(int(text_size * 0.75), 13)), "italic"),
            bg=config.COLOR_BG,
            fg="#f39c12"  # Orange pour attirer l'attention
        )
        temp_warning.pack(side=tk.BOTTOM, pady=int(screen_height * 0.005))

        # Stocker les boutons pour mise à jour
        self.key_buttons = {}

        # Bind clavier global pour capture
        self.parent_frame.master.bind("<KeyPress>", self.on_key_capture)

    def create_player_controls(self, parent, title, color, player_key, section_size, text_size, column):
        """Crée les contrôles pour un joueur

        Args:
            parent: Widget parent
            title: Titre du joueur
            color: Couleur du joueur
            player_key: Clé du joueur ('player1' ou 'player2')
            section_size: Taille de police section
            text_size: Taille de police texte
            column: Colonne dans le grid
        """
        player_frame = tk.Frame(parent, bg=config.COLOR_BG)
        player_frame.grid(row=0, column=column, padx=30, pady=10, sticky="n")

        # Titre du joueur
        tk.Label(
            player_frame,
            text=title,
            font=("Segoe UI", section_size, "bold"),
            bg=config.COLOR_BG,
            fg=color
        ).pack(pady=15)

        # Créer un bouton pour chaque action
        for action in ['left', 'right', 'jump', 'attack', 'special']:
            action_frame = tk.Frame(player_frame, bg=config.COLOR_BG)
            action_frame.pack(pady=8, fill=tk.X)

            # Label de l'action
            action_label = tk.Label(
                action_frame,
                text=keybindings.ACTION_NAMES[action] + " :",
                font=("Segoe UI", text_size),
                bg=config.COLOR_BG,
                fg=config.COLOR_TEXT,
                width=20,
                anchor="w"
            )
            action_label.pack(side=tk.LEFT, padx=5)

            # Bouton de la touche
            key = self.keybindings[player_key][action]
            key_btn = tk.Button(
                action_frame,
                text=keybindings.get_key_display_name(key),
                command=lambda p=player_key, a=action: self.start_capture(p, a),
                font=("Segoe UI", text_size, "bold"),
                bg=config.COLOR_PLATFORM,
                fg="white",
                relief=tk.FLAT,
                cursor="hand2",
                width=15,
                padx=10,
                pady=5
            )
            key_btn.pack(side=tk.LEFT, padx=5)
            key_btn.bind("<Enter>", lambda e, b=key_btn: b.config(bg=config.COLOR_BUTTON))
            key_btn.bind("<Leave>", lambda e, b=key_btn: b.config(bg=config.COLOR_PLATFORM))

            # Stocker le bouton pour mise à jour
            self.key_buttons[(player_key, action)] = key_btn

    def start_capture(self, player, action):
        """Commence la capture d'une touche

        Args:
            player: Joueur ('player1' ou 'player2')
            action: Action à configurer
        """
        self.capturing = True
        self.capture_player = player
        self.capture_action = action
        self.capture_button = self.key_buttons[(player, action)]

        # Changer l'apparence du bouton
        self.capture_button.config(
            text="Appuyez sur une touche...",
            bg="#7EA8BE"
        )

    def on_key_capture(self, event):
        """Gère la capture d'une touche

        Args:
            event: Événement clavier
        """
        if not self.capturing:
            return

        key = event.keysym

        # Vérifier si la touche est interdite
        if key in keybindings.get_forbidden_keys():
            messagebox.showwarning(
                "Touche interdite",
                f"La touche '{keybindings.get_key_display_name(key)}' est réservée et ne peut pas être utilisée."
            )
            self.cancel_capture()
            return

        # Vérifier les conflits
        has_conflict, conflict_action, conflict_player = keybindings.check_key_conflict(
            self.keybindings,
            self.capture_player,
            self.capture_action,
            key
        )

        if has_conflict:
            response = messagebox.askyesno(
                "Conflit de touche",
                f"La touche '{keybindings.get_key_display_name(key)}' est déjà utilisée pour "
                f"'{keybindings.ACTION_NAMES[conflict_action]}'.\n\n"
                f"Voulez-vous l'échanger ?"
            )

            if response:
                # Échanger les touches
                old_key = self.keybindings[self.capture_player][self.capture_action]
                self.keybindings[conflict_player][conflict_action] = old_key
                self.keybindings[self.capture_player][self.capture_action] = key

                # Mettre à jour les deux boutons
                self.key_buttons[(conflict_player, conflict_action)].config(
                    text=keybindings.get_key_display_name(old_key)
                )
                self.key_buttons[(self.capture_player, self.capture_action)].config(
                    text=keybindings.get_key_display_name(key),
                    bg=config.COLOR_PLATFORM
                )
            else:
                self.cancel_capture()
                return
        else:
            # Pas de conflit, assigner la touche
            self.keybindings[self.capture_player][self.capture_action] = key
            self.capture_button.config(
                text=keybindings.get_key_display_name(key),
                bg=config.COLOR_PLATFORM
            )

        # Terminer la capture
        self.capturing = False
        self.capture_player = None
        self.capture_action = None
        self.capture_button = None

    def cancel_capture(self):
        """Annule la capture en cours"""
        if self.capture_button:
            old_key = self.keybindings[self.capture_player][self.capture_action]
            self.capture_button.config(
                text=keybindings.get_key_display_name(old_key),
                bg=config.COLOR_PLATFORM
            )

        self.capturing = False
        self.capture_player = None
        self.capture_action = None
        self.capture_button = None

    def reset_defaults(self):
        """Réinitialise les touches par défaut"""
        response = messagebox.askyesno(
            "Réinitialiser",
            "Voulez-vous vraiment réinitialiser toutes les touches aux valeurs par défaut ?"
        )

        if response:
            self.keybindings = keybindings.reset_to_defaults()

            # Mettre à jour tous les boutons
            for (player, action), button in self.key_buttons.items():
                key = self.keybindings[player][action]
                button.config(text=keybindings.get_key_display_name(key))

            messagebox.showinfo("Réinitialisation", "Les touches ont été réinitialisées aux valeurs par défaut.")

    def save_and_return(self):
        """Applique les touches pour la session en cours et retourne aux paramètres"""
        # Annuler toute capture en cours
        if self.capturing:
            self.cancel_capture()

        # Appliquer les touches pour la session (stockage temporaire en mémoire)
        keybindings.save_keybindings(self.keybindings)

        # Recharger les contrôles dans config pour les appliquer immédiatement
        config.load_controls()

        messagebox.showinfo(
            "Touches appliquées",
            "Les nouvelles touches sont actives pour cette session !\n\n"
            "⚠️ Rappel : Ces modifications seront perdues à la fermeture de l'application."
        )

        # Unbind l'événement clavier
        self.parent_frame.master.unbind("<KeyPress>")

        # Retourner aux paramètres
        self.return_callback()
