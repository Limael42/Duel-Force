"""
Gestion des touches personnalisées
Les touches sont stockées uniquement en mémoire (temporaires pour la session)
Au redémarrage de l'application, les touches reviennent aux valeurs par défaut
"""

# Touches par défaut
DEFAULT_KEYBINDINGS = {
    'player1': {
        'left': 'q',
        'right': 'd',
        'jump': 'z',
        'attack': 'a',
        'special': 'e'
    },
    'player2': {
        'left': 'Left',
        'right': 'Right',
        'jump': 'Up',
        'attack': 'space',
        'special': 'Return'
    }
}

# Touches actuelles en mémoire (initialisées avec les valeurs par défaut)
# Ces touches sont temporaires et seront perdues à la fermeture de l'application
_current_keybindings = None

# Noms lisibles des actions
ACTION_NAMES = {
    'left': 'Déplacement gauche',
    'right': 'Déplacement droite',
    'jump': 'Saut',
    'attack': 'Attaque normale',
    'special': 'Attaque spéciale'
}

# Noms lisibles des touches spéciales
KEY_DISPLAY_NAMES = {
    'Left': '←',
    'Right': '→',
    'Up': '↑',
    'Down': '↓',
    'space': 'Espace',
    'Return': 'Entrée',
    'Control_L': 'Ctrl Gauche',
    'Control_R': 'Ctrl Droit',
    'Shift_L': 'Shift Gauche',
    'Shift_R': 'Shift Droit',
    'Alt_L': 'Alt Gauche',
    'Alt_R': 'Alt Droit',
    'Tab': 'Tab',
    'Escape': 'Échap',
    'BackSpace': 'Retour',
    'Delete': 'Suppr',
    'Insert': 'Inser',
    'Home': 'Début',
    'End': 'Fin',
    'Prior': 'Page ↑',
    'Next': 'Page ↓'
}


def get_key_display_name(key):
    """Retourne le nom d'affichage d'une touche

    Args:
        key: Nom interne de la touche

    Returns:
        Nom lisible de la touche
    """
    return KEY_DISPLAY_NAMES.get(key, key.upper() if len(key) == 1 else key)


def _initialize_keybindings():
    """Initialise les touches en mémoire avec les valeurs par défaut

    Returns:
        dict: Configuration des touches pour les deux joueurs
    """
    global _current_keybindings
    _current_keybindings = {
        'player1': DEFAULT_KEYBINDINGS['player1'].copy(),
        'player2': DEFAULT_KEYBINDINGS['player2'].copy()
    }
    return _current_keybindings


def load_keybindings():
    """Retourne les touches actuelles en mémoire

    Si c'est le premier appel, initialise avec les valeurs par défaut.
    Les touches sont temporaires et ne sont jamais sauvegardées dans un fichier.

    Returns:
        dict: Configuration des touches pour les deux joueurs
    """
    global _current_keybindings
    if _current_keybindings is None:
        return _initialize_keybindings()
    return _current_keybindings


def save_keybindings(keybindings):
    """Met à jour les touches en mémoire pour la session actuelle

    Les touches ne sont PAS sauvegardées dans un fichier.
    Elles sont uniquement stockées en mémoire et seront perdues à la fermeture.

    Args:
        keybindings: Configuration des touches à appliquer

    Returns:
        bool: Toujours True (succès)
    """
    global _current_keybindings
    _current_keybindings = {
        'player1': keybindings['player1'].copy(),
        'player2': keybindings['player2'].copy()
    }
    return True


def reset_to_defaults():
    """Réinitialise les touches aux valeurs par défaut en mémoire

    Returns:
        dict: Configuration par défaut
    """
    return _initialize_keybindings()


def check_key_conflict(keybindings, player, action, new_key):
    """Vérifie si une touche est déjà utilisée

    Args:
        keybindings: Configuration actuelle
        player: 'player1' ou 'player2'
        action: Action à modifier
        new_key: Nouvelle touche proposée

    Returns:
        tuple: (has_conflict: bool, conflict_action: str or None, conflict_player: str or None)
    """
    # Vérifier les conflits dans le même joueur
    for act, key in keybindings[player].items():
        if act != action and key == new_key:
            return (True, act, player)

    # Vérifier les conflits avec l'autre joueur (optionnel, on peut autoriser)
    # Pour l'instant, on autorise les mêmes touches entre joueurs

    return (False, None, None)


def get_forbidden_keys():
    """Retourne la liste des touches interdites pour éviter les problèmes

    Returns:
        set: Ensemble des touches à éviter
    """
    return {
        'Escape',  # Réservé pour quitter/pause
        'F11',     # Plein écran
        'Alt_L',   # Peut causer des problèmes système
        'Alt_R',
        'Super_L', # Touche Windows
        'Super_R',
        'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F12'  # Touches fonction
    }
