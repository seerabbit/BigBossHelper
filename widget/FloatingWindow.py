
from time import sleep
from utils.Log import *
from ttkbootstrap import Button, Scrollbar, Label, Frame, Combobox, Notebook, Checkbutton, LabelFrame, Entry, Style, Toplevel, Canvas
from tkinter import END, IntVar, X, Y, LEFT, RIGHT
from PIL import Image, ImageTk

class FloatingWindow:
        def __init__(self):
            # 原始图片对象需长期保留
            original  = Image.open("icon/attack.png").convert("RGBA")
            # 初始缩放
            initial_size = (100, 100)
            resized = original.resize(initial_size, Image.LANCZOS)
            tk_image = ImageTk.PhotoImage(resized)
            
            self.window = Toplevel(alpha=0)
            self.window.overrideredirect(True)  # 移除标题栏
            self.window.geometry("100x100+500+300")  # 初始位置和大小
            self.window.config(bg="white", highlightthickness=0)
            self.window.attributes("-transparentcolor", "white")  # Windows透明属性
            self.window.attributes('-topmost', 'true')
            
            # 显示组件
            label = Label(self.window, image=tk_image, background="white")
            label.image = tk_image
            label.pack(expand=True, fill="both")

            # 绑定事件
            label.bind("<ButtonPress-1>", self.start_drag)
            label.bind("<B1-Motion>", self.on_drag)

            self.window.wm_attributes("-alpha", 1)
            self.blinker = self.AlphaBlinker(self.window, min_alpha=0.3, interval=25)

        def start_drag(self, event):
            # 记录初始位置
            self.start_x = event.x_root  # 鼠标绝对坐标
            self.start_y = event.y_root
            self.original_x = self.window.winfo_x()  # 窗口左上角坐标
            self.original_y = self.window.winfo_y()

        def on_drag(self, event):
            # 计算偏移量并更新窗口位置
            delta_x = event.x_root - self.start_x
            delta_y = event.y_root - self.start_y
            new_x = self.original_x + delta_x
            new_y = self.original_y + delta_y
            self.window.geometry(f"+{new_x}+{new_y}")  # 更新窗口坐标

        def run(self):
            INFO("floating window run")

        def stop(self):
            INFO("floating window stop")
            self.window.destroy()

        def blink(self, enable):
            INFO("floating window blink")
            if enable:
                self.blinker.start()
            else:
                self.blinker.stop()

        class AlphaBlinker:
            def __init__(self, toplevel, min_alpha=0.3, max_alpha=1.0, interval=50):
                """
                :param toplevel: 目标窗口对象
                :param min_alpha: 最小透明度 (0.0-1.0)
                :param max_alpha: 最大透明度 (0.0-1.0)
                :param interval: 透明度变化间隔 (毫秒)
                """
                self.toplevel = toplevel
                self.min_alpha = min_alpha
                self.max_alpha = max_alpha
                self.interval = interval
                self.step = 0.05  # 每次透明度变化步长
                self.current_alpha = max_alpha
                self.is_increasing = False  # 当前是否处于透明度上升阶段
                self._blink_id = None

            def _animate(self):
                # 计算下一阶段的透明度
                if self.is_increasing:
                    self.current_alpha += self.step
                    if self.current_alpha >= self.max_alpha:
                        self.current_alpha = self.max_alpha
                        self.is_increasing = False  # 下一阶段改为下降
                else:
                    self.current_alpha -= self.step
                    if self.current_alpha <= self.min_alpha:
                        self.current_alpha = self.min_alpha
                        self.is_increasing = True  # 下一阶段改为上升

                # 更新窗口透明度
                self.toplevel.attributes('-alpha', self.current_alpha)
        
                # 继续执行动画
                self._blink_id = self.toplevel.after(self.interval, self._animate)

            def start(self):
                """开始闪烁"""
                if not self._blink_id:
                    self.current_alpha = self.max_alpha
                    self.is_increasing = False
                    self._animate()

            def stop(self):
                """停止闪烁并恢复默认"""
                if self._blink_id:
                    self.toplevel.after_cancel(self._blink_id)
                    self._blink_id = None
                    self.toplevel.attributes('-alpha', self.max_alpha)