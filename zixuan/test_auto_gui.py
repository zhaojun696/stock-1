import pyautogui

if __name__ == '__main__':
    cposition = pyautogui.locateOnScreen(r"D:\software\Bypass\Bypass.exe")  #根据图片定位
    cc = pyautogui.center(cposition)
    pyautogui.moveTo(cc[0],cc[1])  #把鼠标移动到这个位置
    pyautogui.click(clicks=2)