#!/usr/bin/env python
# encoding: utf-8

#@author: 东哥加油!!!
#@file: dfcf.py
#@time: 2019/1/1 15:47



import requests
import requests.packages.urllib3.exceptions
import json
import http
import time
import urllib.parse
import logging
import random
from PIL import Image
import pytesseract
import re

from lxml import etree


class stock():
    def __init__(self,Zqdm,Zqmc,Zqsl,Kysl,Cbjg,Zxjg,Ykbl):

        self.Zqdm = Zqdm             #证券编码
        self.Zqmc = Zqmc             #证券名称
        self.Zqsl = int(Zqsl)        #持仓数量
        self.Kysl = int(Kysl)        #可用数量
        self.Cbjg = float(Cbjg)      #成本价
        self.Zxjg = float(Zxjg)      #当前价
        self.Ykbl = float(Ykbl)      #盈亏比例



class dfcf():
    def __init__(self):
        self.sess = requests.session()
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
        self.headers = {
            'Host': 'jy.xzsec.com',
            'Connection': 'keep - alive',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://jy.xzsec.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Referer': 'https://jy.xzsec.com/Search/Position',
        }
        self.validatekey='8c7f5173-d91a-4c0d-b667-c9bf933eb18a'
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=logging.INFO)
        handler = logging.FileHandler("stock.log")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s:%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        #止损比
        self.zqbl = -0.02
        #止盈比
        self.zybl = 0.04

    #登录并获取cookie
    def dfcf_login(self):

        randNumber=random.random()-0.00000000000000009
        headers = {
            'Host': 'jy.xzsec.com',
            'Connection': 'keep - alive',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://jy.xzsec.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Referer': 'https://jy.xzsec.com/',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        url = 'https://jy.xzsec.com/Login/YZM?randNum='+str(randNumber)
        response = self.sess.get(url,headers=headers,verify=False)
        with  open(r'D:/dfyzm.png', 'wb') as file:
            file.write(response.content)
        image = Image.open('dfyzm.png')
        yzm=pytesseract.image_to_string(image)
        identifyCode = input("输入验证码: ")
        url = 'https://jy.xzsec.com/Login/Authentication?validatekey='
        headers = {
            'Host': 'jy.xzsec.com',
            'Connection': 'keep - alive',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://jy.xzsec.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Referer': 'https://jy.xzsec.com/Login?el=1&clear=1',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data={
            'userId':'540650040321',
            'password':'620813',
            'randNumber':randNumber,
            'identifyCode':identifyCode,
            'duration':1800,
            'authCode':'',
            'type':'Z'
        }

        response = self.sess.post(url, data=data, headers=headers, verify=False)

        c = requests.cookies.RequestsCookieJar()  # 利用RequestsCookieJar获取
        c.set('cookie-name', 'cookie-value')
        self.sess.cookies.update(c)

        headers = {
            'Host': 'jy.xzsec.com',
            'Connection': 'keep - alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Referer': 'https://jy.xzsec.com/Login?el=1&clear=1',
            'Upgrade-Insecure-Requests': '1',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

        url = 'https://jy.xzsec.com/Trade/Buy'
        response = self.sess.get(url,headers=headers, verify=False)
        html = etree.HTML(response.text)
        em_validatekey = html.xpath('//input[@id="em_validatekey"]')[0].get('value')
        print(em_validatekey)
        self.validatekey = em_validatekey


    def get_stocklist(self):
        url = 'https://jy.xzsec.com/Search/GetStockList'
        data = {'validatekey':self.validatekey}

        response = self.sess.post(url,data=data,headers=self.headers,verify=False)
        print(self.sess.cookies)
        rjson = json.loads(response.text)
        t_list = rjson['Data']
        stock_list = []
        for i in t_list:
            si = stock(i['Zqdm'],i['Zqmc'],i['Zqsl'],i['Kysl'],i['Cbjg'],i['Zxjg'],i['Ykbl'])
            stock_list.append(si)

        print(stock_list)
        # for si in stock_list:
        #     #止损比 self.zqbl = -0.02
        #     if si.Ykbl<self.zqbl:
        #         self.sell_stock(si,si.Zxjg,100)
        #         self.logger.info('挂单卖出'+ si.Zqdm+' '+si.Zqmc+' 数量:'+str(100)+' 价格:'+str(si.Zxjg))
        #     #止盈比self.zybl = 0.04
        #     elif si.Ykbl>self.zybl:
        #         # 增加卖出操作
        #         pass
        #     else:
        #         #持仓
        #         pass

    def get_yzm(self):
        pass

    #卖出操作
    def sell_stock(self,stock,price,amount):
        data = {'stockCode':stock.Zqdm,'price':price,'amount':amount,'tradeType':'S','zqmc':stock.Zqmc}
        d = urllib.parse.urlencode(data)
        print(data)
        url = 'https://jy.xzsec.com/Trade/SubmitTrade?validatekey='+self.validatekey
        response = self.sess.post(url, data=data, headers=self.headers, verify=False)
        print(response.text)

    #撤单
    def revoke_stock(self):
        url='https://jy.xzsec.com/Trade/GetRevokeList'
        data={'validatekey':self.validatekey}
        response = self.sess.get(url,data=data,headers=self.headers,verify=False)
        rjson = json.loads(response.text)
        s_list = rjson['Data']
        for si in s_list:
            print(si)
            #revokes=20190110_315084
            data = {'revokes':si['Wtrq']+'_'+si['Wtbh']}
            url = 'https://jy.xzsec.com/Trade/RevokeOrders?validatekey='+self.validatekey
            response = self.sess.post(url, data=data, headers=self.headers, verify=False)
            self.logger.info('卖出撤单 ' + si['Zqdm'] + ' ' + si['Zqmc'] + ' 数量:' + si['Wtsl'] + ' 价格:' + si['Wtjg']+' 服务器响应内容'+response.text)
            print(response.text)

    def processing_image(self):
        image_obj = self.get_pictures() # 获取验证码
        img = image_obj.convert("L") # 转灰度
        pixdata = img.load()
        w, h = img.size
        threshold = 160 # 该阈值不适合所有验证码，具体阈值请根据验证码情况设置
        # 遍历所有像素，大于阈值的为黑色
        for y in range(h):
            for x in range(w):
                if pixdata[x, y] < threshold:
                    pixdata[x, y] = 0
                else:
                    pixdata[x, y] = 255
        return img


    #买入操作
    def buy_stock(self,zqdm,price,amount,zqmc):
        url = 'https://jy.xzsec.com/Trade/SubmitTrade?validatekey='+self.validatekey
        data = {
            'stockCode':zqdm,
            'price':price,
            'amount':amount,
            'tradeType':'B',
            'zqmc':zqmc}
        print(self.sess.cookies)
        response = self.sess.post(url,data=data,headers=self.headers,verify=False)
        print(response.text)

def processing_image(image):
    img = image.convert("L") # 转灰度
    pixdata = img.load()
    w, h = img.size
    threshold = 160 # 该阈值不适合所有验证码，具体阈值请根据验证码情况设置
    # 遍历所有像素，大于阈值的为黑色
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img
if __name__ == '__main__':

    pytesseract.pytesseract.tesseract_cmd = r'D:\Users\lancelot\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    # image = Image.open(r'D:/dfyzm.png')
    # yzm=pytesseract.image_to_string(processing_image(image))
    # print(yzm)

    al = dfcf()
    al.dfcf_login()
    # al.get_stocklist()
    #al.buy_stock('000727',1.5,100,'华东科技')
    #al.revoke_stock()