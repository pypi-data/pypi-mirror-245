import argparse
import datetime
import json
import random
import sys
import time
import traceback

import requests
import urllib3
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter, Retry
import argparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class wxinfo_test6:
    http_adapter = HTTPAdapter(max_retries=3, pool_connections=100, pool_maxsize=100, pool_block=True)
    # 需要打印的代码
    stock_list = []
    session = None
    adapter = None

    @classmethod
    def get_session(cls):
        if cls.session is None:
            cls.adapter = HTTPAdapter(
                max_retries=Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504]),
                pool_connections=100, pool_maxsize=100, pool_block=True)
            cls.session = requests.Session()
            cls.session.mount('http://', cls.adapter)
            cls.session.mount('https://', cls.adapter)
        return cls.session

    @classmethod
    def get_working_proxy(cls):
        """
        获取代理 添加代理
        :return:
        """
        proxyUrl = "http://%(user)s:%(password)s@%(server)s" % {
            "user": "69160CF3",
            "password": "42E62B66543E",
            "server": "tunnel6.qg.net:16670",
        }
        print('当前代理池取出：{0}'.format(proxyUrl))
        proxies = {
            'http': proxyUrl,
            'https': proxyUrl
        }
        cls.get_session().proxies = proxies

    @classmethod
    def postUtil(cls, url, dataList):
        """
        发起请求
        :param url:
        :param dataList:
        :return:
        """
        headers = {
            "Cache-Control": "no-cache",
            "Content-Type": "application/json",
            "User-Agent": UserAgent().random
        }
        response = cls.get_session().post(url, headers=headers, data=json.dumps(dataList))
        dataList.clear()
        return response.text

    @classmethod
    def data_ware(cls, code, n):
        """
        数据处理
        :param code:
        :return:
        """
        url = 'https://emdcstockcontest.eastmoney.com/competitionSrv2'
        data_rate = {
            "args": {
                "competitionCategories": "1",
                "combination": code,
                "allRecords": "true",
                "pageSize": n,
                "pageNo": 1,
                "orderSno": "",
                "bizDate": "",
                "competitionId": "2",
                "hasLoginInfo": "0",
                "uid": "3099366307543296"
            },
            "method": "relocatePositionHandler",
            "client": "ios",
            "disableEncrypt": "true",
            "transactionId": (str(random.randint(0, 900000))),
            "timestamp": int(round(time.time() * 1000)),
            "reserve": "iPhone12-cfw-SecuritesContest-1.0.0.230918150215745",
            "clientType": "cfw",
            "clientVersion": "10.10.2",
            "deviceId": "BD8D6616-7E8E-4BCC-BF67-4AA9BB1D4068"

        }
        return cls.postUtil(url, data_rate)

    def send_message(message):

        webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=6611a028add5a126ab637145aa6fe4b1c3169e315425c1f78e227a70b8b996a3"
        data = {
            "msgtype": "text",
            "text": {"content": message}
        }
        headers = {"Content-Type": "application/json;charset=utf-8"}
        response = requests.post(webhook_url, json=data, headers=headers)
        return response.text

    def update_list(code, i, n):

        data = wxinfo_test6.data_ware(code, n)
        jsondata = json.loads(data)

        new_items = []
        for data_item in jsondata['data']:
            #print(data_item)
            relocate_list = data_item['relocateList']
            for item in relocate_list:
                # time = datetime.datetime.strptime(item['relocateTime'], "%m-%d %H:%M")
                # now = datetime.datetime.now()
                # if time.day == now.day:
                new_items.append({
                        'name': item['stkName'],
                        'action': item['bsMark'],
                        'price': item['relocatePrice'],
                        'time': item['relocateTime'],
                        'afterPositionRate': item['afterPositionRate']
                    })
        if not wxinfo_test6.stock_list:
            wxinfo_test6.stock_list = new_items
        if new_items != wxinfo_test6.stock_list and datetime.datetime.strptime(new_items[0]['time'],
                                                                               "%m-%d %H:%M") > datetime.datetime.strptime(
            wxinfo_test6.stock_list[0]['time'], "%m-%d %H:%M"):
            message = '股票名称：' + new_items[0]['name'] + '\n' + '操作方式：' + new_items[0][
                'action'] + '\n' + '价格：' + new_items[0]['price'] + '\n' + '操作时间：' + new_items[0][
                          'time'] + '\n' + '仓位：' + new_items[0]['afterPositionRate']
            print(message)
            wxinfo_test6.send_message(message)
            wxinfo_test6.stock_list = new_items
        print(i, datetime.datetime.now(), wxinfo_test6.stock_list)


# 判断ip是否可用

if __name__ == '__main__':
    # print(wxinfo_test6.send_message("股票名称：=====》"))
    # data = wxinfo_test6.data_ware("104100") 稳健榜 104100
    # data = wxinfo_test6.data_ware("63590") 庙里的公鸡
    # data = wxinfo_test6.data_ware("24527") 五点下班 （重点）
    # data = wxinfo_test6.data_ware("105183") K先生等风来    16542    -- '继续爱,16542,1.917941',

    # ****************************************************
    #   第一次配置：31405   106449   赚学费  69632  富贵满腹地鲁班,   150024  大数学家峰哥   15049（愉快）
    #
    #
    #
    #
    # #41226  第一名 零天赋（重点），"24527") 五点下班 （重点）日丰！！！
    # '冲刺队一迅游,96924,0.314327

    #
    #
    # 31405    赚学费,106449,   105183 K先生等风来       16542 -- '继续爱,

    # 删选池子：
    # 76801 5084 1671 72675，98486，
    # 38775 72234 32039 69431

    # 31405




    # **************************************************

    # '恬淡虚无1110,107937,0.303354',
    # 继续爱,16542,1.917941










    # parser = argparse.ArgumentParser()
    # parser.add_argument('code', help='stock code')
    # args = parser.parse_args()
    # codes = args.code
    # 创建一个ArgumentParser对象
    parser = argparse.ArgumentParser()

    # 添加命令行参数的定义
    parser.add_argument("code", help="用户id")


    # 解析命令行参数
    args = parser.parse_args()

    # 在这里可以进行相应的处理
    print(args.code)


    codes = args.code

    n = 2
    i = 0
    while True:
        try:
            wxinfo_test6.update_list(codes, i, n)
            i = i + 1
        except:
            print(traceback.print_exc())
            print("数据异常，切换代理重新执行！")
            wxinfo_test6.get_working_proxy()
            wxinfo_test6.get_session().close()
        now = datetime.datetime.now()
        # print(now.hour)
        if now.hour >= 15:
            # 如果当前时间在下午三点或之后，则退出程序
            wxinfo_test6.send_message("祝大家：，收盘快乐！")
            # sys.exit("当天收盘")
