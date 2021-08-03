from xuangubao.api import get_header
import requests
import json

def get_hot_plate():
    header=get_header()
    url='https://flash-api.xuangubao.cn/api/surge_stock/plates'

    resp=requests.get(url)
    return json.loads(resp.text)['data']['items']



if __name__ == '__main__':
    hot_plate=get_hot_plate()
    for item in hot_plate:
        print(item)