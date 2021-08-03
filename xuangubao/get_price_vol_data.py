import pandas as pd

#base是个人写的脚本文件
from datetime import datetime,timedelta

def get_price_vol_data():
    now=datetime.now()
    date=(now-timedelta(360)).strftime('%Y%m%d')
    sql=f'select * from daily_data where trade_date>{date}'
    all_data=pd.read_sql(sql,engine)
    all_data=all_data.sort_values(['ts_code','trade_date'])
    codes=list(all_data.ts_code.unique())
    #前复权
    all_data['adjclose']=all_data.groupby('ts_code').apply(lambda x:x.close*x.adj_factor/x.adj_factor.iloc[-1]).values
    all_data['adjvol']=all_data.groupby('ts_code').apply(lambda x:x.vol*x.adj_factor/x.adj_factor.iloc[-1]).values
    all_data['adjopen']=all_data.groupby('ts_code').apply(lambda x:x.open*x.adj_factor/x.adj_factor.iloc[-1]).values
    all_data['adjhigh']=all_data.groupby('ts_code').apply(lambda x:x.high*x.adj_factor/x.adj_factor.iloc[-1]).values
    all_data['adjlow']=all_data.groupby('ts_code').apply(lambda x:x.low*x.adj_factor/x.adj_factor.iloc[-1]).values

    #设置索引
    all_data=all_data.set_index(['trade_date','ts_code'])[['adjclose','adjvol','adjopen','adjhigh','adjlow']]
    #转成面板数据
    all_data=all_data.unstack()
    return codes,all_data

def find_price_vol_stock(n,r=1.2):
    codes,all_data=get_price_vol_data()
    up_list=[]
    for code in codes:
        close=all_data['adjclose'][code]
        open_=all_data['adjopen'][code]
        high=all_data['adjhigh'][code]
        low=all_data['adjlow'][code]
        vol=all_data['adjvol'][code]
        #剔除一字涨停
        flag=True
        if close.iloc[-1]==open_.iloc[-1]==high.iloc[-1]==low.iloc[-1]:
            flag=False
            break
        #最近五日没有长上影线,以单日回撤3%为长上影线
        for i in range(5):
            if close[-5:][i]*1.03<high[-5:][i]:
                flag=False
                break
        #价格突破前N日新高
        p=close.iloc[-1] #当前价格
        p0=close[-n:-1].min()
        p1=close[-n:-1].max() #前n-1日最高价
        #价格短期已上涨超过50%，涨幅过大不宜介入
        '''
        if (p-p0)/p0>r:
            flag=False
            break '''
        #价格突破且放量上涨
        if flag==True and \
                p1<p<p1*r and \
                vol[-5:].mean()/vol[-10:-5].mean()>2.0:
            up_list.append(code)
    return up_list
