"""
Module de gestion de la base de données des pseudos
Stocke les pseudos des joueurs dans un fichier texte
"""

import os
from datetime import datetime

DATABASE_FILE = "pseudos_database.txt"

def save_pseudos(pseudo1, pseudo2):
    """Sauvegarde les pseudos dans la base de données

    Args:
        pseudo1: Pseudo du joueur 1
        pseudo2: Pseudo du joueur 2
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(DATABASE_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] Joueur 1: {pseudo1} | Joueur 2: {pseudo2}\n")

def get_all_pseudos():
    """Récupère tous les pseudos enregistrés

    Returns:
        list: Liste des lignes de la base de données
    """
    if not os.path.exists(DATABASE_FILE):
        return []

    with open(DATABASE_FILE, "r", encoding="utf-8") as f:
        return f.readlines()

def get_last_pseudos():
    """Récupère les derniers pseudos utilisés

    Returns:
        tuple: (pseudo1, pseudo2) ou (None, None) si aucun n'est trouvé
    """
    pseudos = get_all_pseudos()

    if not pseudos:
        return None, None

    # Lire la dernière ligne
    last_line = pseudos[-1].strip()

    try:
        # Parser la ligne pour extraire les pseudos
        # Format: [date] Joueur 1: pseudo1 | Joueur 2: pseudo2
        parts = last_line.split("|")
        pseudo1 = parts[0].split("Joueur 1:")[1].strip()
        pseudo2 = parts[1].split("Joueur 2:")[1].strip()
        return pseudo1, pseudo2
    except:
        return None, None

def count_games():
    """Compte le nombre de parties jouées

    Returns:
        int: Nombre de parties
    """
    return len(get_all_pseudos())
