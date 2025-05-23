import threading
import keyboard
import random

from time import sleep
from utils.Log import DEBUG
from widget.FloatingWindow import FloatingWindow


class PetMode(threading.Thread):
    def __init__(self, controler, hwnd=int):
        super().__init__()
        self.controler = controler
        self.wow_hwnd = hwnd
        self.daemon = True
        self.state = "idel"
        self.keyboard = controler.get_keyboard()
        self.signal = threading.Event()
        self.auto_attack_t = None
        self.attack = False
        self.float_window = None

    def run(self):
        self.state = "run"

        DEBUG("PetMode run")
        self.float_window = FloatingWindow()
        self.float_window.run()
        keyboard.on_press(self.on_key_press)

        self.signal.wait()

        DEBUG("PetMode stop")
        keyboard.unhook_all()
        self.float_window.stop()
        self.float_window = None
        if self.auto_attack_t is not None:
            self.auto_attack_t.stop()
            self.auto_attack_t = None

        # 结束
        self.state = "idel"
        self.controler.ui.tk_button_button_func_4.config(text="Start")

    def stop(self):
        if self.state == "run":
            self.signal.set()
            self.state = "stop"
            self.float_window.stop()
            self.float_window = None

    def on_key_press(self, event):
        DEBUG("press %s" % event.name)
        # attack
        if event.name == "f1":
            self.keyboard.key_press("k")
            if self.auto_attack_t is None:
                self.auto_attack_t = self.AutoAttack(self.controler)
                self.auto_attack_t.start()
                self.attack = True
            self.float_window.blink(True)

        if event.name == "f2":
            if self.auto_attack_t:
                self.auto_attack_t.stop()
                self.auto_attack_t = None
                self.attack = False
            self.keyboard.key_press("l")
            self.float_window.blink(False)

        if event.name == "f3":
            self.keyboard.key_press("f3")
        if event.name == "f4":
            self.keyboard.key_press("f4")
        if event.name == "f5":
            self.keyboard.key_press("f5")

    class AutoAttack(threading.Thread):
        def __init__(self, controler):
            super().__init__()
            self.controler = controler
            self.daemon = True
            self.state = "idel"
            self.keyboard = controler.get_keyboard()

        def run(self):
            self.state = "run"

            DEBUG("AutoAttack run")
            while self.state == "run":
                self.keyboard.key_press("f1")
                sleep(random.uniform(0, 1.5))
            DEBUG("AutoAttack stop")
            # 结束
            self.state = "idel"

        def stop(self):
            if self.state == "run":
                self.state = "stop"
