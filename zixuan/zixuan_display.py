from sqlalchemy import text

from xuangubao.base import session_factory
from tdx.HP_tdx import get_security_quotes, TdxInit
import time
import os
import pyautogui
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)



if __name__ == '__main__':

    tdxapi=TdxInit()


    session = session_factory()
    stock_list = list(session.execute(text("SELECT * FROM zixuan")))
    tdxapi = TdxInit(ip='183.60.224.178', port=7709)
    clearConsole()
    pyautogui.click(x=2799, y=575)

    while True:
        for stock in stock_list:
            result=tdxapi.get_security_quotes(0 if stock.code=='SZ' else 1,stock.code)
            print(result)

        time.sleep(1)

