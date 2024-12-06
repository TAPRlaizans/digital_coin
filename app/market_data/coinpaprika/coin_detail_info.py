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

# limit
# 60 time per hour
# 20000 time per month
time_request = 3600

url_coinpaprika = "https://api.coinpaprika.com/v1/coins"
path_coin_detail_info_output = "./data/coins_detail_info/coins_detail_info.json"

def get_coin_detail_info(url_coinpaprika, coin_id):
    url_detail_coin_coinpaprika = url_coinpaprika + '/' + coin_id
    try:
        json_coin_detail_data = rh.get_response_json(url_detail_coin_coinpaprika)
    except Exception as e:
        logger.error(f"get coin detail info error: {e}")
    return json_coin_detail_data

def get_coin_list_detail_info(url_coinpaprika, path_output_file, arry_is_new_coin):
    list_coin_detail_info = []
    try:
        for coin_id in arry_is_new_coin:
            url_detail_coin_coinpaprika = url_coinpaprika + '/' + coin_id
            json_coin_detail_data = rh.get_response_json(url_detail_coin_coinpaprika)
            list_coin_detail_info.append(json_coin_detail_data)
    except Exception as e:
        logger.error(f"get coin detail info error: {e}")
        return list_coin_detail_info 

def append_coin_detail_info_to_file(path_output_file, single_coin_data):
    object_source = jh.read_json_file_to_object(path_output_file)
    for item in object_source:
        if item['id'] == single_coin_data['id']:
            logger.info(f"{single_coin_data['id']} already exist in file {path_output_file}")
            return
    object_source.append(single_coin_data)
    with open(path_output_file, "w", encoding="utf-8") as f:
        json.dump(object_source, f, indent=4, ensure_ascii=False)
    logger.info(f"append {single_coin_data['id']} to file {path_output_file}")
    return True
    
# get new coin id index
    # json_data = rh.get_response_json(url_coinpaprika)

    # title = ["id", "symbol", "name", "is_active", "is_new"]
    # excle_data = []

    # list_is_new_coin = []
    # arry_is_new_coin = []

    # for item in json_data:
    #     if item['is_new'] == True:
    #         list_is_new_coin.append(item)
    #         arry_is_new_coin.append(item['id'])

    # if len(list_is_new_coin) == 0:
    #     logger.info("no new coin in coinpaprika")
    # else:  
    #     logger.info(f"{len(list_is_new_coin)} new coin in coinpaprika")
    #     jh.dump_json_to_file("./data/new_coin/new_coin_coinpaprika.json", list_is_new_coin)

#get every new coin id detail info 
single_coin_detail_info = get_coin_detail_info(url_coinpaprika, "1000sats-1000sats-ordinals")

append_coin_detail_info_to_file(path_coin_detail_info_output, single_coin_detail_info)

logger.info("get all new coin detail info done")