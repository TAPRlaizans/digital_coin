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

url_coinpaprika = "https://api.coinpaprika.com/v1/coins"

#get new coin id index
json_data = rh.get_response_json(url_coinpaprika)

title = ["id", "symbol", "name", "is_active", "is_new"]
excle_data = []

list_is_new_coin = []
arry_is_new_coin = []

for item in json_data:
    if item['is_new'] == True:
        list_is_new_coin.append(item)
        arry_is_new_coin.append(item['id'])

if len(list_is_new_coin) == 0:
    logger.info("no new coin in coinpaprika")
else:  
    logger.info(f"{len(list_is_new_coin)} new coin in coinpaprika")
    jh.dump_json_to_file("./data/new_coin/new_coin_coinpaprika.json", list_is_new_coin)

#get every new coin id detail info 
url_detail_coinpaprika = "https://api.coinpaprika.com/v1/coins/"

for coin_id in arry_is_new_coin:
    url_detail_coin_coinpaprika = url_detail_coinpaprika + coin_id
    json_coin_detail_data = rh.get_response_json(url_detail_coin_coinpaprika)
    jh.append_json_to_file("./data/new_coin/detail_coinpaprika.json", json_coin_detail_data)

logger.info("get all new coin detail info done")