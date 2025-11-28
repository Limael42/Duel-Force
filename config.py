# Configuration du jeu

# Dimensions
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

GAME_WIDTH = 1000
GAME_HEIGHT = 600

# Couleurs - Palette rouge et blanc (thème Street Fighter)
COLOR_BG = "#C41E3A"            # Rouge cardinal (moins agressif) - Fond principal
COLOR_BUTTON = "#8B0000"        # Rouge foncé - Boutons
COLOR_BUTTON_HOVER = "#B01030"  # Rouge moyen - Boutons au survol
COLOR_TEXT = "#FFFFFF"          # Blanc - Texte principal
COLOR_GAME_BG = "#FFF5F5"       # Rose très clair - Fond de jeu (doux pour les yeux)
COLOR_PLATFORM = "#335C81"      # Bleu mousse - Plateformes du jeu
COLOR_PLAYER1 = "#e74c3c"       # Rouge - Joueur 1
COLOR_PLAYER2 = "#f39c12"       # Orange - Joueur 2
COLOR_HEALTH_BAR = "#FFFFFF"    # Blanc - Barre de vie
COLOR_HEALTH_BG = "#8B0000"     # Rouge foncé - Fond de la barre de vie

# Paramètres des joueurs
PLAYER_WIDTH = 70
PLAYER_HEIGHT = 110
PLAYER_SPEED = 20
JUMP_FORCE = -24
GRAVITY = 1
MAX_JUMPS = 2

# Attaques
ATTACK_DAMAGE = 10
ATTACK_RANGE = 60
ATTACK_COOLDOWN = 300
SPECIAL_DAMAGE = 25
SPECIAL_COOLDOWN = 1800

# Projectiles
PROJECTILE_SPEED = 35
PROJECTILE_WIDTH = 12
PROJECTILE_HEIGHT = 12
PROJECTILE_COLOR_P1 = "#e74c3c"
PROJECTILE_COLOR_P2 = "#f39c12"

# Knockback
NORMAL_KNOCKBACK_FORCE = 8
SPECIAL_KNOCKBACK_BASE = 35
SPECIAL_KNOCKBACK_MAX_MULTIPLIER = 4.0

# Paramètres des plateformes
PLATFORM_COLOR = "#335C81"  # Bleu mousse - Plateformes du jeu
GROUND_HEIGHT = 550

# Points de vie
MAX_HEALTH = 100

# Contrôles - Chargés dynamiquement depuis keybindings.py
# Ces valeurs par défaut sont remplacées au démarrage
P1_CONTROLS = {
    'left': 'q',
    'right': 'd',
    'jump': 'z',
    'attack': 'a',
    'special': 'e'
}

P2_CONTROLS = {
    'left': 'Left',
    'right': 'Right',
    'jump': 'Up',
    'attack': 'space',
    'special': 'Return'
}

def load_controls():
    """Charge les contrôles personnalisés depuis keybindings.py"""
    try:
        import keybindings
        bindings = keybindings.load_keybindings()
        global P1_CONTROLS, P2_CONTROLS
        P1_CONTROLS = bindings['player1']
        P2_CONTROLS = bindings['player2']
    except Exception as e:
        print(f"Erreur lors du chargement des contrôles: {e}")

# Charger les contrôles au démarrage
load_controls()

# Paramètres
SETTINGS = {
    'difficulty': 'Normal',
    'sound': True,
    'music': True,
    'volume': 70
}
