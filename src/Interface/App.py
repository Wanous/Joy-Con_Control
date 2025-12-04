#imports libraries used by the software
import tkinter as tk
from tkinter import messagebox,PhotoImage,colorchooser,ttk
from tkinter.filedialog import askopenfilename,asksaveasfilename
import copy

# Tools
from src.Tools.INIConfiguration import ConfigINIManager
from src.Tools.JCCFormat import JCCFormat
from src.Tools.StyleManager import StyleManager

from src.JoyCon.JoyCon import MyJoyCon


# Pages
from src.Interface.Pages.Main_menu import MainMenuPage
from src.Interface.Pages.Menu_JCR import RightJoyConConfigPage
from src.Interface.Pages.Menu_JCL import LeftJoyConConfigPage
from src.Interface.Pages.Menu_JCLR import LeftRightJoyConConfigPage


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # --- .ini configuration handler     
        self.IniConfig = ConfigINIManager(r"src/Ressources/Configuration/App_configuration/App_configuration.ini")

        # --- .jcc configuration handler                  # Exclusif file format for JCC
        self.JCCHandler = ConfigJCCHandler(self)
        self.JCCConfig = None                             # Contain the .jcc configuration
        self.JCCPath = None                               # Contain the .jcc path (if loaded)
        self.modification = False                         # Check if modification are saved  

        # --- Joycons handler 
        self.joycons = {
            "JCR":None,
            "JCL":None
        }

        # --- Window configuration
        self.title("JoyCon Control")
        self.iconbitmap("src/Ressources/Icon/Icon.ico")
        self.geometry("800x500")
        self.dimension = {'x':800,'y':500}
        self.resizable(False, False)                      # Window have strict dimension (this software don't need to resize)
        self.bind("<Configure>", self.resize)             # Method called when resizing 

        # --- Window theme (Initiated in 82)
        self.style = ttk.Style()
        self.style.theme_use('winnative')
        StyleManager.load_from_config(self.IniConfig)

        # --- Sets shortcuts
        self.Shortcuts()                                  # Initiate keyboard shortcut

        self.after(100,self.Initiate_menus)               # Time before starting
        
    def run(self):
        '''
        Method called only once by main.py that allows the application to start
        by displaying the logo and then starting the Tkinter loop
        '''

        #--- Boot image 
        #img = PhotoImage(file="src/Ressources/Photos/Menu_Demarrage.png")
        #self.label = tk.Label(self, image=img)
        #self.label.place(x=-2,y=0)

        self.mainloop()

    def Initiate_menus(self):
        '''Initiate the menus of the graphic interface'''

        self.current_menu = "MainMenu"
        self.main_menu = MainMenuPage(self)

        self.menu_JCR = RightJoyConConfigPage(self)
        self.menu_JCL = LeftJoyConConfigPage(self)
        self.menu_JCLR = LeftRightJoyConConfigPage(self)


        # Attribute to access the menus and their configuration with their name
        # Name = Menu + type of disposition
        self.menus ={'MainMenu':{"Frame": self.main_menu, "Geometry": "800x500"},
                             'MenuJCR': {"Frame": self.menu_JCR, "Geometry": "500x420"},
                             'MenuJCL': {"Frame": self.menu_JCL, "Geometry": "500x420"},
                             'MenuJCLR': {"Frame":self.menu_JCLR, "Geometry": "1000x840"}
                    } 
        
        # Need to set the theme after all menus are Initiated
        StyleManager.set_theme(self.IniConfig.get("configuartion_data", "theme"), self)
        
        self.Change_menu(self.current_menu )

    def Shortcuts(self):
        self.bind("<Escape>", lambda event : self.To_main_menu())  

        
    def Change_menu(self, menu='MainMenu', loading = False):
        self.debug("[UPDATE] "+"current menu = "+ menu)

        # Unloads the current menu and loads the new one
        self.menus[self.current_menu]["Frame"].forget()
        self.current_menu = menu
        self.menus[self.current_menu]["Frame"].tkraise()

        # Load original configuration (if the user is not loading a file)
        if not loading and menu != "MainMenu":
            self.JCCHandler.init_menu_config(self.current_menu)
            self.menus[self.current_menu]["Frame"].load_config(self.JCCConfig, True)

        # Apply its geometry and display it
        self.geometry(self.menus[self.current_menu]["Geometry"])
        self.menus[self.current_menu]["Frame"].pack(fill="both", expand=True) 

        
    def update_current_menu(self):
        self.debug("[Update] " + self.current_menu)
        self.menus[self.current_menu]["Frame"].update_config()

    def To_main_menu(self):
        change = True
        if self.current_menu == 'MainMenu':
            pass # Skip to not reload the main menu
        else:
            if self.modification:                                   # If there are unsaved modification 
                message = tk.messagebox.askyesno("Unsaved modification",   # A message of prevention is sent
                """
                Are you sure ?
                Any unsaved data will be lost.
                """)
                
                change = message

        print(change)
        if change:
            if self.JCCPath != None :
                self.JCCHandler.deload()
            self.Change_menu()

    def change_theme(self, theme):
        """Method used by MainMenu to change theme"""
        if theme.get()  == 0:
            self.IniConfig.set("configuartion_data", "theme", "light")
            StyleManager.set_theme("light", self)
            self.debug(f"*Theme* set to light")
        else :
            self.IniConfig.set("configuartion_data", "theme", "dark")
            StyleManager.set_theme("dark", self)   
            self.debug(f"*Theme* set to dark")    

        # Save the modification of theme
        self.IniConfig.save()
        
    
    def resize(self,event):
        '''
        Method triggered by the 'window is being resized' event and allows you to
        recalculate the position of widgets on the screen, taking into account the new dimensions
        of the window, while resizing them to maintain the same aspect ratio.
        '''
        #TODO: Maybe one day make the resize true 

        self.dimension['x'] = self.winfo_width()
        self.dimension['y'] = self.winfo_height()

    def error_windows(self, title, message):
        messagebox.showerror(title, message)

    def debug(self, message):
        """Method to centralize every debug messages"""
        print(message)

    def quit(self):
        '''
        This method quits the application after asking the user
        if they really want to quit via a window that asks for a yes or no choice.
        '''
        message = tk.messagebox.askyesno("Quit", "Are you sure you want to leave?")
        if message:
            self.master.destroy() #Fait disparaître la fenêtre
            self.master.quit()    #Stop l'application

class ConfigJCCHandler():
    def __init__(self,parent: Application):
        self.master = parent

        self.OriginalConfig = {
            "JCR" : JCCFormat.load(r"src/Ressources/Configuration/Controllers_configuration/JCR_configuration.jcc"),
            "JCL" : JCCFormat.load(r"src/Ressources/Configuration/Controllers_configuration/JCL_configuration.jcc"),
            "JCLR" : JCCFormat.load(r"src/Ressources/Configuration/Controllers_configuration/JCLR_configuration.jcc"),
        }
    
    def init_menu_config(self, menu):
        self.master.modification = False
        self.master.JCCConfig = copy.deepcopy(self.OriginalConfig[menu[4:]])

        #self.display_config()

    def deload(self):
        self.master.debug("|file deloaded| " + self.master.JCCPath)    
        self.master.modification = False
        self.master.JCCPath = None
        self.master.title("JoyCon Control") 
        self.get_FrameFile()._on_deload()
        # The config will be reinitialise when a new menu is enter

    def load(self):
 
        message=None
        if self.master.modification:                                 # If there are unsaved modification 
            message = tk.messagebox.askyesno("Load configuration",   # A message of prevention is sent
            """
            Are you sure ?
            Any unsaved data will be lost.
            """)
        if message or not self.master.modification :
            try :
                path = askopenfilename(title="Choose a file to open", filetypes=[("JoyConControl", "*.jcc")])
                
                self.master.JCCConfig = JCCFormat.load(path)
                self.master.modification = False
                self.master.JCCPath = path

                self.master.title("JoyCon Control"+" "+path)  # Displays the path name in the main window title 
                self.master.debug("|file loaded| " + path)      

            except FileNotFoundError:                        # Error that occurs if the user closes the window instead of making a choice
                #self.master.error_windows("Error", "File not found")
                return None
        else :
            return None
        # --- config treatment 
        self.apply_config() 
        # --- save it in the .ini as the "last configuration"
        self.master.IniConfig.set("configuartion_data", "last_configuartion",self.master.JCCPath)
        self.master.IniConfig.save()

        return self.master.JCCPath
            
    def set(self, section, option, value):
        """
        Apply modification to the configuration and display it by updating the current configuration menu
        """
        if not self.master.modification :
            self.get_FrameFile()._on_modification()
        self.master.modification = True
        self.master.JCCConfig[section][option] = value

        #self.display_config()

    def save(self,event=None):
        '''Method that saves a configuration to a .jcc file '''
        #If there is no file to import, the program asks for
        #a directory to save it in .jcc 
        if self.master.JCCPath == None:
            try:
                path = asksaveasfilename( filetypes=[("JoyConControl", "*.jcc")])
                if path !='':
                    JCCFormat.save(path+'.jcc', self.master.JCCConfig) 
                    path += ".jcc"
                    self.master.JCCPath = path        
                    self.master.title("JoyCon Control"+" "+path) 
                    self.master.modification = False

                    self.master.debug("|file create| " + path)
            except FileNotFoundError:
                return None
        else:
            # Otherwise the data is just saved without making a request
            JCCFormat.save(self.master.JCCPath, self.master.JCCConfig) 
            self.master.debug("|file saved| " + self.master.JCCPath)
            self.master.modification = False

    def apply_config(self):
        # If the disposition is relate to another menu
        new_menu = "Menu"  + self.master.JCCConfig["Disposition"]["type"] 
        if new_menu != self.master.current_menu :
            self.master.Change_menu(new_menu, True)
            self.get_FrameFile()._on_extern_config_load()

        # Apply the disposition in the appropriate menu
        self.master.menus[self.master.current_menu]["Frame"].load_config(self.master.JCCConfig)

    def get_config(self):
        return self.master.JCCConfig

    def get_path(self):
        return self.master.JCCPath
    
    def get_FrameFile(self):
        """Return the FileFrame object from the current menu"""
        return self.master.menus[self.master.current_menu]["Frame"].file_frame 
            
    def display_config(self):
        """Properly displays the contents of the configuration file."""
        result = ""

        for section in self.master.JCCConfig:
            result += f"[{section}]\n"
            for key, value in self.master.JCCConfig[section].items():
                result += f"\t{key}: {value}\n"
            result += "\n"

        self.master.debug(result.strip())


class JoyConHandler():
    def __init__(self, parent):
        self.master = parent

    def connect(self, controller):
        pass        

        