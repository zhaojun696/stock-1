import pandas as pd
import pytdx.hq
import pytdx.util.best_ip
from pytdx.hq import TdxHq_API
from pytdx.exhq import TdxExHq_API, TDXParams
from pytdx.config.hosts import hq_hosts



def get_security_bars(nCategory=4,nMarket = -1,code='000776', \
                      nStart=0, nCount=240):
    '''
    #(nCategory, nMarket, sStockCode, nStart, nCount)
    #获取市场内指定范围的证券K 线，
    #指定开始位置和指定K 线数量，指定数量最大值为800。
    #参数：
    #nCategory -> K 线种类
    #0 5 分钟K 线
    #1 15 分钟K 线
    #2 30 分钟K 线
    #3 1 小时K 线
    #4 日K 线
    #5 周K 线
    #6 月K 线
    #7 1 分钟
    #8 1 分钟K 线
    #9 日K 线
    #10 季K 线
    #11 年K 线
    #nMarket -> 市场代码0:深圳，1:上海
    #sStockCode -> 证券代码；
    #nStart -> 指定的范围开始位置；
    #nCount -> 用户要请求的K 线数目，最大值为800。
    '''
    global tdxapi,scode,smarket
    scode=code
    if nMarket == -1:
        nMarket=get_market(code)
    smarket=nMarket
    result =tdxapi.get_security_bars(nCategory, nMarket,code, nStart, nCount)
    df=tdxapi.to_df(result)
    #a=[x[0:10] for x in df.datetime]
    #df.insert(0,'date',a)
    # df['date']=df['datetime']
    # df['volume']=df['vol']
    # df['code']=code
    # df['market']=nMarket
    # df['category']=nCategory
    return df


def get_lastest_stocklist():
    """
    使用pytdx从网络获取最新券商列表
    :return:DF格式，股票清单
    """
    import pytdx.hq
    import pytdx.util.best_ip
    print(f"优选通达信行情服务器 也可直接更改为优选好的 {{'ip': '123.125.108.24', 'port': 7709}}")
    # ipinfo = pytdx.util.best_ip.select_best_ip()
    api = pytdx.hq.TdxHq_API()
    # with api.connect(ipinfo['ip'], ipinfo['port']):
    with api.connect('123.125.108.24', 7709):
        data = pd.concat([pd.concat(
            [api.to_df(api.get_security_list(j, i * 1000)).assign(sse='SZ' if j == 0 else 'SS') for i in
             range(int(api.get_security_count(j) / 1000) + 1)], axis=0) for j in range(2)], axis=0)
    # data = data.reindex(columns=['sse', 'code', 'name', 'pre_close', 'volunit', 'decimal_point'])
    data= data.loc[ (data['code'].str.startswith('00')) | (data['code'].str.startswith('60')) |(data['code'].str.startswith('30'))]

    # data.sort_values(by=['sse', 'code'], ascending=True, inplace=True)
    # data.reset_index(drop=True, inplace=True)
    return data

#tdx接口初始化
def TdxInit(ip='59.173.18.140',port=7709):
    global tdxapi
    tdxapi = TdxHq_API(heartbeat=True)
    result=tdxapi.connect(ip, port)
    if result==None:
        return None
    return tdxapi



#获取股票代码表
def GetSecurityList(nMarket = 0):
    """

    Returns:
        object:
    """
    tdxapi = TdxInit(ip='183.60.224.178', port=7709)
    #nMarket = 0    # 0 - 深圳  1 - 上海
    nStart = 0

    m=tdxapi.get_security_count(nMarket)
    df=tdxapi.to_df(tdxapi.get_security_list(nMarket, nStart))
    df=pd.DataFrame(columns = ['code','name','pre_close'])
    df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='')
    while nStart<m:
        result = tdxapi.get_security_list(nMarket, nStart)
        df2=tdxapi.to_df(result)
        df=df.append( df2,ignore_index=True)
        nStart=nStart+1000
    return df
#获取深圳股票代码表
def getSZ():
    base=GetSecurityList(0)
    return base

#'深圳股票代码表'
def szcode():
    #'深圳股票代码'
    sz=getSZ()
    sz['type']=''
    sz['kind']=''
    sz['market']=0
    sz['type2']=10
    for i in range(len(sz)):
        #print(i,sh['code'][i])
        x=int(sz['code'][i])
        if x<2000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='A股股票'
            sz.loc[i,'type2']=1
        elif x>=2000 and x<31000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='中小板'
            sz.loc[i,'type2']=2
        elif x>=31000 and x<80000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='权证'
            sz.loc[i,'type2']=8
        elif x>=80000 and x<100000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='配股'
            sz.loc[i,'type2']=1
        elif x>=100000 and x<150000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='债券'
            sz.loc[i,'type2']=6
        elif x>=150000 and x<200000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='基金'
            sz.loc[i,'type2']=7
        elif x>=200000 and x<300000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='B股股票'
            sz.loc[i,'type2']=5
        elif x>=300000 and x<380000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='创业板'
            sz.loc[i,'type2']=3
        elif x>=390000 and x<400000:
            sz.loc[i,'type']='指数板块'
            sz.loc[i,'kind']='指数'
            sz.loc[i,'type2']=0
        elif x>=400000 and x<500000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='三板'
            sz.loc[i,'type2']=1
        elif x>=500000 and x<600000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='基金'
            sz.loc[i,'type2']=7
        elif x>=600000 and x<800000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='A股股票'
            sz.loc[i,'type2']=1
        elif x>=800000 and x<900000:
            sz.loc[i,'type']='指数板块'
            sz.loc[i,'kind']='板块'
            sz.loc[i,'type2']=0
        elif x>=900000 and x<999000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='B股股票'
            sz.loc[i,'type2']=5
        elif x>=999000 :
            sz.loc[i,'type']='指数板块'
            sz.loc[i,'kind']='指数'
            sz.loc[i,'type2']=0
    sz.to_csv('./data/sz.csv' , encoding= 'gbk')
    return sz

if __name__ == '__main__':
    stock=getSZ()
    print(stock)
