from ui.menu import MainMenu
import tkinter as tk

def main():
    """Fonction principale qui lance l'application"""
    root = tk.Tk()
    root.title("JEUX PROJET NSI - Duel Force")

    # Mettre en plein écran
    root.attributes('-fullscreen', True)

    # Permettre de quitter le plein écran avec F11 ou Echap
    root.bind('<F11>', lambda e: root.attributes('-fullscreen', not root.attributes('-fullscreen')))
    root.bind('<Escape>', lambda e: root.attributes('-fullscreen', False))

    # Créer le menu principal
    app = MainMenu(root)

    # Lancer la boucle principale
    root.mainloop()

if __name__ == "__main__":
    main()
