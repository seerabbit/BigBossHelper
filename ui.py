import configparser
import ctypes

import os
import random
from tkinter import StringVar, Tk
# from tkinter.ttk import *
from tkinter.font import Font
from ttkbootstrap import Button, Scrollbar, Label, Frame, Combobox, Notebook, Checkbutton, LabelFrame, Entry, Style, Toplevel
# from ttkbootstrap import *
from utils.Log import *
from utils.PassWord import KeyWorks

BUILD_VERSION = "V1.1.1"

class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_select_box_select_win = self.__tk_select_box_select_win(self)
        self.tk_tabs_notebook = self.__tk_tabs_notebook(self)
        
        # notebook0
        self.tk_label_frame_func_1 = self.__tk_label_frame_func_1( self.tk_tabs_notebook_0)
        self.tk_label_lable_amount_1 = self.__tk_label_lable_amount_func_1( self.tk_label_frame_func_1) 
        self.tk_input_input_amount_1 = self.__tk_input_input_amount_func_1( self.tk_label_frame_func_1) 
        self.tk_button_button_func_1 = self.__tk_button_button_func_1( self.tk_label_frame_func_1) 

        self.tk_label_frame_func_3 = self.__tk_label_frame_func_3( self.tk_tabs_notebook_0)
        self.tk_label_lable_amount_3 = self.__tk_label_lable_amount_func_3( self.tk_label_frame_func_3) 
        self.tk_input_input_amount_3 = self.__tk_input_input_amount_func_3( self.tk_label_frame_func_3) 
        self.tk_button_button_func_3 = self.__tk_button_button_func_3( self.tk_label_frame_func_3)

        # notebook1
        self.tk_label_frame_func_2 = self.__tk_label_frame_func_2( self.tk_tabs_notebook_1)
        self.tk_check_button_func_1 = self.__tk_check_button_func_1( self.tk_label_frame_func_2)
        self.tk_check_button_func_2 = self.__tk_check_button_func_2( self.tk_label_frame_func_2)
        self.tk_check_button_func_3 = self.__tk_check_button_func_3( self.tk_label_frame_func_2)
        self.tk_button_button_func_2 = self.__tk_button_button_func_2( self.tk_label_frame_func_2)

        self.tk_label_frame_func_4 = self.__tk_label_frame_func_4( self.tk_tabs_notebook_1)
        self.tk_button_button_func_4 = self.__tk_button_button_func_4( self.tk_label_frame_func_4)


    def __win(self):
        # 设置标题
        self.title("BigBossHelper_%s" % BUILD_VERSION)
        # 禁用DPI缩放
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        INFO("[ScaleFactor] %d" % ScaleFactor)
        self.call('tk', 'scaling', ScaleFactor/75)
        self.scaleFactor=ScaleFactor/100
        # 设置窗口大小、居中
        width = 600*self.scaleFactor
        height = 400*self.scaleFactor
        screenwidth = self.winfo_screenwidth() * ScaleFactor /100
        screenheight = self.winfo_screenheight() * ScaleFactor / 100
        # screenwidth = self.winfo_screenwidth()
        # screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)
        # 置顶窗口
        self.attributes('-topmost', 'true')
        # 设置窗口图标
        self.iconbitmap("icon/title.ico")
        # 设置主题
        style = Style()
        style.theme_use("sandstone")
        
    def scrollbar_autohide(self,vbar, hbar, widget):
        """自动隐藏滚动条"""
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())
    
    def v_scrollbar(self,vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')
    def h_scrollbar(self,hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')
    def create_bar(self,master, widget,is_vbar,is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)

    # 选择应用
    def __tk_select_box_select_win(self,parent):
        font_size = int(8*self.scaleFactor)
        font = Font(family='微软雅黑', size=font_size)
        cb = Combobox(parent, state="readonly", justify="left", font=font )
        cb['values'] = ("选择程序")
        cb.place(x=20*self.scaleFactor, y=20*self.scaleFactor, width=560*self.scaleFactor, height=30*self.scaleFactor)
        cb.set("选择程序")
        return cb
    
    # 标签页
    def __tk_tabs_notebook(self,parent):
        frame = Notebook(parent)
        self.tk_tabs_notebook_0 = self.__tk_frame_notebook_0(frame)
        frame.add(self.tk_tabs_notebook_0, text="商业")
        self.tk_tabs_notebook_1 = self.__tk_frame_notebook_1(frame)
        frame.add(self.tk_tabs_notebook_1, text="协作")
        frame.place(x=20*self.scaleFactor, y=75*self.scaleFactor, width=560*self.scaleFactor, height=305*self.scaleFactor)
        return frame
    def __tk_frame_notebook_0(self,parent):
        frame = Frame(parent)
        frame.place(x=20*self.scaleFactor, y=75*self.scaleFactor, width=560*self.scaleFactor, height=305*self.scaleFactor)
        return frame
    def __tk_frame_notebook_1(self,parent):
        frame = Frame(parent)
        frame.place(x=20*self.scaleFactor, y=75*self.scaleFactor, width=560*self.scaleFactor, height=305*self.scaleFactor)
        return frame
    
    # 选矿
    def __tk_label_frame_func_1(self,parent):
        frame = LabelFrame(parent,text="选矿",)
        frame.place(x=10*self.scaleFactor, y=15*self.scaleFactor, width=535*self.scaleFactor, height=80*self.scaleFactor)
        return frame
    def __tk_label_lable_amount_func_1(self,parent):
        label = Label(parent,text="数量",anchor="center", )
        label.place(x=0*self.scaleFactor, y=10*self.scaleFactor, width=70*self.scaleFactor, height=30*self.scaleFactor)
        return label
    def __tk_input_input_amount_func_1(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=70*self.scaleFactor, y=10*self.scaleFactor, width=80*self.scaleFactor, height=30*self.scaleFactor)
        return ipt
    def __tk_button_button_func_1(self,parent):
        btn = Button(parent, text="Start", takefocus=False, padding="center")
        btn.place(x=460*self.scaleFactor, y=10*self.scaleFactor, width=60*self.scaleFactor, height=30*self.scaleFactor)
        return btn
    
    # 常青袋子
    def __tk_label_frame_func_3(self,parent):
        frame = LabelFrame(parent,text="常青袋",)
        frame.place(x=10*self.scaleFactor, y=100*self.scaleFactor, width=535*self.scaleFactor, height=80*self.scaleFactor)
        return frame
    def __tk_label_lable_amount_func_3(self,parent):
        label = Label(parent,text="数量",anchor="center", )
        label.place(x=0*self.scaleFactor, y=10*self.scaleFactor, width=70*self.scaleFactor, height=30*self.scaleFactor)
        return label
    def __tk_input_input_amount_func_3(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=70*self.scaleFactor, y=10*self.scaleFactor, width=80*self.scaleFactor, height=30*self.scaleFactor)
        return ipt
    def __tk_button_button_func_3(self,parent):
        btn = Button(parent, text="Start", takefocus=False, padding="center")
        btn.place(x=460*self.scaleFactor, y=10*self.scaleFactor, width=60*self.scaleFactor, height=30*self.scaleFactor)
        return btn
    
    # 按键协作
    def __tk_label_frame_func_2(self,parent):
        frame = LabelFrame(parent,text="智能助手",)
        frame.place(x=10*self.scaleFactor, y=15*self.scaleFactor, width=535*self.scaleFactor, height=80*self.scaleFactor)
        return frame
    def __tk_check_button_func_1(self,parent):
        cb = Checkbutton(parent, text="镜像模式", onvalue=1, offvalue=0)
        cb.place(x=10*self.scaleFactor, y=10*self.scaleFactor, width=70*self.scaleFactor, height=30*self.scaleFactor)
        return cb
    def __tk_check_button_func_2(self,parent):
        cb = Checkbutton(parent, text="交互键", onvalue=1, offvalue=0)
        cb.place(x=100*self.scaleFactor, y=10*self.scaleFactor, width=70*self.scaleFactor, height=30*self.scaleFactor)
        return cb
    def __tk_check_button_func_3(self,parent):
        cb = Checkbutton(parent, text="自动跟随", onvalue=1, offvalue=0)
        cb.place(x=180*self.scaleFactor, y=10*self.scaleFactor, width=70*self.scaleFactor, height=30*self.scaleFactor)
        return cb
    def __tk_button_button_func_2(self,parent):
        btn = Button(parent, text="Start", takefocus=False, padding="center")
        btn.place(x=460*self.scaleFactor, y=10*self.scaleFactor, width=60*self.scaleFactor, height=30*self.scaleFactor)
        return btn
    
    # PetMode
    def __tk_label_frame_func_4(self, parent):
        frame = LabelFrame(parent,text="PetMode",)
        frame.place(x=10*self.scaleFactor, y=100*self.scaleFactor, width=535*self.scaleFactor, height=80*self.scaleFactor)
        return frame
    def __tk_button_button_func_4(self,parent):
        btn = Button(parent, text="Start", takefocus=False, padding="center")
        btn.place(x=460*self.scaleFactor, y=10*self.scaleFactor, width=60*self.scaleFactor, height=30*self.scaleFactor)
        return btn
    
class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)
        self.password = StringVar()

        config = configparser.ConfigParser()
        config.read('config.ini')
        INFO("Login %s" % config.has_section('login'))
        if not config.has_section('login'):
           self.__lock()
           self.login()
        
        # self.__lock()
        # self.login()

    def __event_bind(self):
        self.tk_select_box_select_win.bind('<<ComboboxSelected>>',self.ctl.onSelected)
        self.tk_button_button_func_1.bind('<Button-1>',self.ctl.onClick)
        self.tk_button_button_func_2.bind('<Button-1>',self.ctl.onClick2)
        self.tk_button_button_func_3.bind('<Button-1>',self.ctl.onClick3)
        self.tk_button_button_func_4.bind('<Button-1>',self.ctl.onClick4)
        self.bind('<FocusIn>', self.ctl.onWindowFocusIn)
        pass
    def __style_config(self):
        pass

    def on_closing(self):
        INFO("EXIT")
        self.destroy()

    def __lock(self):
        self.attributes("-disabled", True)

    def __unlock(self):
        self.attributes("-disabled", False)

    def __on_login(self):
        DEBUG("[PASSWORD] key %s" % self.key)
        DEBUG("[PASSWORD] password %s" % self.password.get())
        if self.password.get() == KeyWorks.get(self.key, None):
            config = configparser.ConfigParser()
            config.add_section('login')
            with open('config.ini', 'w', encoding='UTF-8') as file:
                config.write(file)
            self.__unlock()
            self.login_window.destroy()


    def login(self):
        login = Toplevel(self)
        self.login_window = login
        
        # 设置标题
        login.title("用户登录")

        # 设置窗口大小、居中
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        width = 300*self.scaleFactor
        height = 200*self.scaleFactor
        screenwidth = self.winfo_screenwidth() * ScaleFactor /100
        screenheight = self.winfo_screenheight() * ScaleFactor / 100
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        login.geometry(geometry)
        login.resizable(width=False, height=False)
        # 置顶窗口
        login.attributes('-topmost', 'true')
        # 设置窗口图标
        login.iconbitmap("icon/title.ico")

        INFO("[USER] %s" % os.getlogin())
        INFO("[PATH] %s" % os.getcwd())

        login.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.key = random.choice(list(KeyWorks.keys()))
        
        label = Label(login,text=self.key, anchor="center")
        label.pack(anchor='center', pady=20*self.scaleFactor)
        ipt = Entry(login, textvariable=self.password)
        ipt.pack(anchor='center', pady=20*self.scaleFactor)
        btn = Button(login, text="确定", takefocus=False, padding="center", command=self.__on_login)
        btn.pack(anchor='center', pady=20*self.scaleFactor)

if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()