# PyQt比调用windows API简单很多，而且有windows API的很多优势，比如速度快，可以指定获取的窗口，即使窗口被遮挡。
# 需注意的是，窗口最小化时无法获取截图。
# 首先需要获取窗口的句柄。
import win32gui
# from PyQt5.QtWidgets import QApplication
from PyQt6.QtWidgets import QApplication
import sys

hwnd_title = dict()


def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


win32gui.EnumWindows(get_all_hwnd, 0)
# print(hwnd_title.items())
for h, t in hwnd_title.items():
    if t != "":
        print(h, t)

# 程序会打印窗口的hwnd和title，有了title就可以进行截图了。
hwnd = win32gui.FindWindow(None, 'QQ') #窗口类名 窗口标题名
app = QApplication(sys.argv)
screen = QApplication.primaryScreen()

img = screen.grabWindow(hwnd).toImage()
img.save("screenshot2.jpg")