import tkinter as tk

class FrameTitle(tk.Frame):
    def __init__(self, parent, titre="Titre", couleur="#4A90E2", rayon=15, height=25, width=200, **kwargs):
        super().__init__(parent, **kwargs)

        self.height = height
        self.width = width

        self.configure(width=self.width, height=self.height)
        self.pack_propagate(False)
        
        self.couleur = couleur
        self.rayon = rayon
        self.titre = titre

        # Canvas pour le fond arrondi
        self.canvas = tk.Canvas(self, highlightthickness=0, bg=self["bg"])
        self.canvas.pack(fill="both", expand=True)
        
        # Label du titre
        self.label_titre = tk.Label(self, text=self.titre,bg=self.couleur, fg="white", font=("Segoe UI", 12, "bold"))
        self.label_titre.place(relx=0.45, rely=0.4, anchor="center")

        # Redessiner le fond à chaque redimensionnement
        self.bind("<Configure>", self._redessiner)

    def _redessiner(self, event=None):
        self.canvas.delete("all")

        w, h = self.winfo_width(), self.winfo_height()
        r = self.rayon
        c = self.couleur

        # Crée un rectangle arrondi
        self.canvas.create_arc((0, 0, 2*r, 2*r), start=90, extent=90, fill=c, outline=c)
        self.canvas.create_arc((w-2*r, 0, w, 2*r), start=0, extent=90, fill=c, outline=c)
        self.canvas.create_arc((w-2*r, h-2*r, w, h), start=270, extent=90, fill=c, outline=c)
        self.canvas.create_arc((0, h-2*r, 2*r, h), start=180, extent=90, fill=c, outline=c)
        self.canvas.create_rectangle((r, 0, w-r, h), fill=c, outline=c)
        self.canvas.create_rectangle((0, r, w, h-r), fill=c, outline=c)

# Exemple d'utilisation
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x200")
    root.configure(bg="#2C2C2C")

    cadre = FrameTitle(root, titre="Mon Widget", couleur="#FF6F61", rayon=20, bg="#2C2C2C")
    cadre.pack(padx=20, pady=20, fill="both", expand=True)

    root.mainloop()
