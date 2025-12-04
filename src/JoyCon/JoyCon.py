from pyjoycon import JoyCon ,get_L_id, get_R_id
try :
    from src.JoyCon.Joystick import JoystickDirection
    from src.JoyCon.Command import CommandHandler
except ImportError:
    pass

class MyJoyCon(JoyCon):
    def __init__(self, side="L"):
        # Initializing the left or right JoyCon

        if side == "L":
            self.side = "left"
            joycon_id = get_L_id()
            super().__init__(*joycon_id)
            self.joystick = JoystickDirection(self,self.side )

        elif side == "R":
            self.side = "right"
            joycon_id = get_R_id()
            super().__init__(*joycon_id)
            self.joystick = JoystickDirection(self,self.side)

        else:
            raise ValueError("Side must be 'L' or 'R'")


    # --- Boutons ---
    def get_pressed_buttons(self):
        """
        Returns a list of currently pressed buttons.
        """
        buttons = self.get_status()["buttons"][self.side]
        return [btn for btn, pressed in buttons.items() if pressed]

    def is_pressed(self, button_name: str) -> bool:
        """
        Checks if a button is pressed.
        """
        return self.get_status()["buttons"][self.side].get(button_name, False)

    def is_left(self):
        return isinstance(self, MyJoyCon) and "L" in str(type(self))

    def describe(self):
        """
        Returns a summary: buttons + joystick.
        """
        buttons = self.get_pressed_buttons()
        x, y = self.joystick.get_direction()
        return {
            "buttons": buttons,
            "stick": (x, y)
        }
    
    def execute_command(self):
        for btn in self.get_pressed_buttons():
            self.handler.Treat_command(btn)
    
    def update_joystick(self):
            self.handler.Move_Mouse_Stick(self.joystick)

if __name__ == "__main__":
    import time
    
    joycon = MyJoyCon("R")
    REFRESH_RATE = 0.01   # Seconds between each update


    while True:
        joycon.execute_command()        
        joycon.update_joystick()

        print(joycon.describe())
        time.sleep(REFRESH_RATE)


