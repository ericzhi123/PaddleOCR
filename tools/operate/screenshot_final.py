import win32gui
import win32api
import win32ui
import win32con
import win32print
import time
from PIL import Image


def get_all_hwnd(hwnd, hwnd_title):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

def get_app_hwnd(win_title):
    hwnd_title = dict()
    # 程序会打印窗口的hwnd和title，有了title就可以进行截图了。
    hwnd_app = 0
    win32gui.EnumWindows(get_all_hwnd, hwnd_title)
    for h, t in hwnd_title.items():
        if t != "":
            print(h, t)
        if t == win_title:
            hwnd_app = h
    return hwnd_app


# 局部截图
def window_capturex():
    proportion = round(
        win32print.GetDeviceCaps(win32gui.GetDC(0), win32con.DESKTOPHORZRES) / win32api.GetSystemMetrics(0), 2)
    print(proportion)

    hwnd_target = get_app_hwnd("ITMS2019新群")
    if hwnd_target != 0:
        win32gui.SetForegroundWindow(hwnd_target)
        time.sleep(0.5)

    left, top, right, bot = win32gui.GetWindowRect(win32gui.GetForegroundWindow())
    left = int(left * proportion)
    top = int(top * proportion)
    right = int(right * proportion)
    bot = int(bot * proportion)
    w = right - left
    h = bot - top
    hWndDC = win32gui.GetWindowDC(win32gui.GetDesktopWindow())
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1) #将BGRX颜色格式转换为RGB格式，便于后续处理
    im.save("test.png")

    '''
    try:
        saveBitMap.SaveBitmapFile(saveDC, "tempcap.bmp")
    except Exception as e:
        print("错误")
        pass
    '''
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(win32gui.GetDesktopWindow(), hWndDC)


# 全屏截取
def window_capture():
    hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w, h = get_real_resolution()
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    try:
        saveBitMap.SaveBitmapFile(saveDC, "tempcap.bmp")
    except Exception as e:
        print("错误")
        pass
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(win32gui.GetDesktopWindow(), hwndDC)


def get_real_resolution():
    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    # 横向分辨率
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    # 纵向分辨率
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    proportion = round(w / h, 2)
    return w, h


if __name__ == '__main__':
    # window_capture()
    window_capturex()