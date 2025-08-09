from pyjoycon import JoyCon, get_R_id, get_L_id
from src.Command import CommandHandler
from src.Joystick import JoystickDirection
import time
import os

def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# =========================
# Connexion du Joy-Con
# =========================
def wait_for_joycon():
    print("\n----------Phase de connexion----------\n")
    print("En attente de connexion d'un Joy-Con...")
    while True:
        try:
            joycon_id = get_R_id() or get_L_id()
            if joycon_id:
                print("Joy-Con détecté :", joycon_id)
                print("Mannette connectée !")
                return JoyCon(*joycon_id)
        except Exception:
            pass
        time.sleep(1)
        return None

use_joystick = True
use_gyroscope = not use_joystick 

REFRESH_RATE = 0.01   # Secondes entre chaque mise à jour

# =========================
# Boucle principale
# =========================
if __name__ == "__main__":
    handler = CommandHandler()
    joycon = wait_for_joycon()

    if joycon == None :
        ValueError("Mannette non détecté veuillez réessayez ultérieurement")

    joystick = JoystickDirection(joycon, stick="right", calibration_time=5, deadzone=0.1)

    time.sleep(1)
    clear_console()

    print("\n----------Phase de contrôle----------\n")

    while True:
        state = joycon.get_status()["buttons"]["right"]  # Pour Joy-Con droit
        # print(joycon.get_status()["buttons"])
        for button, pressed in state.items():
            if pressed:          
                handler.Treat_command(button)

        if use_joystick : 
            # JoyStick
            handler.Move_Mouse_Stick(joystick)

        if use_gyroscope :
            # Gyroscope
            gyro_data = (joycon.get_gyro_x(),joycon.get_gyro_y())  # (x, y, z)
            handler.Move_Mouse_Gyro(gyro_data[0], gyro_data[1])

        pressed_buttons = [btn for btn, pressed in state.items() if pressed]
        buttons_str = ", ".join(pressed_buttons) if pressed_buttons else "Aucun"

        x, y = joystick.get_direction()
        joystick_str = f"X={x:.2f} Y={y:.2f}"

        print(f"Buttons pressed: {buttons_str}      ")
        print(f"Joystick pos: {joystick_str}       ")
        print("\033[F\033[F", end='')

        time.sleep(REFRESH_RATE)