import win32gui
import win32ui
import win32con
from ctypes import windll
from PIL import Image

# 根据句柄、截图位置和图片路径，对窗口的客户区截图并存到指定位置
# GetDC一类的需要用ReleaseDC释放，CreateDC一类的用DeleteDC释放，DeleteObject则删除一个逻辑笔、画笔、字体、位图、区域或者调色板，
def ClientRect_PrtSc(hwnd, area=None, filename=''):
    try:
        hwnd = hwnd
        if filename == '':
            filename = '{}.bmp'.format(
                hwnd)
        hwndDC = win32gui.GetDC(
            hwnd)  # 获取窗口的设备上下文Device Context。GetWindowDC包括了非客户区，而GetDC仅为客户区
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)  # 获取mfcDC
        saveDC = mfcDC.CreateCompatibleDC()  # 创建可兼容DC
        saveBitMap = win32ui.CreateBitmap()  # 创建bitmap以保存图片
        '''MonitorDev = win32api.EnumDisplayMonitors(
            None, None)  # 获取显示器信息，枚举显示器，笔记本据说可能有问题'''
        x1, y1, x2, y2 = win32gui.GetClientRect(
            hwnd)  #GetClientRect获取客户区窗口位置，GetWindowRect获取整个窗口的位置信息
        x, y, w, h = (0, 0, 0, 0)
        if area == None:
            x = 0
            y = 0
            w = x2 - x1
            h = y2 - y1
        else:
            x, y, m, n = area
            w = m - x
            h = n - y
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)  # 为bitmap开辟空间
        # 对saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)的理解：
        # 1.mfc相当于一个虚拟屏幕。这里的参数w和h决定了这个屏幕的大小。
        # 2.屏幕的初始状态是黑色，每个坐标都是#000000
        # 3.之前有mfcDC = win32ui.CreateDCFromHandle(hwndDC)，又有hwndDC = win32gui.GetDC(hwnd)
        #   mfcDC和hwnd窗口之间建立了某种关联，可以将hwnd窗口中的图像放到虚拟屏幕上
        saveDC.SelectObject(saveBitMap)  # 将截图保存到saveBitMap中
        saveDC.BitBlt((0, 0), (w, h), mfcDC, (x, y), win32con.SRCCOPY)
        # 对saveDC.BitBlt(坐标1, (w, h), mfcDC, 坐标2, win32con.SRCCOPY)的理解：
        # BitBlt的功能大概是把从hwnd窗口截到的图放到虚拟屏幕上，信息转入saveDC。
        # 1.坐标1是针对窗口截图的，指定截图放在黑色背景上的位置（指定左上角）
        # 2.w和h窗口截图的长宽，而坐标2指定了开始截图的位置
        #   这两个参数决定了从hwnd窗口的哪里截图、截多大的图
        # 3.mfcDC已经和hwnd窗口建立了关联，所以不需要指定虚拟屏幕从哪个窗口获得截图
        # 4.SRCCOPY意为将截图直接拷贝到虚拟屏幕中
        # 接下来的saveBitMap.SaveBitmapFile(saveDC, filename)则是对虚拟屏幕截图并保存到指定位置
        saveBitMap.SaveBitmapFile(saveDC, filename)
        # 清除数据
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)
        print('对句柄 {} 标题 {} 的窗口截图并保存'.format(hwnd,
                                            win32gui.GetWindowText(hwnd)))
    except:
        print('客户区截图 出现错误, 窗口不存在')


if __name__ == '__main__':
    hwnd = win32gui.FindWindow(None, 'QQ')
    ClientRect_PrtSc(hwnd)