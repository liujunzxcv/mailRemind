#!/usr/bin/env python3
# coding=utf-8
import json

import ccxt

if __name__ == '__main__':
    bitmex = ccxt.bitmex()
    bitmex.apiKey = ""
    bitmex.secret = "-"
    ticker = bitmex.privateGetPosition()
    result_json = bitmex.json(ticker)
    print(result_json)
    ss = json.loads(result_json)
    print(ss)
