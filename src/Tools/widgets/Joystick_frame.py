import tkinter as tk
from tkinter import ttk

class FrameJoystick(tk.LabelFrame):
    def __init__(self, parent, id, titre="Joystick", **kwargs):
        super().__init__(parent, text=titre, pady=9, **kwargs)

        self.id = id # Left or Right Joystick 

        self.master = parent
        self.JCCHandler = parent.master.JCCHandler

        self.sensibility = tk.DoubleVar(value=1.0)
        self.invert_x = tk.BooleanVar(value=False)
        self.invert_y = tk.BooleanVar(value=False)

        self.sensibility_str = tk.StringVar(value=f"{self.sensibility.get():.2f}")

        self._create_widgets()
        self._place_widgets()

    def _create_widgets(self):
        # --- Canvas for the joystick ---
        self.canvas = tk.Canvas(self, width=180, height=180, bg="#2C2C2C", highlightthickness=0, highlightbackground="#555")
        
        # Center of the canvas
        self.center = (90, 90)
        self.radius = 70

        # Drawing the outline of the joystick
        self.canvas.create_oval(
            self.center[0]-self.radius, self.center[1]-self.radius,
            self.center[0]+self.radius, self.center[1]+self.radius,
            outline="#888", width=2
        )

        # Central cross
        self.canvas.create_line(0, self.center[1], 180, self.center[1], fill="#555", dash=(3,2))
        self.canvas.create_line(self.center[0], 0, self.center[0], 180, fill="#555", dash=(3,2))

        # Small circle representing the position of the joystick
        self.dot_radius = 5
        self.dot = self.canvas.create_oval(
            self.center[0]-self.dot_radius, self.center[1]-self.dot_radius,
            self.center[0]+self.dot_radius, self.center[1]+self.dot_radius,
            fill="#00FF88"
        )

        # --- Sensibility slider ---
        self.scale_label = ttk.Label(self, text="Sensibility")  
        self.scale_label_sensibility = ttk.Label(self, textvariable=self.sensibility_str)  
        self.scale = ttk.Scale(self, from_=0.1, to=2.0, orient="horizontal",length=150, variable=self.sensibility, command= self.on_sensibility_change)
        

        # --- Check buttons ---
        self.chk_x = ttk.Checkbutton(self, text="Invert X axis", variable=self.invert_x, command= self.on_invert_change)
        self.chk_y = ttk.Checkbutton(self, text="Invert Y axis", variable=self.invert_y, command= self.on_invert_change)
        
        # --- Regular joystick update ---
        self._update_position()


    
    def _place_widgets(self):
        # Canva
        self.canvas.grid(column=0, row=0)

        # Slider
        self.scale_label.grid(column=0, row=1, padx=(5,0), pady=(2,5))
        self.scale_label_sensibility.grid(column=0, row=3, padx=(2,5))
        self.scale.grid(column=0, row=2, pady=(2,0))

        # Check buttons
        self.chk_x.grid(column=0, row=4, pady=2)
        self.chk_y.grid(column=0, row=5, pady=2)

    def _update_position(self):
        """Met à jour la position du point représentant le joystick."""
        x, y = 0, 0

        # If a joystick exists in the App
        if hasattr(self.master, "joycon") and self.master.joycon is not None:
            try:
                x, y = self.master.joycon.joystick.get_direction()
            except Exception:
                pass  # si la méthode n'existe pas ou erreur interne

        # Applying sensitivity and axis inversion
        if self.invert_x.get():
            x = -x
        if self.invert_y.get():
            y = -y

        x *= self.sensibility.get()
        y *= self.sensibility.get()

        # Limit movement inside the circle
        max_move = self.radius
        px = self.center[0] + x * max_move
        py = self.center[1] - y * max_move

        # Deplace little dot
        self.canvas.coords(
            self.dot,
            px - self.dot_radius, py - self.dot_radius,
            px + self.dot_radius, py + self.dot_radius
        )

        # Schedule the next update
        self.after(50, self._update_position)

    def on_sensibility_change(self, value):
        """Appelée quand la barre de sensibilité est déplacée"""
        self.sensibility_str.set(f"{self.sensibility.get():.2f}")
        value = round(float(value), 2)
        self.JCCHandler.set("Joystick", self.id + "Sensibility", str(value))
        self.master.master.debug(f"<CONFIG> Sensibility = {value}")

    def on_invert_change(self):
        """Appelée quand une case est cochée/décochée"""
        self.JCCHandler.set("Joystick", self.id + "Invert_x", str(self.invert_x.get()))
        self.JCCHandler.set("Joystick", self.id + "Invert_y", str(self.invert_y.get()))
        self.master.master.debug(f"<CONFIG> Invert_x = {self.invert_x.get()}, Invert_y = {self.invert_y.get()}")

    def load_config(self, data):
        self.sensibility.set(value=data[self.id + "Sensibility"])
        self.invert_x.set(value=data[self.id + "Invert_x"])
        self.invert_y.set(value=data[self.id + "Invert_y"])
        

# --- Example 
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Joystick Widget")
    root.configure(bg="#2C2C2C")

    # Example without joystick
    widget = FrameJoystick(root,"R", titre="Joystick", bg="#2C2C2C", fg="white")
    widget.pack(padx=20, pady=20)

    root.mainloop()
