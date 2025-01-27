import re
import os
import sys
import json
import time
import shutil
import pprint
from loguru import logger
# from googletrans import Translator

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

class BinanceInfoRequest:
    def __init__(self, logger=None) -> None:
        self.logger = logger
        self.url_exchange_all_coin_info_u_contracts = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
        self.url_exchange_all_coin_info_spot = 'https://api.binance.com/api/v3/exchangeInfo'
        self.url_exchange_all_coin_klines = 'https://fapi.binance.com/fapi/v1/klines'

    #获取u本位合约的所有交易对信息
    def get_all_exchange_coin_name_list_U_contracts(self):
        all_coin_info = []
        response = rh.get_response_json(self.url_exchange_all_coin_info_u_contracts)
        assets = response.get('symbols')
        for item in assets:
            all_coin_info.append(item['symbol'])
        return all_coin_info 

    #获取现货的所有交易对信息
    def get_all_exchange_coin_name_list_spot(self):
        all_coin_info = []
        response = rh.get_response_json(self.url_exchange_all_coin_info_spot)
        assets = response.get('symbols')
        for item in assets:
            all_coin_info.append(item['symbol'])
        return all_coin_info
    
    #获得单个币种的k线数据
    #数据样例见路径：digital_coin/app/market_data/bianance/data/
    def get_single_coin_kline_data(self, symbol="BTCUSDT", interval='1h', limit=500):
        params = {
                    'symbol': {symbol},
                    'interval': {interval},
                    'startTime': None,
                    'endTime': None,
                    'limit': {limit}
                }
        response = rh.get_response_json(self.url_exchange_all_coin_klines, params)
        return response
    
    #获取单个币种的成交量数据
    def get_single_coin_name_list(self, symbol, interval='1h', limit=500):
        list_volume = []
        temp = self.get_single_coin_kline_data(symbol, interval, limit)
        for item in temp:
            list_volume.append([item[0], item[5]])
        return list_volume