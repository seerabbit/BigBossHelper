
import threading
import win32gui
import keyboard
from time import sleep
from tkinter import END, IntVar 
from tkinter import messagebox

from tools.virtual_keyboard import Virtual_Keyboard
from utils.Log import *

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
        INFO("onClick <Button-1> 事件处理: %s" % evt)
        
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
        INFO("onClick2 <Button-1> 事件处理: %s" % evt)
       
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
        INFO("onClick3 <Button-1> 事件处理: %s" % evt)
        
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
        INFO("onClick4 <Button-1> 事件处理: %s" % evt)
       
        if (self.ui.tk_button_button_func_4.cget("text") == "Stop"):
            self.ui.tk_button_button_func_4.config(text="Start")
            if self.petmode_t:
                self.petmode_t.stop()
        else:
            if self.hwnd is None:
                messagebox.showerror("", "没有绑定WoW窗口?")
                return
            
            self.ui.tk_button_button_func_4.config(text="Stop")
            self.petmode_t = PetMode(self, self.hwnd, self.mirror.get(), self.interact.get())
            self.petmode_t.start()


class OreHelper(threading.Thread):
    INTERVAL = 3

    def __init__(self, controler = Controller, hwnd = int):
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
            self.keyboard.key_press('1')
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
        
class HerbsHelper(threading.Thread):
    INTERVAL = 3
    INTERVAL2 = 20
    INTERVAL3 = 600

    def __init__(self, controler = Controller, hwnd = int):
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
     
class KeyHelper(threading.Thread):

    def __init__(self, controler = Controller, hwnd = int, mirror = int, interact = int):
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
                self.keyboard.key_press('1')
            elif event.name == "2":
                self.keyboard.key_press('2')
            elif event.name == "3":
                self.keyboard.key_press('3')
            elif event.name == "4":
                self.keyboard.key_press('4')
            elif event.name == "5":
                self.keyboard.key_press('5')
            elif event.name == "f1":
                self.keyboard.key_press('f1')
            elif event.name == "f2":
                self.keyboard.key_press('f2')
            elif event.name == "f3":
                self.keyboard.key_press('f3')
            elif event.name == "f4":
                self.keyboard.key_press('f4')
            elif event.name == "f5":
                self.keyboard.key_press('f5')
        else:
            if event.name == "f1":
                self.keyboard.key_press('1')
            elif event.name == "f2":
                self.keyboard.key_press('2')
            elif event.name == "f3":
                self.keyboard.key_press('3')
            elif event.name == "f4":
                self.keyboard.key_press('4')
            elif event.name == "f5":
                self.keyboard.key_press('5')
            elif event.name == "f6":
                self.keyboard.key_press('6')
            elif event.name == "f7":
                self.keyboard.key_press('7')
            elif event.name == "f8":
                self.keyboard.key_press('8')
            elif event.name == "f9":
                self.keyboard.key_press('9')
        if self.interact:
            if event.name == "f":
                self.keyboard.key_press('f')

class AutoFollow(threading.Thread):

    def __init__(self, controler = Controller, hwnd = int):
        super().__init__()
        self.controler = controler
        self.wow_hwnd = hwnd
        self.daemon = True
        self.state = "idel"
        self.keyboard = controler.get_keyboard()

    def run(self):
        self.state = "run"

        DEBUG("AutoFollow run")
        while(self.state == 'run'):
            self.keyboard.key_press('l')
            sleep(1)
        DEBUG("AutoFollow stop")
        # 结束
        self.state = "idel"

    def stop(self):
        if self.state == "run":
            self.state = "stop"

class PetMode(threading.Thread):
    def __init__(self, controler = Controller, hwnd = int):
        super().__init__()
        self.controler = controler
        self.wow_hwnd = hwnd
        self.daemon = True
        self.state = "idel"
        self.keyboard = controler.get_keyboard()
        self.signal = threading.Event()
        self.auto_attack_t = None
        self.auto_follow_t = None

    def run(self):
        self.state = "run"

        DEBUG("PetMode run")
        keyboard.on_press(self.on_key_press)

        self.signal.wait()

        DEBUG("PetMode stop")
        keyboard.unhook_all()
        if self.auto_attack_t != None:
            self.auto_attack_t.stop()
            self.auto_attack_t = None
        if self.auto_follow_t != None:
            self.auto_follow_t.stop()
            self.auto_follow_t = None

        # 结束
        self.state = "idel"
        self.controler.ui.tk_button_button_func_4.config(text="Start")

    def stop(self):
        if self.state == "run":
            self.signal.set()
            self.state = "stop"

    def on_key_press(self, event):
        DEBUG("press %s" % event.name)
        # attack
        if event.name == "f1":
            if self.auto_attack_t == None:
                self.auto_attack_t = self.AutoAttack(self.controler)
                self.auto_attack_t.start()
            else:
                self.auto_attack_t.stop()
                self.auto_attack_t = None

        if event.name == "f2":
            if self.auto_follow_t == None:
                self.auto_follow_t = self.AutoFollow(self.controler)
                self.auto_follow_t.start()
            else:
                self.auto_follow_t.stop()
                self.auto_follow_t = None

        if event.name == "f3":
            self.keyboard.key_press('f3')
        if event.name == "f4":
            self.keyboard.key_press('f4')
        if event.name == "f5":
            self.keyboard.key_press('f5')

    class AutoAttack(threading.Thread):

        def __init__(self, controler = Controller):
            super().__init__()
            self.controler = controler
            self.daemon = True
            self.state = "idel"
            self.keyboard = controler.get_keyboard()

        def run(self):
            self.state = "run"

            DEBUG("AutoAttack run")
            while(self.state == 'run'):
                self.keyboard.key_press('f1')
                sleep(1)
            DEBUG("AutoAttack stop")
            # 结束
            self.state = "idel"

        def stop(self):
            if self.state == "run":
                self.state = "stop"

    class AutoFollow(threading.Thread):

        def __init__(self, controler = Controller,):
            super().__init__()
            self.controler = controler
            self.daemon = True
            self.state = "idel"
            self.keyboard = controler.get_keyboard()

        def run(self):
            self.state = "run"

            DEBUG("AutoFollow run")
            while(self.state == 'run'):
                self.keyboard.key_press('f2')
                sleep(1)
            DEBUG("AutoFollow stop")
            # 结束
            self.state = "idel"

        def stop(self):
            if self.state == "run":
                self.state = "stop"