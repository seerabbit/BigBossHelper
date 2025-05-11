import threading

from time import sleep
from utils.Log import DEBUG


class AutoFollow(threading.Thread):
    def __init__(self, controler, hwnd=int):
        super().__init__()
        self.controler = controler
        self.wow_hwnd = hwnd
        self.daemon = True
        self.state = "idel"
        self.keyboard = controler.get_keyboard()

    def run(self):
        self.state = "run"

        DEBUG("AutoFollow run")
        while self.state == "run":
            self.keyboard.key_press("l")
            sleep(1)
        DEBUG("AutoFollow stop")
        # 结束
        self.state = "idel"

    def stop(self):
        if self.state == "run":
            self.state = "stop"
