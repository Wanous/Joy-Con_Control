import tkinter as tk
from tkinter import ttk
from src.Tools.widgets.Title_frame import FrameTitle

class StyleManager:
    """Manage and apply theme-based colors to widgets."""

    current_theme = "light"
    themes = {}

    @classmethod
    def load_from_config(cls, config_manager):
        """Load theme colors directly from the config file."""
        cls.themes.clear()

        for theme_name in ("light", "dark"):
            section_name = f"colors.{theme_name}"
            cls.themes[theme_name] = dict(config_manager.items(section_name))


    @classmethod
    def set_theme(cls, theme_name, parent):
        """Switch the current theme."""
        theme_name = theme_name.lower()
        cls.current_theme = theme_name
        StyleManager.apply_to_all(parent)

    @classmethod
    def get_color(cls, key, fallback=None):
        """Get a color value from the current theme."""
        return cls.themes.get(cls.current_theme, {}).get(key, fallback)

    @classmethod
    def apply(cls, widget):
        """Apply the current theme colors to a given widget."""
        theme = cls.themes.get(cls.current_theme, {})
        bg = theme.get("bg", "#FFFFFF")
        fg = theme.get("text", "#000000")

        # --- Tk widgets ---
        try:
            # Special cases here
            if isinstance(widget, tk.Label) and isinstance(widget.master, FrameTitle):
                widget.configure(fg=fg)
            elif isinstance(widget, (tk.Frame, tk.Canvas)):
                widget.configure(bg=bg)
            # All cases that are not speciale here
            else:
                widget.configure(bg=bg, fg=fg)
        except tk.TclError:
            #print("erreur : " + widget.winfo_name())
            pass  # Some widgets (like ttk) don't support direct bg/fg (also frame)




        # --- Ttk widgets ---

        if isinstance(widget, ttk.Widget):
            try :
                style = ttk.Style()
                style.theme_use("clam")  # 'clam' permet de redéfinir les couleurs

                # Style unique par classe
                widget_class = widget.winfo_class()  # Ex: TLabel, TButton...
                style_name = f"{cls.current_theme}.{widget_class}"
                # print(widget_class)

                # Configuration du style de base
                style.configure(style_name,
                                background=bg,
                                foreground=fg,
                                fieldbackground=fg,
                                troughcolor=fg)

                # Mapping (hover, active)
                style.map(style_name,
                        background=[("active", "#8B8B8B"), ("!disabled", bg)],
                        foreground=[("disabled", "#8B8B8B")])

                # Application du style
                widget.configure(style=style_name)
            except tk.TclError:
                pass


    @classmethod
    def apply_to_all(cls, parent):
        """Recursively apply theme to all child widgets."""
        for child in parent.winfo_children():
            cls.apply(child)
            if isinstance(child, (tk.Frame, ttk.Frame, tk.LabelFrame)):
                cls.apply_to_all(child)

if __name__ == "__main__":
    # Assuming ConfigManager already loaded your ini file
    from INIConfiguration import ConfigINIManager

    config = ConfigINIManager(r"C:\Users\marai\Desktop\GitHub\Joy-Con_Control\src\Tools\test.ini")

    StyleManager.load_from_config(config)

    root = tk.Tk()
    
    frame = tk.Frame(root)    
    frame.pack(fill="both", expand=True)

    StyleManager.set_theme("dark", root)

    btnLight = tk.Button(frame, text="Light", command= lambda  : StyleManager.set_theme("light", root))
    btnDark = tk.Button(frame, text="Dark", command= lambda  : StyleManager.set_theme("dark", root))
    slider = ttk.Scale(frame, from_=0, to=10)
    lbl = tk.Label(frame, text="Hello World")

    btnLight.pack(pady=5)
    btnDark.pack(pady=5)

    slider.pack(pady=5)
    lbl.pack(pady=5)

    # Apply theme to all widgets in the root
    StyleManager.apply_to_all(root)

    root.mainloop()
