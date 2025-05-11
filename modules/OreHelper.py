import threading
import win32gui

from time import sleep
from tkinter import END


class OreHelper(threading.Thread):
    INTERVAL = 3

    def __init__(self, controler, hwnd=int):
        super().__init__()
        self.controler = controler
        self.wow_hwnd = hwnd
        self.daemon = True
        self.state = "idel"
        self.keyboard = controler.get_keyboard()

    def run(self):
        self.state = "run"

        if win32gui.IsIconic(self.wow_hwnd):
            win32gui.ShowWindow(self.wow_hwnd, True)
        else:
            win32gui.BringWindowToTop(self.wow_hwnd)
            win32gui.SetForegroundWindow(self.wow_hwnd)

        self.controler.ui.tk_input_input_amount_1.config(state="disabled")
        amount = int(self.controler.ui.tk_input_input_amount_1.get())
        times = int(amount / 5)
        sleep(OreHelper.INTERVAL)
        # 选矿
        for var in range(times):
            if self.state == "stop":
                return
            self.keyboard.key_press("1")
            tmp = int(self.controler.ui.tk_input_input_amount_1.get())
            self.controler.ui.tk_input_input_amount_1.config(state="normal")
            self.controler.ui.tk_input_input_amount_1.delete(0, END)
            self.controler.ui.tk_input_input_amount_1.insert(0, tmp - 5)
            self.controler.ui.tk_input_input_amount_1.config(state="disable")
            sleep(OreHelper.INTERVAL)
        # 结束
        self.state = "idel"
        self.controler.ui.tk_input_input_amount_1.config(state="normal")
        self.controler.ui.tk_button_button_func_1.config(text="Start")

    def stop(self):
        if self.state == "run":
            self.state = "stop"
