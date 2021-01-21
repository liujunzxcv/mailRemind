#!/usr/bin/env python
# coding=utf-8
import json
import logging
import os
import random
import re
import time
import requests
from bs4 import BeautifulSoup
from lxml import etree
from os import path
from mail import Mail

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

ticks = 1611016660

def _get_info():
    global origin_position
    while True:
        try:
            url = 'https://www.apple.com.cn/shop/refurbished/ipad'

            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
            }
            r = requests.get(url, headers=headers)
            r.encoding = r.apparent_encoding
            html = r.text
            soup = BeautifulSoup(html, 'lxml')  # 转换为BeautifulSoup的解析对象()里第二个参数为解析方式
            # titles = soup.find_all('a', class_='as-producttile-tilelink')
            titles = soup.find_all(text=re.compile('(?=.*翻新 iPad )'))
            result = ''
            for each in titles:
                if each.find("GB") != -1 & each.find("\n") == -1:
                    result += each + '\n'
            if result.__len__() > 0:
                time2 = time.time()
                global ticks 
                timediff = time2 - ticks
                logger.info("距离上次发邮件小时数" + str(timediff/60/60))
                if timediff > 86400:
                    send_email = Mail(text=result, sender='wo', receiver='ni', subject='iPad Pro 有货', logger=logger,
                                  smtp_server=smtp_server, from_addr=from_addr, password=password)
                    send_email.send()
                    ticks = time2
            else:
                logger.info("商品无货" + result)
        except Exception as e:
            logger.error(e)
        time.sleep(600)


if __name__ == '__main__':
    _get_info()
