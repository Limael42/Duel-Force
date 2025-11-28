"""
Menu principal de l'application
Contient les pages : Jouer, Paramètres, Quitter
"""

import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
from ui.settings_page import SettingsPage
from ui.pseudo_page import PseudoPage
from ui.rounds_page import RoundsPage
from ui.map_selection_page import MapSelectionPage
from ui.countdown_page import CountdownPage
from game.game import Game
import config


class MainMenu:
    """Classe gérant le menu principal avec navigation entre pages"""

    def __init__(self, root):
        """Initialise le menu principal

        Args:
            root: Fenêtre Tkinter principale
        """
        self.root = root
        self.root.configure(bg=config.COLOR_BG)

        # Frame principal
        self.main_frame = tk.Frame(root, bg=config.COLOR_BG)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Forcer la mise à jour pour obtenir les vraies dimensions
        self.root.update_idletasks()

        # Stocker les dimensions de référence (une seule fois)
        self.screen_width = self.root.winfo_width()
        self.screen_height = self.root.winfo_height()

        # Variable pour arrêter l'animation GIF proprement
        self.gif_animation_id = None

        self.show_menu()

    def clear_frame(self):
        """Efface tous les widgets du frame principal"""
        # Arrêter l'animation GIF si elle existe
        if self.gif_animation_id is not None:
            self.root.after_cancel(self.gif_animation_id)
            self.gif_animation_id = None

        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def get_bg_portion(self, x, y, width, height):
        """Extrait une portion de l'image de fond pour un widget

        Args:
            x: Position X du centre du widget
            y: Position Y du centre du widget
            width: Largeur du widget
            height: Hauteur du widget

        Returns:
            PhotoImage de la portion de fond ou None
        """
        if not self.bg_image:
            return None

        try:
            # Calculer les coordonnées de la zone à extraire
            left = max(0, int(x - width // 2))
            top = max(0, int(y - height // 2))
            right = min(self.bg_image.width, int(x + width // 2))
            bottom = min(self.bg_image.height, int(y + height // 2))

            # Extraire la portion
            portion = self.bg_image.crop((left, top, right, bottom))
            return ImageTk.PhotoImage(portion)
        except Exception as e:
            print(f"Erreur extraction fond: {e}")
            return None

    def show_menu(self):
        """Affiche le menu principal avec les 3 options"""
        self.clear_frame()

        # Utiliser les dimensions stockées (constantes)
        screen_width = self.screen_width
        screen_height = self.screen_height

        # Configurer le fond avec un dégradé rouge et blanc
        self.main_frame.configure(bg="#DC143C")  # Rouge crimson

        # Créer un canvas pour le dégradé
        canvas = tk.Canvas(
            self.main_frame,
            width=screen_width,
            height=screen_height,
            highlightthickness=0
        )
        canvas.pack(fill=tk.BOTH, expand=True)

        # Créer un dégradé du haut vers le bas (blanc vers rouge)
        for i in range(screen_height):
            # Interpolation linéaire du blanc (#FFFFFF) vers le rouge (#DC143C)
            ratio = i / screen_height
            r = int(255 - (255 - 220) * ratio)
            g = int(255 - (255 - 20) * ratio)
            b = int(255 - (255 - 60) * ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, screen_width, i, fill=color)

        # Calculs adaptatifs basés sur la taille de l'écran
        title_size = max(18, min(int(screen_height * 0.05), 60))
        button_size = max(10, min(int(screen_height * 0.02), 28))

        title_font = font.Font(family="Segoe UI", size=title_size, weight="bold")
        button_font = font.Font(family="Segoe UI", size=button_size, weight="bold")

        # Espacement adaptatif
        title_pady = int(screen_height * 0.03)

        # Titre du jeu avec ombre pour le contraste
        title_y = int(screen_height * 0.08)
        # Ombre du titre
        canvas.create_text(
            screen_width // 2 + 3,
            title_y + 3,
            text="Duel Force",
            font=title_font,
            fill="#000000",
            anchor="center"
        )
        # Titre principal
        canvas.create_text(
            screen_width // 2,
            title_y,
            text="Duel Force",
            font=title_font,
            fill="#FFFFFF",
            anchor="center"
        )

        # Container pour les boutons (ligne horizontale)
        button_container = tk.Frame(canvas, bg="#DC143C", highlightthickness=0)
        canvas.create_window(screen_width // 2, int(screen_height * 0.3), window=button_container, anchor="center")

        # Espacement adaptatif pour les boutons
        btn_padx = int(screen_width * 0.015)  # 1.5% de la largeur
        btn_pady = int(screen_height * 0.015)  # 1.5% de la hauteur

        # Bouton JOUER - Rouge vif
        play_frame = self.create_button_with_icon(
            button_container,
            "▶ JOUER",
            self.start_game,
            "#DC143C",  # Rouge crimson
            button_font
        )
        play_frame.grid(row=0, column=0, padx=btn_padx, pady=btn_pady)

        # Bouton PARAMÈTRES - Blanc
        settings_frame = self.create_button_with_icon(
            button_container,
            "⚙ PARAMÈTRES",
            self.show_settings,
            "#FFFFFF",  # Blanc
            button_font,
            text_color="#DC143C"  # Texte rouge
        )
        settings_frame.grid(row=0, column=1, padx=btn_padx, pady=btn_pady)

        # Bouton QUITTER - Rouge foncé
        quit_frame = self.create_button_with_icon(
            button_container,
            "✕ QUITTER",
            self.quit_game,
            "#8B0000",  # Rouge foncé
            button_font
        )
        quit_frame.grid(row=0, column=2, padx=btn_padx, pady=btn_pady)


        # Centrage des boutons horizontalement
        button_container.grid_columnconfigure((0, 1, 2), weight=1)

        # Ajout du GIF animé sous les boutons
        self.add_gif_animation(canvas)

        # Crédits en bas
        credit_size = max(7, min(int(screen_height * 0.012), 14))
        credit_y = int(screen_height * 0.96)
        # Ombre des crédits
        canvas.create_text(
            screen_width // 2 + 2,
            credit_y + 2,
            text="Crédit: Kylian SEGOND et Emilien NEPVEU",
            font=("Segoe UI", credit_size),
            fill="#000000",
            anchor="center"
        )
        # Crédits principaux
        canvas.create_text(
            screen_width // 2,
            credit_y,
            text="Crédit: Kylian SEGOND et Emilien NEPVEU",
            font=("Segoe UI", credit_size),
            fill="#FFFFFF",
            anchor="center"
        )

    def create_button_with_icon(self, parent, text, command, color, font_style, text_color="white"):
        """Crée un bouton élégant avec effet hover"""
        frame = tk.Frame(parent, bg="#DC143C")

        # Utiliser les dimensions stockées (constantes) - Tailles réduites
        screen_width = self.screen_width
        screen_height = self.screen_height
        btn_width = int(screen_width * 0.012)  # Réduit: Largeur relative
        btn_height = int(screen_height * 0.003)  # Réduit: Hauteur relative

        button = tk.Button(
            frame,
            text=text,
            command=command,
            font=font_style,
            bg=color,
            fg=text_color,
            width=btn_width,
            height=btn_height,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=self.darken_color(color),
            activeforeground=text_color,
        )
        button.pack()

        # Effet hover
        button.bind("<Enter>", lambda e: button.config(bg=self.darken_color(color)))
        button.bind("<Leave>", lambda e: button.config(bg=color))

        return frame

    def darken_color(self, color):
        """Assombrit une couleur pour l'effet hover"""
        dark_colors = {
            "#DC143C": "#B01030",  # Rouge crimson plus foncé
            "#FFFFFF": "#F0F0F0",  # Blanc légèrement grisé
            "#8B0000": "#6B0000",  # Rouge foncé encore plus foncé
        }
        return dark_colors.get(color, color)

    def add_gif_animation(self, canvas):
        """Ajoute et anime un GIF sous les boutons sur le canvas"""
        frames = []
        i = 0

        # Calculer le zoom adaptatif en fonction de la taille de l'écran
        base_height = 1080
        zoom_factor = max(2, min(int((self.screen_height / base_height) * 3), 5))

        try:
            while True:
                # Agrandir le GIF avec un zoom adaptatif
                frame = tk.PhotoImage(file="street.gif", format=f"gif -index {i}").zoom(zoom_factor, zoom_factor)
                frames.append(frame)
                i += 1
        except Exception:
            pass  # Fin du chargement

        if frames:
            # Créer un label pour le GIF et le placer sur le canvas
            gif_frame = tk.Frame(canvas, bg="#DC143C", highlightthickness=0)
            gif_label = tk.Label(gif_frame, bg="#DC143C", highlightthickness=0)
            gif_label.pack()

            # Positionner le GIF sur le canvas
            canvas.create_window(
                self.screen_width // 2,
                int(self.screen_height * 0.65),
                window=gif_frame,
                anchor="center"
            )

            def animate(index):
                if gif_label.winfo_exists():  # Vérifier que le widget existe encore
                    frame = frames[index]
                    gif_label.configure(image=frame)
                    # Stocker l'ID de l'animation pour pouvoir l'arrêter
                    self.gif_animation_id = self.root.after(200, animate, (index + 1) % len(frames))

            animate(0)

    def start_game(self):
        """Affiche la page de saisie des pseudos"""
        self.clear_frame()
        PseudoPage(self.root, self.main_frame, self.show_menu, self.show_rounds_selection,
                   self.screen_width, self.screen_height)

    def show_rounds_selection(self, pseudo1, pseudo2):
        """Affiche la page de sélection du nombre de rounds

        Args:
            pseudo1: Pseudo du joueur 1
            pseudo2: Pseudo du joueur 2
        """
        self.clear_frame()
        RoundsPage(self.root, self.main_frame, self.show_menu, self.show_map_selection,
                   pseudo1, pseudo2, self.screen_width, self.screen_height)

    def show_map_selection(self, pseudo1, pseudo2, rounds):
        """Affiche la page de sélection de map

        Args:
            pseudo1: Pseudo du joueur 1
            pseudo2: Pseudo du joueur 2
            rounds: Nombre de rounds
        """
        self.clear_frame()
        MapSelectionPage(self.root, self.main_frame, self.show_menu, self.show_countdown,
                        pseudo1, pseudo2, rounds, self.screen_width, self.screen_height)

    def show_countdown(self, pseudo1, pseudo2, rounds, map_id):
        """Affiche le compte à rebours avant de lancer le jeu

        Args:
            pseudo1: Pseudo du joueur 1
            pseudo2: Pseudo du joueur 2
            rounds: Nombre de rounds
            map_id: ID de la map sélectionnée
        """
        self.clear_frame()
        CountdownPage(self.root, self.main_frame, self.launch_game,
                     pseudo1, pseudo2, rounds, map_id)

    def launch_game(self, pseudo1, pseudo2, rounds=1, map_id="classic"):
        """Lance le jeu avec les pseudos des joueurs, le nombre de rounds et la map

        Args:
            pseudo1: Pseudo du joueur 1
            pseudo2: Pseudo du joueur 2
            rounds: Nombre de rounds à jouer (par défaut 1)
            map_id: ID de la map sélectionnée (par défaut "classic")
        """
        self.clear_frame()
        Game(self.root, self.main_frame, self.show_menu, pseudo1, pseudo2, rounds, map_id)

    def show_settings(self):
        """Affiche la page des paramètres"""
        self.clear_frame()
        SettingsPage(self.main_frame, self.show_menu, self.screen_width, self.screen_height)

    def quit_game(self):
        """Quitte l'application"""
        self.root.quit()
