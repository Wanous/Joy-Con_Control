import os
import tkinter as tk
from tkinter import ttk

class FrameFileControl(tk.Frame):
    """A widget for saving/loading a file and displaying its name."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.master = parent
        self.file_handler = parent.master.JCCHandler
        self.filename = tk.StringVar(value="No file loaded")

        self._create_widgets()
        self._place_widgets()

    def _create_widgets(self):
        """Create the buttons and label."""
        self.save_button = ttk.Button(self, text="Save", command=self._on_save)
        self.load_button = ttk.Button(self, text="Load", command=self._on_load)
        self.file_label = ttk.Label(self, textvariable=self.filename, width=25)

    def _place_widgets(self):
        """Place the widgets using grid layout."""
        self.save_button.grid(row=0, column=0, padx=5, pady=5)
        self.load_button.grid(row=0, column=1, padx=5, pady=5)
        self.file_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        # Label stretch if frame expands (not very useful)
        # self.grid_columnconfigure(2, weight=1)
    
    def _on_modification(self):
        if self.file_handler.get_path() != None :
             self.filename.set(os.path.basename(self.file_handler.get_path())+"*")
    
    def _on_extern_config_load(self):
        self.filename.set(os.path.basename(self.file_handler.get_path()))

    def _on_save(self):
        """Trigger file saving through FileHandler."""
        if self.file_handler:
            self.file_handler.save()
            self.filename.set(os.path.basename(self.file_handler.get_path()))
        else:
            print("No FileHandler assigned.")

    def _on_load(self):
        """Trigger file loading through FileHandler."""
        if self.file_handler:
            loaded_name = self.file_handler.load()
            self.filename.set(os.path.basename(loaded_name))
            self.file_label.update()
        else:
            print("No FileHandler assigned.")
    
    def _on_deload(self):
        self.filename.set("No file loaded")

if __name__ == "__main__":
    root = tk.Tk()
    widget = FrameFileControl(root)
    widget.pack(padx=10, pady=10)
    root.mainloop()
