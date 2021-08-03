"""
选股多线程版本文件。导入数据——执行策略——显示结果
为保证和通达信选股一致，需使用前复权数据
"""
import os
import sys
import time
import pandas as pd
from multiprocessing import Pool, RLock, freeze_support
from rich import print
from tqdm import tqdm
import CeLue  # 个人策略文件，不分享
import func
import user_config as ucfg
from .tdx import HP_tdx

# 配置部分
start_date = ''
end_date = ''

# 变量定义
tdxpath = ucfg.tdx['tdx_path']
csvdaypath = ucfg.tdx['pickle']
已选出股票列表 = []  # 策略选出的股票
要剔除的通达信概念 = ["ST板块", ]  # list类型。通达信软件中查看“概念板块”。
要剔除的通达信行业 = ["T1002", ]  # list类型。记事本打开 通达信目录\incon.dat，查看#TDXNHY标签的行业代码。

starttime_str = time.strftime("%H:%M:%S", time.localtime())
starttime = time.time()
starttime_tick = time.time()


def make_stocklist():
    # 要进行策略的股票列表筛选
    stocklist = [i[:-4] for i in os.listdir(ucfg.tdx['csv_lday'])]  # 去文件名里的.csv，生成纯股票代码list
    print(f'生成股票列表, 共 {len(stocklist)} 只股票')
    print(f'剔除通达信概念股票: {要剔除的通达信概念}')
    tmplist = []
    df = func.get_TDX_blockfilecontent("block_gn.dat")
    # 获取df中blockname列的值是ST板块的行，对应code列的值，转换为list。用filter函数与stocklist过滤，得出不包括ST股票的对象，最后转为list
    for i in 要剔除的通达信概念:
        tmplist = tmplist + df.loc[df['blockname'] == i]['code'].tolist()
    stocklist = list(filter(lambda i: i not in tmplist, stocklist))
    print(f'剔除通达信行业股票: {要剔除的通达信行业}')
    tmplist = []
    df = pd.read_csv(ucfg.tdx['tdx_path'] + os.sep + 'T0002' + os.sep + 'hq_cache' + os.sep + "tdxhy.cfg",
                     sep='|', header=None, dtype='object')
    for i in 要剔除的通达信行业:
        tmplist = tmplist + df.loc[df[2] == i][1].tolist()
    stocklist = list(filter(lambda i: i not in tmplist, stocklist))
    print("剔除科创板股票")
    tmplist = []
    for stockcode in stocklist:
        if stockcode[:2] != '68':
            tmplist.append(stockcode)
    stocklist = tmplist
    return stocklist


def load_dict_stock(stocklist):
    dicttemp = {}
    starttime_tick = time.time()
    tq = tqdm(stocklist)
    for stockcode in tq:
        tq.set_description(stockcode)
        pklfile = csvdaypath + os.sep + stockcode + '.pkl'
        # dict[stockcode] = pd.read_csv(csvfile, encoding='gbk', index_col=None, dtype={'code': str})
        dicttemp[stockcode] = pd.read_pickle(pklfile)
    print(f'载入完成 用时 {(time.time() - starttime_tick):.2f} 秒')
    return dicttemp


def run_celue1(stocklist, df_today, tqdm_position=None):
    if 'single' in sys.argv[1:]:
        tq = tqdm(stocklist[:])
    else:
        tq = tqdm(stocklist[:], leave=False, position=tqdm_position)
    for stockcode in tq:
        tq.set_description(stockcode)
        pklfile = csvdaypath + os.sep + stockcode + '.pkl'
        try:
            df_stock = pd.read_pickle(pklfile)
            if df_today is not None:  # 更新当前最新行情，否则用昨天的数据
                df_stock = func.update_stockquote(stockcode, df_stock, df_today)
            df_stock['date'] = pd.to_datetime(df_stock['date'], format='%Y-%m-%d')  # 转为时间格式
            df_stock.set_index('date', drop=False, inplace=True)  # 时间为索引。方便与另外复权的DF表对齐合并
            celue1 = CeLue.策略1(df_stock, start_date=start_date, end_date=end_date, mode='fast')
            if not celue1:
                stocklist.remove(stockcode)
        except:
            pass

    return stocklist


def run_celue2(stocklist, HS300_信号, df_gbbq, df_today, tqdm_position=None):
    if 'single' in sys.argv[1:]:
        tq = tqdm(stocklist[:])
    else:
        tq = tqdm(stocklist[:], leave=False, position=tqdm_position)
    for stockcode in tq:
        tq.set_description(stockcode)
        pklfile = csvdaypath + os.sep + stockcode + '.pkl'
        try:
            df_stock = pd.read_pickle(pklfile)
        except:
            continue
        df_stock['date'] = pd.to_datetime(df_stock['date'], format='%Y-%m-%d')  # 转为时间格式
        df_stock.set_index('date', drop=False, inplace=True)  # 时间为索引。方便与另外复权的DF表对齐合并

        if '09:00:00' < time.strftime("%H:%M:%S", time.localtime()) < '16:00:00' \
                and 0 <= time.localtime(time.time()).tm_wday <= 4:
            df_today_code = df_today.loc[df_today['code'] == stockcode]
            df_stock = func.update_stockquote(stockcode, df_stock, df_today_code)
            # 判断今天是否在该股的权息日内。如果是，需要重新前复权
            now_date = pd.to_datetime(time.strftime("%Y-%m-%d", time.localtime()))
            if now_date in df_gbbq.loc[df_gbbq['code'] == stockcode]['权息日'].to_list():
                cw_dict = func.readall_local_cwfile()
                df_stock = func.make_fq(stockcode, df_stock, df_gbbq, cw_dict)
        celue2 = CeLue.策略2(df_stock, HS300_信号, start_date=start_date, end_date=end_date).iat[-1]
        if not celue2:
            stocklist.remove(stockcode)
    return stocklist


# 主程序开始
if __name__ == '__main__':
    if 'single' in sys.argv[1:]:
        print(f'检测到参数 single, 单进程执行')
    else:
        print(f'附带命令行参数 single 单进程执行(默认多进程)')

    stocklist = make_stocklist()
    print(f'共 {len(stocklist)} 只候选股票')
    HP_tdx.getSH()
