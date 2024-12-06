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

path_coin_detail_info_output = "./data/coins_detail_info/coins_detail_info.json"

list_team_num = []

list_source_data = jh.read_json_file_to_object(path_coin_detail_info_output)

for source in list_source_data:
    if source['team'] != None:
        list_team_num.append({'id' : source['id'], 'length' : len(source['team'])}) 

sorted(list_team_num, key=lambda x: x['length'])
pprint.pprint(list_team_num)
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

logger.info("done")