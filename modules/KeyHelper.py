import threading
import keyboard

from utils.Log import DEBUG


class KeyHelper(threading.Thread):
    def __init__(self, controler, hwnd=int, mirror=int, interact=int):
        super().__init__()
        self.controler = controler
        self.wow_hwnd = hwnd
        self.daemon = True
        self.state = "idel"
        self.mirror = mirror
        self.interact = interact
        self.keyboard = controler.get_keyboard()
        self.signal = threading.Event()

    def run(self):
        self.state = "run"

        DEBUG("KeyHelper run")
        keyboard.on_press(self.on_key_press)

        self.signal.wait()

        DEBUG("KeyHelper stop")
        keyboard.unhook_all()
        # 结束
        self.state = "idel"
        self.controler.ui.tk_button_button_func_2.config(text="Start")

    def stop(self):
        if self.state == "run":
            self.signal.set()
            self.state = "stop"

    def on_key_press(self, event):
        DEBUG("press %s" % event.name)
        if self.mirror:
            if event.name == "1":
                self.keyboard.key_press("1")
            elif event.name == "2":
                self.keyboard.key_press("2")
            elif event.name == "3":
                self.keyboard.key_press("3")
            elif event.name == "4":
                self.keyboard.key_press("4")
            elif event.name == "5":
                self.keyboard.key_press("5")
            elif event.name == "f1":
                self.keyboard.key_press("f1")
            elif event.name == "f2":
                self.keyboard.key_press("f2")
            elif event.name == "f3":
                self.keyboard.key_press("f3")
            elif event.name == "f4":
                self.keyboard.key_press("f4")
            elif event.name == "f5":
                self.keyboard.key_press("f5")
        else:
            if event.name == "f1":
                self.keyboard.key_press("1")
            elif event.name == "f2":
                self.keyboard.key_press("2")
            elif event.name == "f3":
                self.keyboard.key_press("3")
            elif event.name == "f4":
                self.keyboard.key_press("4")
            elif event.name == "f5":
                self.keyboard.key_press("5")
            elif event.name == "f6":
                self.keyboard.key_press("6")
            elif event.name == "f7":
                self.keyboard.key_press("7")
            elif event.name == "f8":
                self.keyboard.key_press("8")
            elif event.name == "f9":
                self.keyboard.key_press("9")
        if self.interact:
            if event.name == "f":
                self.keyboard.key_press("f")
