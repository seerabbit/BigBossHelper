#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   keyboard.py
@Time    :   2024/06/14 12:10:03
@Author  :   JJJ
@Version :   1.0
@Contact :   seerabbit@hotmail.com
@Desc    :   None
'''

import win32con
import win32gui
import win32api
import time
from ctypes import GetLastError

class Virtual_Keyboard(object):
 
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.hwnd_title = win32gui.GetWindowText(hwnd)
        self.vlaue_key = {
            "A": "65",
            "B": "66",
            "C": "67",
            "D": "68",
            "E": "69",
            "F": "70",
            "G": "71",
            "H": "72",
            "I": "73",
            "J": "74",
            "K": "75",
            "L": "76",
            "M": "77",
            "N": "78",
            "O": "79",
            "P": "80",
            "Q": "81",
            "R": "82",
            "S": "83",
            "T": "84",
            "U": "85",
            "V": "86",
            "W": "87",
            "X": "88",
            "Y": "89",
            "Z": "90",
            "0": "48",
            "1": "49",
            "2": "50",
            "3": "51",
            "4": "52",
            "5": "53",
            "6": "54",
            "7": "55",
            "8": "56",
            "9": "57",
            "F1": "112",
            "F2": "113",
            "F3": "114",
            "F4": "115",
            "F5": "116",
            "F6": "117",
            "F7": "118",
            "F8": "119",
            "F9": "120",
            "F10": "121",
            "F11": "122",
            "F12": "123",
            "TAB": "9",
            "ALT": "18"
        }
 
    # 模拟一次按键的输入，间隔值默认0.1S
    def key_press(self, key: str, interval=0.1):
        key = key.upper()
        key_num = int(self.vlaue_key[key])
        num = win32api.MapVirtualKey(key_num, 0)
        dparam = 1 | (num << 16)
        uparam = 1 | (num << 16) | (1 << 30) | (1 << 31)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, key_num, dparam)
        time.sleep(interval)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, key_num, uparam)
 
    # 模拟一个按键的按下
    def key_down(self, key: str):
        key = key.upper()
        key_num = int(self.vlaue_key[key])
        num1 = win32api.MapVirtualKey(key_num, 0)
        dparam = 1 | (num1 << 16)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, None, dparam)
 
    # 模拟一个按键的弹起
    def key_up(self, key: str):
        key = key.upper()
        key_num = int(self.vlaue_key[key])
        num1 = win32api.MapVirtualKey(key_num, 0)
        uparam = 1 | (num1 << 16) | (1 << 30) | (1 << 31)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, None, uparam)