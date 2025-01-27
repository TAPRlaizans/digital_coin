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
from common.email_helper import EmailHelper 

# limit
# 60 time per hour
# 20000 time per month
time_request = 3600
check_time_interval = 43200  # 12小时检查一次
time_append_to_file = 0

url_coinpaprika = "https://api.coinpaprika.com/v1/coins"
path_all_coins_info = "./data/all_coin_info/all_coin_info.json"
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
    time_append_to_file = time_append_to_file + 1
    return True
    
def check_coin_id_exist(source_data, dest_id):
    for item in source_data:
        if item['id'] == dest_id:
            return True
    return False
        
if __name__ == "__main__":
    #create email helper
    email_helper = EmailHelper()

    # get new coin id index
    title = ["id", "symbol", "name", "is_active", "is_new"]
    flag_exits = False
    excle_data = []
    list_is_new_coin = []
    arry_is_new_coin = []

    list_source_data = jh.read_json_file_to_object(path_all_coins_info)

    while True:
        logger.info("check one time coinpaprika new coin!")
        list_reponse_data = rh.get_response_json(url_coinpaprika)
        
        jh.dump_json_to_file(f"./data/all_coin_info/check_coinpaprika_{th.get_time_stamp_format()}.json", list_reponse_data)

        #依次检查response数据里面相比于文件内部有没有新币种
        #只检查币种ID，不检查币种细节
        for item_respone in list_reponse_data:
            if not check_coin_id_exist(list_source_data, item_respone['id']):
                list_is_new_coin.append(item_respone)
                arry_is_new_coin.append(item_respone['id'])
                single_coin_detail_info = get_coin_detail_info(url_coinpaprika, item_respone['id'])
                append_coin_detail_info_to_file(path_coin_detail_info_output, single_coin_detail_info)
        
        #上面完成了所有币种检查，和币种细节信息的存储
        #发送邮件进行提醒，有新币种才进行提醒
        if len(arry_is_new_coin) != 0:
            #send a notification to email
            subject = "新币种检查"
            body = f"发现 {len(arry_is_new_coin)} 个新币种，注意检查！"
            email_helper.send_email()

            logger.info(f"find {len(arry_is_new_coin)} new coin!")
            logger.info(arry_is_new_coin)
        time_append_to_file = 0
        th.sleep_s(check_time_interval)

