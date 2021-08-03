import pytdx.hq
import pytdx.util.best_ip
from strategy.WeekConsecutiveCross import WeekConsecutiveCross
from sqlalchemy import create_engine
from tdx.api import *

# print(f"优选通达信行情服务器 也可直接更改为优选好的 {{'ip': '123.125.108.24', 'port': 7709}}")
# ipinfo = pytdx.util.best_ip.select_best_ip()
api = pytdx.hq.TdxHq_API()

if __name__ == '__main__':


    tdxapi = TdxInit(ip='183.60.224.178', port=7709)
    # latest=get_security_quotes('600460')
    # df=szStockList()
    # df=get_security_bars(5,1,'600460',0,10)
    # df['category']='week'


    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/gp?charset=utf8mb4',encoding='utf-8', echo=True)

    # //获取all stock
    all_stock=get_lastest_stocklist()
    all_stock.to_sql('stock', engine, index=False,if_exists='append')
    weekCross=WeekConsecutiveCross(df)
    weekCross.run()