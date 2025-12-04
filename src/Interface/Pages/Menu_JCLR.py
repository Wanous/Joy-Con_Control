import tkinter as tk
from tkinter import ttk

class LeftRightJoyConConfigPage(tk.Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        """
        parent : conteneur (souvent root ou une frame principale)
        controller : référence optionnelle vers ton contrôleur principal
        """
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self._create_widgets()
        self._place_widgets()        

    def _create_widgets(self):
        """Create the widgets of the page (without placing it)."""
        self.title_label = ttk.Label(self, text="Configuration Joy-Con Droit", font=("Arial", 16, "bold"))

        # Buttons
        self.button_label = ttk.Label(self, text="Mapper un bouton :")
        self.button_entry = ttk.Entry(self)

        # Option
        self.stick_label = ttk.Label(self, text="Sensibilité du stick :")
        self.stick_scale = ttk.Scale(self, from_=0.1, to=2.0, orient="horizontal")

        # Bouton de sauvegarde
        self.save_button = ttk.Button(self, text="Enregistrer", command=self._save_config)

        # Bouton retour
        self.back_button = ttk.Button(self, text="Retour", command=self._go_back)

    def _place_widgets(self):
        """Placer les widgets dans la grille ou avec pack/place."""
        self.title_label.pack(pady=10)

        self.button_label.pack(anchor="w", padx=10)
        self.button_entry.pack(fill="x", padx=10, pady=5)

        self.stick_label.pack(anchor="w", padx=10)
        self.stick_scale.pack(fill="x", padx=10, pady=5)

        self.save_button.pack(pady=10)
        self.back_button.pack(pady=5)

    def _save_config(self):
        """Méthode appelée quand l’utilisateur clique sur 'Enregistrer'."""
        button = self.button_entry.get()
        sensitivity = self.stick_scale.get()
        print(f"[DEBUG] Sauvegarde config Joy-Con droit → bouton: {button}, sensibilité: {sensitivity}")

        # Ici tu pourrais envoyer ça dans Command.py ou un fichier JSON

    def _go_back(self):
        """Retour au menu principal"""
        if self.controller:
            self.controller.show_frame("MainMenuPage")  # Exemple d’appel
        else:
            print("[DEBUG] Retour demandé (pas de controller).")
