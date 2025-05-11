
import threading
import win32gui
import keyboard
from time import sleep

from tkinter import messagebox
from modules.AutoFollow import AutoFollow
from modules.HerbsHelper import HerbsHelper
from modules.KeyHelper import KeyHelper
from modules.OreHelper import OreHelper
from modules.PetMode import PetMode
from tools.virtual_keyboard import Virtual_Keyboard
from utils.Log import *
from tkinter import END, IntVar, X, Y, LEFT, RIGHT

class Controller:
    # 导入UI类后，替换以下的 object 类型，将获得 IDE 属性提示功能
    ui: object
    def __init__(self):
        pass
    def init(self, ui):
        """
        得到UI实例,对组件进行初始化配置
        """
        self.ui = ui
        # TODO 组件初始化 赋值操作
        self.hwnd = None
        self.keyboard = None
        self.mirror = IntVar()
        self.interact = IntVar()
        self.follow = IntVar()
        self.keyhelper_t = None
        self.follow_t = None
        self.petmode_t = None
        self.__check_button_init()

    def __find_window(self, hwnd, windows = list):
        if win32gui.GetWindowText(hwnd) == '魔兽世界':
            temp = []
            temp.append(hex(hwnd))
            temp.append(win32gui.GetClassName(hwnd))
            temp.append(win32gui.GetWindowText(hwnd))
            windows.append(temp)

    def __combobox_init(self):
        hwnd_list = []
        win32gui.EnumWindows(self.__find_window, hwnd_list)
        if len(hwnd_list) > 0:
            self.ui.tk_select_box_select_win.config(values=hwnd_list)

    def __check_button_init(self):
        self.ui.tk_check_button_func_1.config(variable=self.mirror)
        self.mirror.set(0)
        self.ui.tk_check_button_func_2.config(variable=self.interact)
        self.interact.set(0)
        self.ui.tk_check_button_func_3.config(variable=self.follow)
        self.follow.set(0)

    def get_keyboard(self):
        self.keyboard = Virtual_Keyboard(self.hwnd)
        return self.keyboard
    
    def onWindowFocusIn(self,evt):
        self.__combobox_init() 

    def onSelected(self,evt):
        INFO("onSelected <ComboboxSelected> 事件处理: %s" % evt)
        selected_value = evt.widget.get()
        if selected_value == 'Application':
            messagebox.showerror('Title', 'Its not Application')
        else:
            windows = selected_value.split()
            hwnd = int(windows[0], 16)
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, True)
            else:
                win32gui.BringWindowToTop(hwnd)
                win32gui.SetForegroundWindow(hwnd)
            sleep(0.5)
            value = messagebox.askquestion('', '是否控制当前WoW窗口')
            DEBUG("onSelected: %s" % value)
            if value == 'yes':
               self.hwnd = hwnd
               self.keyboard = Virtual_Keyboard(self.hwnd)

    def onClick(self,evt):
        INFO("OreHelper <Button-1> 事件处理: %s" % evt)
        
        if (self.ui.tk_button_button_func_1.cget("text") == "Stop"):
            self.ui.tk_button_button_func_1.config(text="Start")
            self.orehelper_t.stop()
        else:
            if self.hwnd is None:
                messagebox.showerror("", "没有绑定WoW窗口?")
                return
            else:
                if win32gui.IsIconic(self.hwnd):
                    win32gui.ShowWindow(self.hwnd, True)
                else:
                    win32gui.BringWindowToTop(self.hwnd)
                    win32gui.SetForegroundWindow(self.hwnd)
            self.ui.tk_button_button_func_1.config(text="Stop")
            self.orehelper_t = OreHelper(self, self.hwnd)
            self.orehelper_t.start()

    def onClick2(self,evt):
        INFO("KeyHelper <Button-1> 事件处理: %s" % evt)
       
        if (self.ui.tk_button_button_func_2.cget("text") == "Stop"):
            self.ui.tk_button_button_func_2.config(text="Start")
            if self.keyhelper_t:
                self.keyhelper_t.stop()
            if self.follow_t:
                self.follow_t.stop()
            self.ui.tk_check_button_func_1.config(state="active")
            self.ui.tk_check_button_func_2.config(state="active")
            self.ui.tk_check_button_func_3.config(state="active")
        else:
            if self.hwnd is None:
                messagebox.showerror("", "没有绑定WoW窗口?")
                return
            
            self.ui.tk_button_button_func_2.config(text="Stop")
            INFO("mirror mode: %d" % self.mirror.get())
            self.ui.tk_check_button_func_1.config(state="disabled")
            self.ui.tk_check_button_func_2.config(state="disabled")
            self.ui.tk_check_button_func_3.config(state="disabled")

            self.keyhelper_t = KeyHelper(self, self.hwnd, self.mirror.get(), self.interact.get())
            self.keyhelper_t.start()

            if self.follow.get():
                self.follow_t = AutoFollow(self, self.hwnd)
                self.follow_t.start()


    def onClick3(self,evt):
        INFO("HerbsHelper <Button-1> 事件处理: %s" % evt)
        
        if (self.ui.tk_button_button_func_3.cget("text") == "Stop"):
            self.ui.tk_button_button_func_3.config(text="Start")
            self.herbshelper_t.stop()
            self.state = "idel"
            self.ui.tk_input_input_amount_3.config(state="normal")
            self.ui.tk_button_button_func_3.config(text="Start")
        else:
            if self.hwnd is None:
                messagebox.showerror("", "没有绑定WoW窗口?")
                return
            else:
                if win32gui.IsIconic(self.hwnd):
                    win32gui.ShowWindow(self.hwnd, True)
                else:
                    win32gui.BringWindowToTop(self.hwnd)
                    win32gui.SetForegroundWindow(self.hwnd)
            self.ui.tk_button_button_func_3.config(text="Stop")
            self.herbshelper_t = HerbsHelper(self, self.hwnd)
            self.herbshelper_t.start()

    def onClick4(self,evt):
        INFO("PetMode <Button-1> 事件处理: %s" % evt)
       
        if (self.ui.tk_button_button_func_4.cget("text") == "Stop"):
            self.ui.tk_button_button_func_4.config(text="Start")
            if self.petmode_t:
                self.petmode_t.stop()
        else:
            if self.hwnd is None:
                messagebox.showerror("", "没有绑定WoW窗口?")
                return
            
            self.ui.tk_button_button_func_4.config(text="Stop")
            self.petmode_t = PetMode(self, self.hwnd)
            self.petmode_t.start()
     



