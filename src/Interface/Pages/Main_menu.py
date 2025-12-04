import tkinter as tk
from tkinter import ttk

class MainMenuPage(tk.Frame):
    def __init__(self, parent,*args, **kwargs):
        """
        parent : conteneur (souvent root ou une frame principale)
        controller : référence optionnelle vers ton contrôleur principal
        """
        super().__init__(parent, *args, **kwargs)

        self.master = parent
        self.type_disposition = {
            'JCL':"Joy-Con left", 
            'JCR':"Joy-Con right",
            'JCLR':"Joy-Con right + left"
        }

        self.dark_theme = tk.BooleanVar(value=self.master.IniConfig.get("configuartion_data", "theme") == "dark")

        self._create_widgets()
        self._place_widgets()

    def _create_widgets(self):
        """Create the widgets of the page (without placing it)."""

        #self.bouton_nouveau = tk.Button(self, text="Créer",command=self.commencement_graphe)
        #self.bouton_nouveau.place(x=35,y=110)

        option_title = {'font': ('Tahoma', 20, "bold")}
        self.message = ttk.Label(self, text="Type of disposition :",**option_title)
        
        # configuration of the buttons
        self.option_buttons = {
            'activeforeground':"white",
            'fg':"#FFFFFF",
            'anchor':"center",
            'bd':3,
            'bg':"lightgray",
            'width':15,
            'height':7,
            'wraplength':200,
        }
        
        self.disposition_buttons = []
        
        for disposition in self.type_disposition:
            self.disposition_buttons.append(tk.Button(self, 
                                                      text=self.type_disposition[disposition],
                                                      command=lambda d=disposition: self._go_in(d),
                                                      **self.option_buttons))
            
        self.theme = ttk.Checkbutton(self, text="Dark theme", variable=self.dark_theme , command=lambda v = self.dark_theme: self.master.change_theme(v))

    def _place_widgets(self):
        """Placer les widgets dans la grille ou avec pack/place."""
        self.message.place(
            x = self.master.winfo_width()*0.1, 
            y = self.master.winfo_height()*0.1
        )

        gap = 20 + self.option_buttons['width']*4 # gap + button lenght 
        counter = 0
        start_x = self.master.winfo_width()*0.15 
        start_y = self.master.winfo_height()*0.2   

        for i in range (len(self.disposition_buttons)):
            self.disposition_buttons[i].place(x = i*gap + start_x + counter, y = start_y)
            counter += gap

        self.theme.place(
            x = self.master.winfo_width()*0.8, 
            y = self.master.winfo_height()*0.9
        )

    def resize(self):
        self._place_widgets()

    def _go_in(self, menu):
        """Va vers le menu indiqué en paramètre"""
        for disposition in self.type_disposition:
            if disposition == menu :
                self.master.Change_menu('Menu'+menu) # Menu + JCL = MenuJCL
