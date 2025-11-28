"""
Configurations des différentes maps du jeu
Chaque map contient une disposition unique de plateformes
"""

class MapConfig:
    """Classe représentant une configuration de map"""

    def __init__(self, name, description, ascii_preview, platforms_func):
        """
        Args:
            name: Nom de la map
            description: Description courte
            ascii_preview: Prévisualisation ASCII de la map
            platforms_func: Fonction qui génère les plateformes selon la taille d'écran
        """
        self.name = name
        self.description = description
        self.ascii_preview = ascii_preview
        self.platforms_func = platforms_func


def classic_map(screen_width, screen_height):
    """Map Classique - Style Super Smash Bros pyramidal"""
    # Marges de sécurité pour que tout reste visible
    margin_top = int(screen_height * 0.15)
    margin_bottom = int(screen_height * 0.85)

    main_platform_width = int(screen_width * 0.5)
    main_platform_x = int(screen_width * 0.25)
    main_platform_y = int(screen_height * 0.75)

    small_platform_width = int(screen_width * 0.1)
    left_small_x = int(screen_width * 0.22)
    right_small_x = int(screen_width * 0.68)
    middle_platform_y = int(screen_height * 0.55)

    medium_platform_width = int(screen_width * 0.12)
    left_medium_x = int(screen_width * 0.18)
    right_medium_x = int(screen_width * 0.7)
    high_platform_y = int(screen_height * 0.35)

    top_platform_width = int(screen_width * 0.2)
    top_platform_x = int(screen_width * 0.4)
    top_platform_y = max(margin_top, int(screen_height * 0.2))

    return [
        (main_platform_x, main_platform_y, main_platform_width, 15),
        (left_small_x, middle_platform_y, small_platform_width, 15),
        (right_small_x, middle_platform_y, small_platform_width, 15),
        (left_medium_x, high_platform_y, medium_platform_width, 15),
        (right_medium_x, high_platform_y, medium_platform_width, 15),
        (top_platform_x, top_platform_y, top_platform_width, 15)
    ]


def battlefield_map(screen_width, screen_height):
    """Map Battlefield - 3 plateformes équilibrées"""
    # Grande plateforme principale
    main_width = int(screen_width * 0.6)
    main_x = int(screen_width * 0.2)
    main_y = int(screen_height * 0.75)

    # Trois plateformes aériennes alignées
    platform_width = int(screen_width * 0.15)
    left_x = int(screen_width * 0.15)
    center_x = int(screen_width * 0.425)
    right_x = int(screen_width * 0.7)
    platform_y = int(screen_height * 0.5)

    return [
        (main_x, main_y, main_width, 15),
        (left_x, platform_y, platform_width, 15),
        (center_x, platform_y, platform_width, 15),
        (right_x, platform_y, platform_width, 15)
    ]


def final_destination_map(screen_width, screen_height):
    """Map Final Destination - Une seule grande plateforme plate"""
    platform_width = int(screen_width * 0.7)
    platform_x = int(screen_width * 0.15)
    platform_y = int(screen_height * 0.65)

    return [
        (platform_x, platform_y, platform_width, 15)
    ]


def towers_map(screen_width, screen_height):
    """Map Tours - Deux tours symétriques"""
    # Plateforme centrale basse
    center_width = int(screen_width * 0.3)
    center_x = int(screen_width * 0.35)
    center_y = int(screen_height * 0.78)

    # Tours gauche
    left_base_width = int(screen_width * 0.15)
    left_x = int(screen_width * 0.1)
    left_low_y = int(screen_height * 0.65)
    left_mid_y = int(screen_height * 0.5)
    left_high_y = int(screen_height * 0.35)

    # Tours droite
    right_x = int(screen_width * 0.75)

    return [
        (center_x, center_y, center_width, 15),
        (left_x, left_low_y, left_base_width, 15),
        (left_x, left_mid_y, left_base_width, 15),
        (left_x, left_high_y, left_base_width, 15),
        (right_x, left_low_y, left_base_width, 15),
        (right_x, left_mid_y, left_base_width, 15),
        (right_x, left_high_y, left_base_width, 15)
    ]


def arena_map(screen_width, screen_height):
    """Map Arène - Grande plateforme centrale avec coins"""
    # Plateforme centrale
    center_width = int(screen_width * 0.4)
    center_x = int(screen_width * 0.3)
    center_y = int(screen_height * 0.65)

    # Coins supérieurs
    corner_width = int(screen_width * 0.12)
    left_corner_x = int(screen_width * 0.08)
    right_corner_x = int(screen_width * 0.8)
    corner_y = int(screen_height * 0.3)

    # Plateformes latérales moyennes
    mid_y = int(screen_height * 0.48)

    return [
        (center_x, center_y, center_width, 15),
        (left_corner_x, corner_y, corner_width, 15),
        (right_corner_x, corner_y, corner_width, 15),
        (left_corner_x, mid_y, corner_width, 15),
        (right_corner_x, mid_y, corner_width, 15)
    ]


def chaos_map(screen_width, screen_height):
    """Map Chaos - Plateformes dispersées aléatoirement"""
    small_width = int(screen_width * 0.08)
    medium_width = int(screen_width * 0.12)
    large_width = int(screen_width * 0.18)

    return [
        # Base
        (int(screen_width * 0.4), int(screen_height * 0.75), large_width, 15),

        # Niveau bas - dispersé
        (int(screen_width * 0.15), int(screen_height * 0.65), small_width, 15),
        (int(screen_width * 0.75), int(screen_height * 0.65), small_width, 15),

        # Niveau moyen - décalé
        (int(screen_width * 0.25), int(screen_height * 0.52), medium_width, 15),
        (int(screen_width * 0.6), int(screen_height * 0.57), small_width, 15),

        # Niveau haut - asymétrique
        (int(screen_width * 0.1), int(screen_height * 0.4), medium_width, 15),
        (int(screen_width * 0.7), int(screen_height * 0.35), small_width, 15),

        # Sommet
        (int(screen_width * 0.45), int(screen_height * 0.22), medium_width, 15)
    ]


# ASCII Previews
CLASSIC_ASCII = """
        ▄▄▄▄▄
      ▄▄▄  ▄▄▄
    ▄▄▄      ▄▄▄
  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
"""

BATTLEFIELD_ASCII = """
  ▄▄▄  ▄▄▄  ▄▄▄


  ▄▄▄▄▄▄▄▄▄▄▄▄▄
"""

FINAL_DEST_ASCII = """




  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
"""

TOWERS_ASCII = """
  ▄▄▄      ▄▄▄
  ▄▄▄      ▄▄▄
  ▄▄▄      ▄▄▄
    ▄▄▄▄▄▄▄
"""

ARENA_ASCII = """
  ▄▄▄      ▄▄▄
  ▄▄▄      ▄▄▄

    ▄▄▄▄▄▄▄▄
"""

CHAOS_ASCII = """
      ▄▄▄
▄▄▄     ▄▄   ▄▄
  ▄▄▄    ▄▄
▄▄     ▄▄▄▄
"""


# Dictionnaire des maps disponibles
AVAILABLE_MAPS = {
    "classic": MapConfig(
        "Classique",
        "Pyramide équilibrée",
        CLASSIC_ASCII,
        classic_map
    ),
    "battlefield": MapConfig(
        "Battlefield",
        "3 plateformes aériennes",
        BATTLEFIELD_ASCII,
        battlefield_map
    ),
    "final_destination": MapConfig(
        "Final Destination",
        "Combat pur, une plateforme",
        FINAL_DEST_ASCII,
        final_destination_map
    ),
    "towers": MapConfig(
        "Tours",
        "Deux tours symétriques",
        TOWERS_ASCII,
        towers_map
    ),
    "arena": MapConfig(
        "Arène",
        "Centre + coins stratégiques",
        ARENA_ASCII,
        arena_map
    ),
    "chaos": MapConfig(
        "Chaos",
        "Plateformes dispersées",
        CHAOS_ASCII,
        chaos_map
    )
}
