import os
import sys
import time
import requests
import feedparser
from openai import OpenAI
from loguru import logger
from datetime import datetime

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


def main():
    path_key_json_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(fh.get_current_file_path())))), "common", "all_platform_api_key.json")
    key_object = jh.read_json_file_to_object(path_key_json_file)

    while True:
        client = OpenAI(api_key=key_object["deepseek"]["api_key"], base_url="https://api.deepseek.com")

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Hello"},
            ],
            stream=False
        )
        print(response.choices[0].message.content)
        th.time_sleep(5, 's')
        
if __name__ == "__main__":
    main()