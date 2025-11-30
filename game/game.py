"""
Classe Game - Gestion du jeu principal
Contient la boucle de jeu, l'affichage et la gestion des événements
"""

import tkinter as tk
from game.player import Player
from game.maps import AVAILABLE_MAPS
import config
import pygame
pygame.mixer.init()

class Game:
    """Classe principale gérant le déroulement du jeu"""

    def __init__(self, root, parent_frame, return_callback, pseudo1="Joueur 1", pseudo2="Joueur 2", total_rounds=1, map_id="classic"):
        """Initialise le jeu

        Args:
            root: Fenêtre Tkinter principale
            parent_frame: Frame parent
            return_callback: Fonction pour retourner au menu
            pseudo1: Pseudo du joueur 1
            pseudo2: Pseudo du joueur 2
            total_rounds: Nombre total de rounds à jouer
            map_id: ID de la map sélectionnée
        """
        # Recharger les contrôles personnalisés au début du jeu
        config.load_controls()

        self.root = root
        self.parent_frame = parent_frame
        self.return_callback = return_callback
        self.pseudo1 = pseudo1
        self.pseudo2 = pseudo2

        # Gestion des rounds
        self.total_rounds = total_rounds
        self.current_round = 1
        self.player1_wins = 0
        self.player2_wins = 0
        self.rounds_to_win = (total_rounds // 2) + 1  # Victoires nécessaires

        # Récupérer les dimensions de la fenêtre
        self.screen_width = root.winfo_width() if root.winfo_width() > 1 else 900
        self.screen_height = root.winfo_height() if root.winfo_height() > 1 else 900

        # Canvas de jeu adaptatif
        self.canvas = tk.Canvas(
            parent_frame,
            width=self.screen_width,
            height=self.screen_height,
            bg=config.COLOR_GAME_BG,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Charger la configuration de la map sélectionnée
        if map_id in AVAILABLE_MAPS:
            map_config = AVAILABLE_MAPS[map_id]
            self.platforms = map_config.platforms_func(self.screen_width, self.screen_height)
        else:
            # Map par défaut si l'ID n'existe pas
            self.platforms = AVAILABLE_MAPS["classic"].platforms_func(self.screen_width, self.screen_height)

        # Trouver la plateforme la plus basse (spawn platform)
        spawn_platform = self.find_spawn_platform()

        # Création des joueurs sur la plateforme de spawn
        # Joueur 1 (Rouge, ZQSD) à GAUCHE - 1/3 de la plateforme
        # Joueur 2 (Orange, Flèches) à DROITE - 2/3 de la plateforme
        plat_x, plat_y, plat_width, plat_height = spawn_platform
        player1_x = plat_x + int(plat_width * 0.33)  # Gauche
        player2_x = plat_x + int(plat_width * 0.67)  # Droite
        # Positionner les joueurs juste au-dessus de la plateforme
        player_spawn_y = plat_y - config.PLAYER_HEIGHT - 5

        self.player1 = Player(
            player1_x, player_spawn_y,
            config.COLOR_PLAYER1,
            config.P1_CONTROLS,
            1,
            self.screen_width
        )

        self.player2 = Player(
            player2_x, player_spawn_y,
            config.COLOR_PLAYER2,
            config.P2_CONTROLS,
            2,
            self.screen_width
        )

        # État du jeu
        self.game_over = False
        self.winner = None
        self.paused = False
        self.quit_confirmation = False  # Pour afficher la confirmation de sortie

        # Compte à rebours entre les rounds
        self.round_countdown = 0
        self.round_countdown_active = False
        self.last_countdown_update = 0

        # Liste des projectiles actifs
        self.projectiles = []

        # Touches pressées
        self.keys_pressed = set()

        # Unbind les événements globaux d'Echap pour éviter les conflits
        self.root.unbind('<Escape>')

        # Bind des événements clavier
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)

        # Lancer la boucle de jeu
        self.game_loop()

    def find_spawn_platform(self):
        """Trouve la plateforme de spawn (la plus basse et la plus large)

        Returns:
            tuple: (x, y, width, height) de la plateforme de spawn
        """
        if not self.platforms:
            # Fallback au cas où il n'y aurait aucune plateforme
            return (int(self.screen_width * 0.25), int(self.screen_height * 0.7),
                   int(self.screen_width * 0.5), 20)

        # Trouver la plateforme la plus basse (Y le plus grand)
        lowest_platforms = sorted(self.platforms, key=lambda p: p[1], reverse=True)

        # Parmi les plateformes basses, prendre la plus large
        # On considère les 3 plateformes les plus basses
        candidates = lowest_platforms[:min(3, len(lowest_platforms))]
        spawn_platform = max(candidates, key=lambda p: p[2])  # p[2] = width

        return spawn_platform

    def on_key_press(self, event):
        """Gère les touches pressées

        Args:
            event: Événement clavier
        """
        key = event.keysym
        self.keys_pressed.add(key)

        # Gestion de la confirmation de sortie
        if self.quit_confirmation:
            if key == "y" or key == "o":  # Oui en anglais ou français
                self.return_to_menu()
                return
            elif key == "n" or key == "Escape":  # Non ou annulation
                self.quit_confirmation = False
                self.paused = False
                return

        # Echap pour afficher la confirmation de sortie
        if key == "Escape" and not self.game_over:
            self.quit_confirmation = True
            self.paused = True
            return

        if not self.game_over and not self.paused:
            # Joueur 1
            if key == config.P1_CONTROLS['attack']:
                projectile = self.player1.attack()
                if projectile:
                    self.projectiles.append(projectile)
            elif key == config.P1_CONTROLS['special']:
                self.player1.special_attack(self.player2)

            # Joueur 2 (seulement si pas en mode bot)
            if key == config.P2_CONTROLS['attack']:
                projectile = self.player2.attack()
                if projectile:
                    self.projectiles.append(projectile)
            elif key == config.P2_CONTROLS['special']:
                self.player2.special_attack(self.player1)

    def on_key_release(self, event):
        """Gère les touches relâchées

        Args:
            event: Événement clavier
        """
        key = event.keysym
        self.keys_pressed.discard(key)

    def toggle_pause(self):
        """Met le jeu en pause ou le reprend"""
        self.paused = not self.paused

    def handle_continuous_input(self):
        """Gère les entrées continues (mouvement)"""
        if self.game_over or self.paused:
            return

        # Joueur 1
        if config.P1_CONTROLS['left'] in self.keys_pressed:
            self.player1.move_left()
        if config.P1_CONTROLS['right'] in self.keys_pressed:
            self.player1.move_right()
        if config.P1_CONTROLS['jump'] in self.keys_pressed:
            self.player1.jump()
            self.keys_pressed.discard(config.P1_CONTROLS['jump'])  # Éviter le saut continu

        # Joueur 2 (seulement si pas en mode bot)
        if config.P2_CONTROLS['left'] in self.keys_pressed:
            self.player2.move_left()
        if config.P2_CONTROLS['right'] in self.keys_pressed:
            self.player2.move_right()
        if config.P2_CONTROLS['jump'] in self.keys_pressed:
            self.player2.jump()
            self.keys_pressed.discard(config.P2_CONTROLS['jump'])

    def update(self):
        """Met à jour l'état du jeu"""
        # Gérer le compte à rebours entre les rounds
        if self.round_countdown_active:
            import time
            current_time = time.time()
            if current_time - self.last_countdown_update >= 1.0:
                self.last_countdown_update = current_time
                self.round_countdown -= 1
                if self.round_countdown <= 0:
                    self.round_countdown_active = False
                    self.paused = False
            return

        if self.game_over or self.paused:
            return

        # Gestion des entrées
        self.handle_continuous_input()

        # Mise à jour des joueurs (sans sol, mettre None)
        self.player1.update(self.platforms, None)
        self.player2.update(self.platforms, None)

        # Mise à jour des projectiles
        for projectile in self.projectiles[:]:
            projectile.update()

            # Vérifier collision avec les joueurs
            if projectile.owner == 1 and projectile.check_collision(self.player2):
                self.player2.take_damage(config.ATTACK_DAMAGE)
                self.player1.apply_normal_knockback(self.player2)
            elif projectile.owner == 2 and projectile.check_collision(self.player1):
                self.player1.take_damage(config.ATTACK_DAMAGE)
                self.player2.apply_normal_knockback(self.player1)

            # Retirer les projectiles inactifs
            if not projectile.active:
                self.projectiles.remove(projectile)

        # Vérifier les collisions entre les deux joueurs
        self.player1.check_collision_with_player(self.player2)

        # Vérifier si un joueur est tombé (mort par chute) - utiliser les dimensions d'écran
        if self.player1.y > self.screen_height:
            self.player1.health = 0  # Le joueur 1 est mort par chute
        if self.player2.y > self.screen_height:
            self.player2.health = 0  # Le joueur 2 est mort par chute

        # Vérifier si un joueur est mort
        if not self.player1.is_alive():
            self.handle_round_end(winner=2)
        elif not self.player2.is_alive():
            self.handle_round_end(winner=1)

    def draw(self):
        """Dessine tous les éléments du jeu"""
        # Effacer le canvas
        self.canvas.delete("all")

        # Dessiner un fond doux en rose très clair (pas agressif pour les yeux)
        self.canvas.create_rectangle(
            0, 0,
            self.screen_width, self.screen_height,
            fill=config.COLOR_GAME_BG,  # Rose très clair - doux pour les yeux
            outline=""
        )

        # Dessiner les plateformes avec un style épuré
        for platform in self.platforms:
            x, y, w, h = platform
            # Dessiner la plateforme principale
            self.canvas.create_rectangle(
                x, y, x + w, y + h,
                fill=config.PLATFORM_COLOR,
                outline=""
            )
            # Ajouter une ligne plus claire sur le dessus pour donner de la profondeur
            self.canvas.create_rectangle(
                x, y, x + w, y + 3,
                fill=config.COLOR_BUTTON_HOVER,
                outline=""
            )

        # Dessiner les joueurs
        self.draw_player(self.player1)
        self.draw_player(self.player2)

        # Dessiner les projectiles
        for projectile in self.projectiles:
            projectile.draw(self.canvas)

        # Dessiner l'interface (barres de vie, cooldowns)
        self.draw_ui()

        # Dessiner les messages (pause, game over)
        self.draw_messages()

    def draw_player(self, player):
        """Dessine un joueur avec effet visuel

        Args:
            player: Instance de Player à dessiner
        """
        x, y, w, h = player.get_rect()

        # Corps principal
        self.canvas.create_rectangle(
            x, y, x + w, y + h,
            fill=player.color,
            outline="black",
            width=2
        )

        # Tête
        head_size = w // 2
        head_x = x + w // 4
        head_y = y - head_size
        self.canvas.create_oval(
            head_x, head_y,
            head_x + head_size, head_y + head_size,
            fill=player.color,
            outline="black",
            width=2
        )

        # Indicateur de direction (flèche)
        if player.facing_right:
            arrow_x = x + w
            self.canvas.create_polygon(
                arrow_x, y + h // 2,
                arrow_x + 10, y + h // 2 - 5,
                arrow_x + 10, y + h // 2 + 5,
                fill="yellow",
                outline="black"
            )
        else:
            arrow_x = x
            self.canvas.create_polygon(
                arrow_x, y + h // 2,
                arrow_x - 10, y + h // 2 - 5,
                arrow_x - 10, y + h // 2 + 5,
                fill="yellow",
                outline="black"
            )

        # Effet d'attaque
        if player.is_attacking:
            attack_x = x + w + 10 if player.facing_right else x - 30
            self.canvas.create_oval(
                attack_x, y + h // 3,
                attack_x + 20, y + h // 3 + 20,
                fill="white",
                outline="orange",
                width=3
            )
            player.is_attacking = False

    def draw_ui(self):
        """Dessine l'interface utilisateur (barres de vie, cooldowns)"""
        # Positions adaptatives
        margin = int(self.screen_width * 0.03)
        top_margin = int(self.screen_height * 0.03)

        # Barre de vie Joueur 1 (avec pseudo)
        self.draw_health_bar(margin, top_margin, self.player1.health, self.pseudo1, config.COLOR_PLAYER1)

        # Barre de vie Joueur 2 (avec pseudo)
        p2_x = int(self.screen_width - margin - 200)
        self.draw_health_bar(p2_x, top_margin, self.player2.health, self.pseudo2, config.COLOR_PLAYER2)

        # Cooldowns Joueur 1
        self.draw_cooldowns(margin, top_margin + 40, self.player1)

        # Cooldowns Joueur 2
        self.draw_cooldowns(p2_x, top_margin + 40, self.player2)

        # Bouton retour au menu (en haut au centre)
        btn_width = 120
        btn_height = 30
        btn_x = self.screen_width // 2 - btn_width // 2
        btn_y = 10
        font_size = int(self.screen_height * 0.015)

        self.canvas.create_rectangle(
            btn_x, btn_y, btn_x + btn_width, btn_y + btn_height,
            fill=config.COLOR_BUTTON,
            outline=config.COLOR_BUTTON_HOVER,
            width=2,
            tags="menu_btn"
        )
        self.canvas.create_text(
            self.screen_width // 2, btn_y + 15,
            text="← MENU (Echap)",
            font=("Segoe UI", font_size, "bold"),
            fill="white",
            tags="menu_btn_text"
        )

        # Afficher le score des rounds si mode multi-rounds
        if self.total_rounds > 1:
            score_y = btn_y + btn_height + 15
            score_size = int(self.screen_height * 0.025)

            # Round actuel
            round_text = f"ROUND {self.current_round}/{self.total_rounds}"
            self.canvas.create_text(
                self.screen_width // 2, score_y,
                text=round_text,
                font=("Segoe UI", score_size, "bold"),
                fill=config.COLOR_HEALTH_BAR
            )

            # Score
            score_text = f"{self.pseudo1}: {self.player1_wins}  |  {self.pseudo2}: {self.player2_wins}"
            self.canvas.create_text(
                self.screen_width // 2, score_y + 30,
                text=score_text,
                font=("Segoe UI", int(score_size * 0.8), "bold"),
                fill="#8B0000"
            )

    def draw_health_bar(self, x, y, health, label, color):
        """Dessine une barre de vie

        Args:
            x: Position X
            y: Position Y
            health: Points de vie actuels
            label: Nom du joueur
            color: Couleur du joueur
        """
        bar_width = 200
        bar_height = 25

        # Fond de la barre
        self.canvas.create_rectangle(
            x, y, x + bar_width, y + bar_height,
            fill=config.COLOR_HEALTH_BG,
            outline="black",
            width=2
        )

        # Barre de vie actuelle
        current_width = (health / config.MAX_HEALTH) * bar_width
        self.canvas.create_rectangle(
            x, y, x + current_width, y + bar_height,
            fill=config.COLOR_HEALTH_BAR,
            outline=""
        )

        # Texte
        self.canvas.create_text(
            x + bar_width // 2, y + bar_height // 2,
            text=f"{label}: {int(health)} HP",
            font=("Segoe UI", 12, "bold"),
            fill="#8B0000"
        )

    def draw_cooldowns(self, x, y, player):
        """Dessine les indicateurs de cooldown

        Args:
            x: Position X
            y: Position Y
            player: Instance de Player
        """
        # Cooldown attaque normale
        attack_ready = player.attack_cooldown == 0
        attack_color = "green" if attack_ready else "red"
        self.canvas.create_rectangle(
            x, y, x + 90, y + 15,
            fill=attack_color,
            outline="black"
        )
        self.canvas.create_text(
            x + 45, y + 7,
            text="Attaque",
            font=("Segoe UI", 9, "bold"),
            fill="white"
        )

        # Cooldown attaque spéciale
        special_ready = player.special_cooldown == 0
        special_color = "green" if special_ready else "red"
        self.canvas.create_rectangle(
            x + 100, y, x + 200, y + 15,
            fill=special_color,
            outline="black"
        )
        self.canvas.create_text(
            x + 150, y + 7,
            text="Spécial",
            font=("Segoe UI", 9, "bold"),
            fill="white"
        )

    def draw_messages(self):
        """Dessine les messages (game over, countdown et confirmation de sortie)"""
        # Afficher la confirmation de sortie
        if self.quit_confirmation:
            center_x = self.screen_width // 2
            center_y = self.screen_height // 2

            # Boîte de dialogue
            box_width = int(self.screen_width * 0.5)
            box_height = int(self.screen_height * 0.3)

            self.canvas.create_rectangle(
                center_x - box_width // 2, center_y - box_height // 2,
                center_x + box_width // 2, center_y + box_height // 2,
                fill=config.COLOR_BG,
                outline=config.COLOR_HEALTH_BAR,
                width=4
            )

            # Titre
            title_size = int(self.screen_height * 0.04)
            self.canvas.create_text(
                center_x, center_y - 50,
                text="Êtes-vous sûr de vouloir quitter ?",
                font=("Segoe UI", title_size, "bold"),
                fill=config.COLOR_TEXT
            )

            # Instructions
            instruction_size = int(self.screen_height * 0.025)
            self.canvas.create_text(
                center_x, center_y + 10,
                text="O = Oui | N = Non",
                font=("Segoe UI", instruction_size),
                fill=config.COLOR_HEALTH_BAR
            )

            self.canvas.create_text(
                center_x, center_y + 45,
                text="(Échap pour annuler)",
                font=("Segoe UI", int(instruction_size * 0.8)),
                fill="#8B0000"
            )
            return

        # Afficher le compte à rebours entre les rounds
        if self.round_countdown_active and self.round_countdown > 0:
            center_x = self.screen_width // 2
            center_y = self.screen_height // 2

            # Message "Round X"
            round_text = f"ROUND {self.current_round}"
            round_size = int(self.screen_height * 0.05)
            self.canvas.create_text(
                center_x, center_y - 80,
                text=round_text,
                font=("Segoe UI", round_size, "bold"),
                fill=config.COLOR_TEXT
            )

            # Message "Préparez-vous"
            ready_size = int(self.screen_height * 0.03)
            self.canvas.create_text(
                center_x, center_y - 20,
                text="Préparez-vous !",
                font=("Segoe UI", ready_size),
                fill=config.COLOR_HEALTH_BAR
            )

            # Compte à rebours (grand et coloré)
            countdown_size = int(self.screen_height * 0.15)
            self.canvas.create_text(
                center_x, center_y + 60,
                text=str(self.round_countdown),
                font=("Segoe UI", countdown_size, "bold"),
                fill=config.COLOR_HEALTH_BAR
            )

        if self.game_over:
            # Afficher le pseudo du gagnant
            winner_pseudo = self.pseudo1 if self.winner == 1 else self.pseudo2
            winner_text = f"{winner_pseudo} GAGNE !"

            # Ajouter le score si mode multi-rounds
            if self.total_rounds > 1:
                winner_text += f"\n({self.player1_wins} - {self.player2_wins})"

            # Dimensions adaptatives
            box_width = int(self.screen_width * 0.4)
            box_height = int(self.screen_height * 0.3)
            center_x = self.screen_width // 2
            center_y = self.screen_height // 2

            title_size = int(self.screen_height * 0.06)
            subtitle_size = int(self.screen_height * 0.02)

            self.canvas.create_rectangle(
                center_x - box_width // 2, center_y - box_height // 2,
                center_x + box_width // 2, center_y + box_height // 2,
                fill=config.COLOR_BG,
                outline="gold",
                width=5
            )
            self.canvas.create_text(
                center_x, center_y - 30,
                text=winner_text,
                font=("Segoe UI", title_size, "bold"),
                fill="gold"
            )
            self.canvas.create_text(
                center_x, center_y + 30,
                text="Appuyez sur Echap pour retourner au menu",
                font=("Segoe UI", subtitle_size),
                fill=config.COLOR_TEXT
            )

            # Retour au menu si Echap est pressé
            if "Escape" in self.keys_pressed:
                self.return_to_menu()

    def handle_round_end(self, winner):
        """Gère la fin d'un round

        Args:
            winner: Numéro du joueur gagnant (1 ou 2)
        """
        # Incrémenter le score du gagnant
        if winner == 1:
            self.player1_wins += 1
        else:
            self.player2_wins += 1

        # Vérifier si un joueur a gagné le match
        if self.player1_wins >= self.rounds_to_win:
            self.game_over = True
            self.winner = 1
        elif self.player2_wins >= self.rounds_to_win:
            self.game_over = True
            self.winner = 2
        else:
            # Préparer le round suivant
            self.prepare_next_round()

    def prepare_next_round(self):
        """Prépare le round suivant avec un compte à rebours"""
        self.current_round += 1

        # Mettre le jeu en pause et démarrer le countdown
        import time
        self.paused = True
        self.round_countdown = 3
        self.round_countdown_active = True
        self.last_countdown_update = time.time()

        # Réinitialiser les projectiles
        self.projectiles = []

        # Réinitialiser les joueurs sur la plateforme de spawn
        spawn_platform = self.find_spawn_platform()
        plat_x, plat_y, plat_width, plat_height = spawn_platform
        player1_x = plat_x + int(plat_width * 0.33)
        player2_x = plat_x + int(plat_width * 0.67)
        player_spawn_y = plat_y - config.PLAYER_HEIGHT - 5

        self.player1.health = config.MAX_HEALTH
        self.player2.health = config.MAX_HEALTH
        self.player1.x = player1_x
        self.player1.y = player_spawn_y
        self.player2.x = player2_x
        self.player2.y = player_spawn_y
        self.player1.velocity_x = 0
        self.player1.velocity_y = 0
        self.player2.velocity_x = 0
        self.player2.velocity_y = 0
        self.player1.jumps_left = config.MAX_JUMPS
        self.player2.jumps_left = config.MAX_JUMPS

    def return_to_menu(self):
        """Retourne au menu principal"""
        self.root.unbind("<KeyPress>")
        self.root.unbind("<KeyRelease>")

        # Rebinder Echap pour quitter le plein écran
        self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))

        self.canvas.destroy()
        self.return_callback()

    def game_loop(self):
        """Boucle principale du jeu (60 FPS)"""
        self.update()
        self.draw()

        # Relancer la boucle (environ 60 FPS)
        self.root.after(16, self.game_loop)
