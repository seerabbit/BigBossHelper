
import threading
import win32gui
from time import sleep

from tkinter import END, IntVar, X, Y, LEFT, RIGHT


class HerbsHelper(threading.Thread):
    INTERVAL = 3
    INTERVAL2 = 20
    INTERVAL3 = 600

    def __init__(self, controler, hwnd = int):
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

        self.controler.ui.tk_input_input_amount_3.config(state="disabled")
        amount = int(self.controler.ui.tk_input_input_amount_3.get())

        sleep(HerbsHelper.INTERVAL)

        for var in range(amount):
            if self.state == "stop":
                break
            # 使用常青袋
            self.keyboard.key_press('1')
            tmp = int(self.controler.ui.tk_input_input_amount_3.get())
            self.controler.ui.tk_input_input_amount_3.config(state="normal")
            self.controler.ui.tk_input_input_amount_3.delete(0, END)
            self.controler.ui.tk_input_input_amount_3.insert(0, tmp - 1)
            self.controler.ui.tk_input_input_amount_3.config(state="disable")
            
            sleep(HerbsHelper.INTERVAL2)
            # 使用草药包
            self.keyboard.key_press('2')

            # 等待10分钟
            sleep(HerbsHelper.INTERVAL3)


        # 结束
        self.state = "idel"
        self.controler.ui.tk_input_input_amount_3.config(state="normal")
        self.controler.ui.tk_button_button_func_3.config(text="Start")

    def stop(self):
        if self.state == "run":
            self.state = "stop"