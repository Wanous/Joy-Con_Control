from pyjoycon import JoyCon, get_R_id, get_L_id
from pynput.keyboard import Controller, Key
from pynput.mouse import Controller as MouseController, Button
from src.Joystick import JoystickDirection
import pyautogui
import time
# =========================
# Classe pour exécuter des commandes
# =========================
class CommandHandler:
    def __init__(self):
        self.keyboard = Controller()
        self.mouse = MouseController()
        
        self.GYRO_SENSITIVITY = 0.05
        self.STICK_SENSITIVITY = 30
        self.MOUSE_CLICK_TIME = 0.1
    
    def Treat_command(self, command):
        if command == "y":
            self.Left_Arrow()
        elif command == "a":
            self.Right_Arrow()
        elif command == "x":
            self.Up_Arrow()
        elif command == "b":
            self.Down_Arrow()
        elif command == "r":
            self.Click_Left()
        elif command == "zr":
            self.Center_Mouse()

    def Left_Arrow(self):
        # print("Simule flèche gauche")
        self.keyboard.press(Key.left)
        self.keyboard.release(Key.left)

    def Right_Arrow(self):
        # print("Simule flèche droite")
        self.keyboard.press(Key.right)
        self.keyboard.release(Key.right)

    def Up_Arrow(self):
        # print("Simule flèche haut")
        self.keyboard.press(Key.up)
        self.keyboard.release(Key.up)

    def Down_Arrow(self):
        # print("Simule flèche bas")
        self.keyboard.press(Key.down)
        self.keyboard.release(Key.down)

    def Click_Left(self):
        self.mouse.click(Button.left)
        time.sleep(self.MOUSE_CLICK_TIME)

    def Move_Mouse_Gyro(self, gyro_x, gyro_y):
        dx = int(gyro_y * self.GYRO_SENSITIVITY)   # inversion X/Y pour correspondre aux mouvements réels
        dy = int(-gyro_x * self.GYRO_SENSITIVITY)  # signe négatif pour mouvement naturel
        if dx != 0 or dy != 0:
            pos = self.mouse.position
            self.mouse.position = (pos[0] + dx, pos[1] + dy)
    
    def Move_Mouse_Stick(self, joystick:JoystickDirection):
            x, y = joystick.get_direction()
            self.mouse.move(x * self.STICK_SENSITIVITY, -y * self.STICK_SENSITIVITY)

    def Center_Mouse(self):
        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2
        self.mouse.position = (center_x, center_y)

