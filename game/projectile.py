# Projectiles

import config


class Projectile:
    def __init__(self, x, y, direction, owner, screen_width=None):
        self.x = x
        self.y = y
        self.direction = direction
        self.owner = owner
        self.active = True
        self.width = config.PROJECTILE_WIDTH
        self.height = config.PROJECTILE_HEIGHT
        self.speed = config.PROJECTILE_SPEED
        self.screen_width = screen_width if screen_width else config.GAME_WIDTH

    def update(self):
        if self.active:
            self.x += self.speed * self.direction
            if self.x < -50 or self.x > self.screen_width + 50:
                self.active = False

    def check_collision(self, player):
        if not self.active:
            return False
        if (self.x < player.x + player.width and
            self.x + self.width > player.x and
            self.y < player.y + player.height and
            self.y + self.height > player.y):
            self.active = False
            return True

        return False

    def draw(self, canvas):
        if self.active:
            color = config.PROJECTILE_COLOR_P1 if self.owner == 1 else config.PROJECTILE_COLOR_P2
            canvas.create_oval(
                self.x,
                self.y,
                self.x + self.width,
                self.y + self.height,
                fill=color,
                outline="white",
                width=2
            )
