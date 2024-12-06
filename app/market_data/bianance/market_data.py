import re
import os
import sys
import json
import time
import shutil
import pprint
from loguru import logger
from googletrans import Translator

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
PARENT_PARENT_DIR = os.path.dirname(PARENT_DIR)
PARENT_PARENT_PARENT_DIR = os.path.dirname(PARENT_PARENT_DIR)
sys.path.append(BASE_DIR)
sys.path.append(PARENT_DIR)
sys.path.append(PARENT_PARENT_DIR)
sys.path.append(PARENT_PARENT_PARENT_DIR)

from common.time_helper import TimeHelper as th
from common.json_helper import JsonHelper as jh
from common.logger import Logger, LogLevel 
from common.file_helper import FileHelper as fh
from common.math_helper import MathHelper as mh
from common.excle_helper import ExcleHelper as eh
from common.request_helper import RequestHelper as rh

# api description url: https://developers.binance.com/docs/zh-CN/derivatives/usds-margined-futures/market-data/rest-api/Kline-Candlestick-Data
# limit
# 60 time per hour
# 20000 time per month
time_request = 3600

# url_bianance = "https://developers.binance.com/docs/zh-CN/derivatives/usds-margined-futures/market-data/rest-api/Kline-Candlestick-Data/fapi/v1/klines"
url_bianance = "https://api.binance.com/api/v3/klines"
# url_bianance = "https://api.binance.com//fapi/v1/klines"
time_level = ["1d", "1h", "1m"]

for item in time_level:
    params = {
        "symbol": "ETHUSDT",
        "interval": item,
        # "startTime": 1000,
        # "endTime": 1000,
        "limit": 100
    }
    fh.check_folder_exist(f"./data/{params['symbol']}", True)

    reponse = rh.get_response_json(url_bianance, params)

    list_title = ["开盘时间", "开盘价", "最高价", "最低价", "收盘价", "收盘时间", "成交量", "成交额", "成交笔数", "主动买入成交量", "主动买入成交额", "请忽略该参数"]

    for item in reponse:
        item[0] = th.get_format_time(int(item[0]))

    eh.write_excel_xls(f"./data/{params['symbol']}/{params['symbol']}_{params['interval']}.xls", "data", reponse, list_title)