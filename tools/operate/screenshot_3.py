import win32gui
import win32ui
import win32con
import win32api
import win32print

# 局部截图
def window_capturex():
    proportion = round(
        win32print.GetDeviceCaps(win32gui.GetDC(0), win32con.DESKTOPHORZRES) / win32api.GetSystemMetrics(0), 2)
    print(proportion)
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
    try:
        saveBitMap.SaveBitmapFile(saveDC, "tempcap.bmp")
    except Exception as e:
        print("错误")
        pass
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
    hwnd = win32gui.FindWindow(None, 'QQ')
    # window_capture()
    window_capturex()