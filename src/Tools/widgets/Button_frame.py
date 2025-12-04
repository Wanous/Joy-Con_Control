import tkinter as tk
from tkinter import ttk

class FrameButtons(tk.LabelFrame):
    def __init__(self, parent, name, liste_buttons, function = lambda b: print("hello, " + b), *args, **kwargs):
        """"""
        super().__init__(parent,text = name, labelanchor='nw', borderwidth=2)
        
        self.buttons = liste_buttons
        self.master = parent
        self.JCCHandler = parent.master.JCCHandler
        self.function = function

        self._create_widgets()
        self._place_widgets()        

    def _create_widgets(self):
        """Create the widgets of the page (without placing it)."""

        # Frame content

        self.option_buttons = {
            'anchor':"center",
            'bd':3,
            'width':15,
            'height':1,
            'wraplength':200,
            'bg':"#000000",
            'fg':"#FFFFFF"
        }

        self.label_buttons = {}
        self.button_buttons = {}

        for button in self.buttons:
            self.label_buttons[button]  = (ttk.Label(self, text=button+" : ", font=("Arial", 16, "bold")))
            self.button_buttons[button] = (tk.Button(self, 
                                                      text=(str)(self.buttons[button]),
                                                      command=lambda b=button: self.map_key(b, self.master),
                                                      **self.option_buttons))
    

    def _place_widgets(self):
        """Placer les widgets dans la grille ou avec grid."""
        
        self.grid(column=0, row=0, padx=0, pady=0)  

        buttons = list(self.buttons.keys())

        # Placements of the first button (to assure a padding between frame and the list)
        first_button = buttons[0]
        self.label_buttons[first_button].grid(column=0, row=0, padx=(20,0), pady=(20,5))
        self.button_buttons[first_button].grid(column=1, row=0, padx=(0,25), pady=(20,5))

        # Placements of the other buttons
        for i, button in enumerate(buttons[1:], start=1):
            self.label_buttons[button].grid(column=0, row=i, padx=(20,0), pady=(5,5))
            self.button_buttons[button].grid(column=1, row=i, padx=(0,25), pady=(5,5))

    def map_key(self, key, root: tk.Tk):
        """
        Met Tkinter en pause et attend qu'une touche soit pressée.
        Retourne le nom de la touche ou None si 'Escape' est pressée.
        """
        result = {"key": None}  # Utilisé pour stocker la touche capturée

        # Création de la fenêtre modale
        top = tk.Toplevel(self.master)
        top.title("Entrée d'une touche")
        top.geometry("250x100")
        top.resizable(False, False)
        top.grab_set()  # rend la fenêtre modale

        # Message
        label = tk.Label(top, text="Appuyez sur une touche…", font=("Arial", 11))
        label.pack(expand=True, pady=20)

        # Gestionnaire d'événement pour la touche appuyée
        def on_key(event):
            if event.keysym == "Escape":
                result["key"] = None  # annulation
            else:
                result["key"] = event.keysym  # nom symbolique de la touche
            top.destroy()  # ferme la fenêtre

        # Liaison clavier
        top.bind("<Key>", on_key)

        # Attente (bloquante mais locale à cette fenêtre)
        self.master.wait_window(top)

        if result["key"] != self.button_buttons[key].cget("text") :

            if self.button_buttons[key].cget("text") == "None":
                self.master.master.debug("<Config> -Key initialised-  " + key + " --> " + (str)(result["key"]))
            else :
                self.master.master.debug("<Config> -Key changed-  " + self.button_buttons[key].cget("text") + " --> " + (str)(result["key"]))

            self.JCCHandler.set("Buttons", key, result["key"])
            self.button_buttons[key].configure(text=(str)(result["key"]))

    def load_config(self, data):
        for key, value in data.items():
            if key in self.button_buttons:
                self.button_buttons[key].configure(text=(str)(value))


        




if __name__ == "__main__":

    def dis_bonjour(button):
        print("bonjour ", button)

    window = tk.Tk()
    option_buttons = {
        'text':"Buttons",
        'relief':"groove",
    }
    test = FrameButtons(window,"test",{'A':None, 'B': None, 'X': None, 'Y': None}, dis_bonjour)
    window.mainloop()
