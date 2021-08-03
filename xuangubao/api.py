import requests
import json
from xuangubao.kline import kline
from xuangubao.base import session_factory
import datetime
from  xuangubao.kline_week import kline_week

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': '*/*',
    'Origin': 'https://xuangubao.cn',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://xuangubao.cn/',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6,zh-TW;q=0.5,fr;q=0.4,pt;q=0.3',
}

params = (
    ('fields', 'tick_at,close_px,avg_px,turnover_volume,turnover_value,open_px,high_px,low_px,px_change,px_change_rate'),
    ('prod_code', '600428.SS'),
)

response = requests.get('https://api-ddc-wscn.xuangubao.cn/market/trend', headers=headers, params=params)


def get_header():
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': '*/*',
        'Origin': 'https://xuangubao.cn',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://xuangubao.cn/',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6,zh-TW;q=0.5,fr;q=0.4,pt;q=0.3',
    }

    return headers;

def get_kline(code,cateory='day'):
    headers = get_header()

    if cateory=='day':
        cateory_code='86400'
    elif cateory=='week':
        cateory_code='604800'

    params = (
        ('tick_count', '256'),
        ('prod_code', code),
        ('adjust_price_type', 'forward'),
        ('period_type', cateory_code),
        ('fields', 'tick_at,open_px,close_px,high_px,low_px,turnover_volume,turnover_value,turnover_ratio,average_px,px_change,px_change_rate,avg_px,business_amount,business_balance,ma5,ma10,ma20,ma60'),
    )

    response = requests.get('https://api-ddc-wscn.xuangubao.cn/market/kline', headers=headers, params=params)
    text=response.text
    return json.loads(text)['data']['candle']

def get_hot_plate():

    headers = get_header()
    response = requests.get(' https://baoer-api.xuangubao.cn/api/v2/tab/recommend?module=trending_plates', headers=headers)
    return response.text



if __name__ == '__main__':

    # hot_plate=get_hot_plate()
    # print(hot_plate)

    session = session_factory()

    stock_list=session.execute(text("select * from stock where code >='000514' "));
    for stock in stock_list:
        code=stock['code']+'.'+stock['sse']
        data=get_kline(code)

        for item in data[code]['lines']:

            kline_entity=kline_week(
                open=item[0],code=stock['code'],
                close=item[1], high=item[2],low=item[3],turnover_volume=item[7],
                turnover_ratio=item[15],ma5=item[11],ma10=item[12],ma20=item[13],ma60=item[14],
                week=datetime.datetime.fromtimestamp(item[9])
            )
            session.add(kline_entity)
            session.commit()
            print(data)





