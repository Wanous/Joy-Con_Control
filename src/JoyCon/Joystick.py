import time
from pyjoycon import JoyCon, get_R_id
from pynput.mouse import Controller as MouseController

class JoystickDirection:
    def __init__(self, joycon, stick="right", calibration_time=5, deadzone=0.1):

        self.joycon = joycon
        self.stick = stick
        self.calibration_time = calibration_time
        self.deadzone = deadzone

        self.x_min = float('inf')
        self.x_max = float('-inf')
        self.y_min = float('inf')
        self.y_max = float('-inf')
        self.x_center = 0
        self.y_center = 0

        self.calibrate()

    def calibrate(self):
        print("\n----------Phase de calibration----------\n")
        print(f"Calibration du joystick {self.stick}... Bougez-le dans toutes les directions pendant {self.calibration_time} sec.")
        start = time.time()
        while time.time() - start < self.calibration_time:
            raw = self._get_stick_raw()
            x, y = raw["x"], raw["y"]

            if x < self.x_min: self.x_min = x
            if x > self.x_max: self.x_max = x
            if y < self.y_min: self.y_min = y
            if y > self.y_max: self.y_max = y

            time.sleep(0.01)

        self.x_center = (self.x_min + self.x_max) / 2
        self.y_center = (self.y_min + self.y_max) / 2

        print(f"Calibration terminée.")
        print("\n----------Calibration----------\n")

        print(f"X : min={self.x_min}, center={self.x_center}, max={self.x_max}")
        print(f"Y : min={self.y_min}, center={self.y_center}, max={self.y_max}")

    def _get_stick_raw(self):
        if self.stick == "right":
            return {'x':self.joycon.get_stick_right_horizontal(),'y':self.joycon.get_stick_right_vertical() }
        else:
            return {'x':self.joycon.get_stick_left_horizontal(),'y':self.joycon.get_left_right_vertical() }

    def _normalize(self, value, min_val, center_val, max_val):
        if value >= center_val:
            return (value - center_val) / (max_val - center_val)
        else:
            return (value - center_val) / (center_val - min_val)

    def get_direction(self):
        """Retourne un tuple (x, y) normalisé dans [-1, 1], avec deadzone appliquée."""
        raw = self._get_stick_raw()
        x = self._normalize(raw["x"], self.x_min, self.x_center, self.x_max)
        y = self._normalize(raw["y"], self.y_min, self.y_center, self.y_max)

        if abs(x) < self.deadzone:
            x = 0
        if abs(y) < self.deadzone:
            y = 0

        return (x, y)
    
    def Display_Data(self):
        data = joystick.get_direction()
        print("x:",data[0],", y",data[1])


# Test
if __name__ == "__main__":
    joycon_id = get_R_id()
    joycon = JoyCon(*joycon_id)
    mouse = MouseController()

    joystick = JoystickDirection(joycon, stick="right", calibration_time=5, deadzone=0.1)

    print("Contrôle de la souris avec joystick (CTRL+C pour quitter)")
    try:
        while True:
            x, y = joystick.get_direction()
            mouse.move(x * 15, -y * 15)
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\nArrêt.")
