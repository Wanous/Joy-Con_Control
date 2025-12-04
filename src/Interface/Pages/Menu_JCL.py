import tkinter as tk
from tkinter import ttk

from src.Tools.widgets.FileControl_frame import FrameFileControl
from src.Tools.widgets.Button_frame import FrameButtons
from src.Tools.widgets.Joystick_frame import FrameJoystick
from src.Tools.widgets.Title_frame import FrameTitle


class LeftJoyConConfigPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        """
        Page for the configuration of the Left JoyCon
        """
        super().__init__(parent, *args, **kwargs)

        self.master = parent
        self.JCLConfig = self.master.JCCHandler.OriginalConfig["JCL"]

        self._create_widgets()
        self._place_widgets()        

    def _create_widgets(self):
        """Create the widgets of the page (without placing it)."""

        # Frame for file control
        self.file_frame = FrameFileControl(self)

        # Frame for the buttons configuration
        self.buttons = self.JCLConfig["Buttons"]
        self.buttons_frame = FrameButtons(self, "", self.buttons)
        self.buttons_frame_title = FrameTitle(self, titre="Joy con left buttons", couleur="#00BBDB", rayon=10, width=200,height=30, bg="#F0F0F0")

        # Frame for the joystick configuration
        self.joystick_frame = FrameJoystick(self, "L", titre="Joystick", bg="#F0F0F0", fg="white")
        self.joystick_frame_title = FrameTitle(self, titre="Left Joystick", couleur="#00BBDB", rayon=10, width=150,height=30, bg="#F0F0F0")

    def _place_widgets(self):
        """Place widgets in the frame with place method."""
        self.file_frame.place(
            x = int(self.master.winfo_width()*0.04), 
            y = int(self.master.winfo_height()*0.02) 
        )

        self.buttons_frame_title.place(
            x = int(self.master.winfo_width()*0.03), 
            y = int(self.master.winfo_height()*0.12)
        )  
        
        self.buttons_frame.place(
            x = int(self.master.winfo_width()*0.05), 
            y = int(self.master.winfo_height()*0.15)
        ) 

        self.joystick_frame_title.place(
            x = int(self.master.winfo_width()*0.32), 
            y = int(self.master.winfo_height()*0.12)
        )  
        
        self.joystick_frame.place(
            x = int(self.master.winfo_width()*0.35), 
            y = int(self.master.winfo_height()*0.14)
        )   

    def load_config(self, config, init = False):
        self.JCLConfig = config
        self.buttons_frame.load_config(self.JCLConfig["Buttons"])
        self.joystick_frame.load_config(self.JCLConfig["Joystick"])

        if init :
            print("<Config> " + "Original config applied")
            
        else :
            print("<Config> " + "New config applied")

    def _go_back(self):
        """ Warning before potentially going back to main menu"""
        pass