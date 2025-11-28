# Classe joueur

import config

class Player:
    def __init__(self, x, y, color, controls, player_id, screen_width=None):
        # Position et dimensions
        self.x = x
        self.y = y
        self.width = config.PLAYER_WIDTH
        self.height = config.PLAYER_HEIGHT
        self.screen_width = screen_width if screen_width else config.GAME_WIDTH

        # Physique
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.jump_count = 0

        # Combat
        self.health = config.MAX_HEALTH
        self.is_attacking = False
        self.attack_cooldown = 0
        self.special_cooldown = 0
        self.facing_right = True if player_id == 1 else False
        # Visuel
        self.color = color
        self.controls = controls
        self.player_id = player_id

        # État du mouvement
        self.moving_left = False
        self.moving_right = False

    def update(self, platforms, ground_height):
        # Application de la gravité
        if not self.on_ground:
            self.velocity_y += config.GRAVITY

        # Limitation de la vitesse de chute
        if self.velocity_y > 20:
            self.velocity_y = 20

        # Mise à jour de la position
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Vérification des limites horizontales (utilise screen_width)
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > self.screen_width:
            self.x = self.screen_width - self.width

        # Collision avec le sol
        self.on_ground = False
        if ground_height is not None:
            if self.y + self.height >= ground_height:
                self.y = ground_height - self.height
                self.velocity_y = 0
                self.on_ground = True
                self.jump_count = 0

        # Vérification collision avec les plateformes
        self.check_platform_collision(platforms)

        # Réduction des cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.special_cooldown > 0:
            self.special_cooldown -= 1

        # Friction
        self.velocity_x *= 0.85

    def check_platform_collision(self, platforms):
        for platform in platforms:
            px, py, pw, ph = platform

            # Vérifie si le joueur est sur la plateforme
            if (self.velocity_y >= 0 and
                self.x + self.width > px and
                self.x < px + pw and
                self.y + self.height > py and
                self.y + self.height < py + ph + 20):

                self.y = py - self.height
                self.velocity_y = 0
                self.on_ground = True
                self.jump_count = 0

    def move_left(self):
        self.velocity_x = -config.PLAYER_SPEED
        self.facing_right = False
        self.moving_left = True

    def move_right(self):
        self.velocity_x = config.PLAYER_SPEED
        self.facing_right = True
        self.moving_right = True

    def jump(self):
        # Double saut
        if self.jump_count < config.MAX_JUMPS:
            self.velocity_y = config.JUMP_FORCE
            self.on_ground = False
            self.jump_count += 1

    def attack(self):
        if self.attack_cooldown > 0:
            return None

        self.is_attacking = True
        self.attack_cooldown = config.ATTACK_COOLDOWN // 16

        # Position du projectile
        projectile_x = self.x + self.width // 2 if self.facing_right else self.x + self.width // 2
        projectile_y = self.y + self.height // 2

        direction = 1 if self.facing_right else -1
        from game.projectile import Projectile
        return Projectile(projectile_x, projectile_y, direction, self.player_id, self.screen_width)

    def apply_normal_knockback(self, other_player):
        # Recul
        knockback_force = config.NORMAL_KNOCKBACK_FORCE

        if self.facing_right:
            other_player.velocity_x = knockback_force
            other_player.velocity_y = -knockback_force * 0.5
        else:
            other_player.velocity_x = -knockback_force
            other_player.velocity_y = -knockback_force * 0.5

    def special_attack(self, other_player):
        # Attaque spéciale
        if self.special_cooldown > 0:
            return False

        self.is_attacking = True
        self.special_cooldown = config.SPECIAL_COOLDOWN // 16
        if self.check_attack_hit(other_player, config.ATTACK_RANGE * 1.5):
            other_player.take_damage(config.SPECIAL_DAMAGE)
            self.apply_smash_knockback(other_player)
            return True
        return False

    def apply_smash_knockback(self, other_player):
        # Propulsion basée sur les dégâts
        damage_percentage = (config.MAX_HEALTH - other_player.health) / config.MAX_HEALTH
        base_knockback = config.SPECIAL_KNOCKBACK_BASE
        damage_multiplier = 1 + (damage_percentage * (config.SPECIAL_KNOCKBACK_MAX_MULTIPLIER - 1))

        if self.facing_right:
            knockback_x = base_knockback * damage_multiplier
            knockback_y = -base_knockback * damage_multiplier * 0.8
        else:
            knockback_x = -base_knockback * damage_multiplier
            knockback_y = -base_knockback * damage_multiplier * 0.8
        other_player.velocity_x = knockback_x
        other_player.velocity_y = knockback_y
        other_player.on_ground = False

    def check_attack_hit(self, other_player, attack_range):
        distance = abs(self.x - other_player.x)
        if self.facing_right and other_player.x > self.x:
            return distance < attack_range
        elif not self.facing_right and other_player.x < self.x:
            return distance < attack_range

        return False

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

    def get_rect(self):
        return (self.x, self.y, self.width, self.height)

    def check_collision_with_player(self, other_player):
        x1, y1, w1, h1 = self.get_rect()
        x2, y2, w2, h2 = other_player.get_rect()
        if (x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            y1 + h1 > y2):
            overlap_x = min(x1 + w1, x2 + w2) - max(x1, x2)
            overlap_y = min(y1 + h1, y2 + h2) - max(y1, y2)
            if overlap_x < overlap_y:
                push_force = 8

                if x1 < x2:
                    self.velocity_x = -push_force
                    other_player.velocity_x = push_force
                else:
                    self.velocity_x = push_force
                    other_player.velocity_x = -push_force
            else:
                if y1 < y2:
                    other_player.y = y1 + h1
                    other_player.velocity_y = max(other_player.velocity_y, 0)
                else:
                    self.y = y2 + h2
                    self.velocity_y = max(self.velocity_y, 0)
