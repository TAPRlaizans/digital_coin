# 导入相关模块
import os
import sys
import time
import pprint
import openpyxl
import requests
import numpy as np
import tushare as ts
import pandas as pd
import loguru as lg

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
PARENT_PARENT_DIR = os.path.dirname(PARENT_DIR)
PARENT_PARENT_PARENT_DIR = os.path.dirname(PARENT_PARENT_DIR)
sys.path.append(BASE_DIR)
sys.path.append(PARENT_DIR)
sys.path.append(PARENT_PARENT_DIR)
sys.path.append(PARENT_PARENT_PARENT_DIR)
from common.json_helper import ArgsParse as ap
from common.logger import Logger, LogLevel 
from common.time_until import TimeUntil as tm
from common.excle_helper import ExcleHelper as ex
from common.candle_data_helper import CandleHelper as ch

def get_trading_pair_raw_data(trading_pair):
    return True

def get_moment_info(raw_data, process_mode="substract"):
    return True

def plot_concentrated_chart(raw_data, moment_info):
    return True

if __name__ == '__main__':
    pth_json_file = "./moment_trading.json"
    param_object =ap.read_json_file_to_object(pth_json_file)

    data = ch.get_candle_data_from_binance()
    ex.save_excle(data)

    data_wif = ch.get_candle_data_from_binance("WIFUSDT", "1h")
    ex.save_excle(data_wif, "WIF_data.xlsx")

    raw_data = get_trading_pair_raw_data(param_object["trading_code"])
    
    if raw_data != True:
        print("get raw data failed!")
        exit(-1)
    
    moment_info = get_moment_info(raw_data, param_object["process_mode"])
    if moment_info != True: 
        print("get raw data failed!")
        exit(-1)

    plot_concentrated_chart(raw_data, moment_info)