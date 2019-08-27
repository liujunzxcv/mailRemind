#!/usr/bin/env python3
# coding=utf-8
import json
import logging
import os
import random
import time
from os import path

import ccxt

from mail import Mail

#  引入ccxt框架， 通过pip install ccxt 可以进行安装
# ccxt 的github地址为： https://github.com/ccxt/ccxt

origin_position = 0

BASIC_FORMAT = "%(asctime)s:%(levelname)s:%(message)s"
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(filename='biz.log', format=BASIC_FORMAT,
                    level=logging.INFO, filemode='a', datefmt=DATE_FORMAT)
chlr = logging.StreamHandler()  # 输出到控制台的handler

formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
chlr.setFormatter(formatter)
chlr.setLevel('INFO')  # 也可以不设置，不设置就默认用logger的level

logger = logging.getLogger()
logger.addHandler(chlr)

# mailbox setting
local_dir = path.dirname(__file__)
with open(os.path.join(local_dir, 'mailbox.txt'), 'r') as f:
    mail_setting = f.readlines()
from_addr = mail_setting[0].strip()
password = mail_setting[1].strip()
smtp_server = mail_setting[2].strip()
apikey = mail_setting[3].strip()
secret = mail_setting[4].strip()


def _get_info():
    # 初始化bitme交易所对象
    bitmex = ccxt.bitmex()
    bitmex.apiKey = apikey
    bitmex.secret = secret
    global origin_position
    while True:
        try:
            data = bitmex.privateGetPosition()
            bitmex_json = bitmex.json(data)
            print(bitmex_json)
            result_json = json.loads(bitmex_json)
            print(result_json)

            if origin_position != result_json[0]['currentQty']:
                content = ' 当前仓位由' + str(origin_position) + '，变为：' + str(
                    result_json[0]['currentQty']) + ';  还有未成交买单:' + str(
                    result_json[0]['openOrderBuyQty']) + ',未成交卖单:' + str(
                    result_json[0]['openOrderSellQty'])
                send_email = Mail(text=content, sender='wo', receiver='ni', subject='仓位变动', logger=logger,
                                  smtp_server=smtp_server, from_addr=from_addr, password=password)
                send_email.send()
                origin_position = result_json[0]['currentQty']
                logger.info(bitmex_json)
                logger.info(content)
            else:
                logger.info('仓位没有变化,当前仓位:' + str(origin_position) + ';  还有未成交买单:' + str(
                    result_json[0]['openOrderBuyQty']) + ',未成交卖单:' + str(
                    result_json[0]['openOrderSellQty']))
        except Exception as e:
            logger.error(e)
        time.sleep(5 + random.uniform(0, 3))


if __name__ == '__main__':
    _get_info()
