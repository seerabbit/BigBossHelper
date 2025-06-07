import threading
from time import sleep

from utils.Log import DEBUG


class Jump(threading.Thread):
    def __init__(self, controler):
        super().__init__()
        self.controler = controler
        self.daemon = True
        self.state = "idel"
        self.keyboard = controler.get_keyboard()
        self.signal = threading.Event()

    def run(self):
        self.state = "run"

        DEBUG("Jump run")
        sleep(0.5)
        self.keyboard.key_press("space")
        DEBUG("Jump stop")