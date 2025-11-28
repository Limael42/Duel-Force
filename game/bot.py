"""
Bot IA pour le jeu avec 3 niveaux de difficulté
Gère le comportement automatique d'un joueur contrôlé par l'ordinateur
"""

import random
import config


class Bot:
    """Classe représentant un bot IA avec différents niveaux de difficulté"""

    # Paramètres par niveau de difficulté
    DIFFICULTY_SETTINGS = {
        'facile': {
            'reaction_time': 15,  # Frames avant de réagir (lent)
            'accuracy': 0.4,      # 40% de précision dans les attaques
            'dodge_chance': 0.2,  # 20% de chance d'esquiver
            'jump_skill': 0.3,    # 30% de bons sauts
            'attack_frequency': 0.3,  # 30% de chance d'attaquer quand proche
            'special_usage': 0.1,  # 10% d'utilisation du spécial
            'error_rate': 0.4,    # 40% d'erreurs stratégiques
        },
        'moyen': {
            'reaction_time': 8,
            'accuracy': 0.65,
            'dodge_chance': 0.5,
            'jump_skill': 0.6,
            'attack_frequency': 0.6,
            'special_usage': 0.4,
            'error_rate': 0.2,
        },
        'difficile': {
            'reaction_time': 3,
            'accuracy': 0.9,
            'dodge_chance': 0.8,
            'jump_skill': 0.85,
            'attack_frequency': 0.85,
            'special_usage': 0.7,
            'error_rate': 0.05,
        }
    }

    def __init__(self, player, opponent, difficulty='moyen', platforms=None):
        """
        Initialise le bot

        Args:
            player: Instance du Player contrôlé par le bot
            opponent: Instance du Player adversaire
            difficulty: Niveau de difficulté ('facile', 'moyen', 'difficile')
            platforms: Liste des plateformes du jeu
        """
        self.player = player
        self.opponent = opponent
        self.difficulty = difficulty
        self.settings = self.DIFFICULTY_SETTINGS[difficulty]
        self.platforms = platforms or []

        # Variables de comportement
        self.reaction_counter = 0
        self.target_x = None
        self.last_action = None
        self.decision_cooldown = 0

    def update(self, projectiles):
        """
        Met à jour le comportement du bot

        Args:
            projectiles: Liste des projectiles actifs

        Returns:
            Projectile ou None si le bot a généré un projectile
        """
        # Cooldown de décision
        if self.decision_cooldown > 0:
            self.decision_cooldown -= 1
            return None

        # Temps de réaction
        self.reaction_counter += 1
        if self.reaction_counter < self.settings['reaction_time']:
            return None

        self.reaction_counter = 0

        # Décisions du bot
        return self._make_decision(projectiles)

    def _make_decision(self, projectiles):
        """Prend une décision stratégique

        Returns:
            Projectile ou None si le bot a généré un projectile
        """
        # Esquiver les projectiles en priorité
        if self._should_dodge_projectile(projectiles):
            self._dodge_projectile(projectiles)
            return None

        # Distance avec l'adversaire
        distance = abs(self.player.x - self.opponent.x)

        # Stratégie selon la distance
        if distance < 150:  # Combat rapproché
            return self._close_combat_strategy()
        elif distance < 400:  # Moyenne distance
            return self._mid_range_strategy()
        else:  # Longue distance
            return self._long_range_strategy()

    def _should_dodge_projectile(self, projectiles):
        """Vérifie si un projectile menace le bot"""
        for proj in projectiles:
            # Vérifier si le projectile appartient à l'adversaire
            if proj.owner != self.player.player_number:
                # Vérifier si le projectile se dirige vers le bot
                dist_x = abs(proj.x - self.player.x)
                dist_y = abs(proj.y - self.player.y)

                if dist_x < 200 and dist_y < 100:
                    # Appliquer la chance d'esquive
                    if random.random() < self.settings['dodge_chance']:
                        return True
        return False

    def _dodge_projectile(self, projectiles):
        """Esquive un projectile"""
        # Trouver le projectile le plus proche
        closest_proj = None
        min_dist = float('inf')

        for proj in projectiles:
            if proj.owner != self.player.player_number:
                dist = abs(proj.x - self.player.x)
                if dist < min_dist:
                    min_dist = dist
                    closest_proj = proj

        if closest_proj:
            # Sauter pour esquiver
            if random.random() < self.settings['jump_skill']:
                self.player.jump()
            # Ou se déplacer dans la direction opposée
            elif closest_proj.x < self.player.x:
                self.player.move_right()
            else:
                self.player.move_left()

    def _close_combat_strategy(self):
        """Stratégie de combat rapproché"""
        # Erreur stratégique possible
        if random.random() < self.settings['error_rate']:
            return self._random_action()

        # Utiliser l'attaque spéciale si disponible
        if (self.player.special_cooldown == 0 and
            random.random() < self.settings['special_usage']):
            self.player.special_attack(self.opponent)
            self.decision_cooldown = 20
            return None

        # Attaque normale
        if (self.player.attack_cooldown == 0 and
            random.random() < self.settings['attack_frequency']):
            # Viser avec une certaine précision
            if random.random() < self.settings['accuracy']:
                # S'orienter vers l'adversaire avant d'attaquer
                if self.opponent.x > self.player.x:
                    self.player.move_right()
                else:
                    self.player.move_left()
            projectile = self.player.attack()
            if projectile:
                self.decision_cooldown = 10
                return projectile

        # Se positionner
        if abs(self.player.x - self.opponent.x) > 80:
            if self.opponent.x > self.player.x:
                self.player.move_right()
            else:
                self.player.move_left()
        else:
            # Reculer parfois pour éviter l'attaque adverse
            if random.random() < 0.3:
                if self.opponent.x > self.player.x:
                    self.player.move_left()
                else:
                    self.player.move_right()

        return None

    def _mid_range_strategy(self):
        """Stratégie à moyenne distance"""
        if random.random() < self.settings['error_rate']:
            return self._random_action()

        # Attaquer à distance
        if (self.player.attack_cooldown == 0 and
            random.random() < self.settings['attack_frequency'] * 0.7):
            if random.random() < self.settings['accuracy']:
                projectile = self.player.attack()
                if projectile:
                    self.decision_cooldown = 15
                    return projectile

        # Se rapprocher de l'adversaire
        if self.opponent.x > self.player.x:
            self.player.move_right()
        else:
            self.player.move_left()

        # Sauts stratégiques sur les plateformes
        if random.random() < self.settings['jump_skill'] * 0.5:
            if self._should_jump_to_platform():
                self.player.jump()

        return None

    def _long_range_strategy(self):
        """Stratégie à longue distance"""
        # Se rapprocher rapidement
        if self.opponent.x > self.player.x:
            self.player.move_right()
        else:
            self.player.move_left()

        # Tirer occasionnellement
        if (self.player.attack_cooldown == 0 and
            random.random() < self.settings['attack_frequency'] * 0.4):
            projectile = self.player.attack()
            if projectile:
                return projectile

        # Navigation sur les plateformes
        if random.random() < self.settings['jump_skill'] * 0.3:
            if self._should_jump_to_platform():
                self.player.jump()

        return None

    def _should_jump_to_platform(self):
        """Détermine si le bot devrait sauter vers une plateforme"""
        # Logique simple : sauter si on est sous l'adversaire
        if self.player.y > self.opponent.y + 50:
            return True
        return False

    def _random_action(self):
        """Action aléatoire (pour simuler des erreurs)"""
        action = random.choice(['left', 'right', 'jump', 'attack', 'nothing'])

        if action == 'left':
            self.player.move_left()
        elif action == 'right':
            self.player.move_right()
        elif action == 'jump':
            self.player.jump()
        elif action == 'attack' and self.player.attack_cooldown == 0:
            return self.player.attack()

        return None

    def reset(self):
        """Réinitialise l'état du bot"""
        self.reaction_counter = 0
        self.target_x = None
        self.last_action = None
        self.decision_cooldown = 0
