import re
import os
import sys
import json
import time
import shutil
import pprint
from loguru import logger
import matplotlib.pyplot as plt
from binance_info_request import BinanceInfoRequest
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

if __name__ == "__main__":
    Binance_handler = BinanceInfoRequest()
    # result = Binance_handler.get_all_exchange_coin_name_list_U_contracts()
    # result = Binance_handler.get_single_coin_kline_data("BTCUSDT")
    result = Binance_handler.get_single_coin_name_list("BTCUSDT")

    # logger.info(f"num total exchange coin is : {len(result)}")

    # jh.dump_json_to_file("./data/all_coin_u_contracts.json", result)
    jh.dump_json_to_file("./data/btc_trade_volume_list.json", result)

    logger.info(f"info collect over, please check ./data/all_coin_u_contracts.json")

    time = [item[0] for item in result]
    price = [float(item[1]) for item in result]

    plt.plot(time, price)
    plt.xlabel('时间')
    plt.ylabel('价格')
    plt.title('时间和价格')
    plt.show()