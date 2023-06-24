import re

import pydirectinput
import pyperclip

from Event.Event import Event
from loguru import logger

import ctypes
import win32con
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
numofmonitors = user32.GetSystemMetrics(win32con.SM_CMONITORS)
# 主屏分辨率
SW, SH = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


class WindowsEvent(Event):
    # 改变坐标
    # pos 为包含横纵坐标的元组
    # 值为int型:绝对坐标
    # 值为float型:相对坐标
    def changepos(self, pos: tuple):
        if self.event_type == 'EM':
            x, y = pos
            if isinstance(x, int):
                self.action[0] = int(x * 65535 / SW)
            else:
                self.action[0] = int(x * 65535)
            if isinstance(y, int):
                self.action[1] = int(y * 65535 / SH)
            else:
                self.action[1] = int(y * 65535)

    # 执行操作
    def execute(self, thd=None):
        self.sleep(thd)

        if self.event_type == 'EM':
            x, y = self.action
            # 兼容旧版的绝对坐标
            if not isinstance(x, int) and not isinstance(y, int):
                x = float(re.match('([0-1].[0-9]+)%', x).group(1))
                y = float(re.match('([0-1].[0-9]+)%', y).group(1))

            if self.action == [-1, -1]:
                # 约定 [-1, -1] 表示鼠标保持原位置不动
                pass
            else:
                pydirectinput.moveTo(int(x*SW), int(y*SH))

            if self.message == 'mouse left down':
                pydirectinput.mouseDown(None, None, 'left')
            elif self.message == 'mouse left up':
                pydirectinput.mouseUp(None, None, 'left')
            elif self.message == 'mouse right down':
                pydirectinput.mouseDown(None, None, 'right')
            elif self.message == 'mouse right up':
                pydirectinput.mouseUp(None, None, 'right')
            elif self.message == 'mouse middle down':
                pydirectinput.mouseDown(None, None, 'middle')
            elif self.message == 'mouse middle up':
                pydirectinput.mouseUp(None, None, 'middle')
            elif self.message == 'mouse wheel up':
                pydirectinput.mouseDown(None, None, 'wheel')

            elif self.message == 'mouse wheel down':
                pydirectinput.mouseUp(None, None, 'wheel')
            elif self.message == 'mouse move':
                pass
            else:
                logger.warning('Unknown mouse event:%s' % self.message)

        elif self.event_type == 'EK':
            key_code, key_name, extended = self.action

            # shift ctrl alt
            # if key_code >= 160 and key_code <= 165:
            #     key_code = int(key_code/2) - 64

            # 不执行热键
            # if key_name in HOT_KEYS:
            #     return

            base = 0
            if extended:
                base = win32con.KEYEVENTF_EXTENDEDKEY

            if self.message == 'key down':
                pydirectinput.keyDown(str.lower(key_name))
            elif self.message == 'key up':
                pydirectinput.keyUp(str.lower(key_name))
            else:
                logger.warning('Unknown keyboard event:', self.message)

        elif self.event_type == 'EX':
            return
