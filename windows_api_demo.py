import win32gui
import win32con

win = win32gui.FindWindow('Notepad++', 'CC.txt')
tid = win32gui.FindWindowEx(win, None, 'Edit', None)
win32gui.SendMessage(tid, win32con.WM_SETTEXT, None, 'hello world')
win32gui.PostMessage(tid, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
