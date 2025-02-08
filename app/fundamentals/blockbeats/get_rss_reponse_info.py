import os
import sys
import time
import requests
import feedparser
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

def fetch_rss_feed(url):
    response = requests.get(url)
    response.raise_for_status()  

    feed = feedparser.parse(response.content)
    return feed

def main():
    while True:
        logger.info("started fetch one time info from blockbeats")
        rss_url = "https://api.theblockbeats.news/v1/open-api/home-xml" 
        feed = fetch_rss_feed(rss_url)

        string_current_time = th.get_time_stamp_format()
        string_txt_absolute_path = os.path.join(os.path.dirname(fh.get_current_file_path()),f"rss_reponse_{string_current_time}.txt")
        with open(f"{string_txt_absolute_path}", "w+",encoding="utf-8") as f:
            for entry in feed.entries:
                f.write(f"\nTitle: {entry.title}\n")
                f.write(f"Link: {entry.link}\n")
                f.write(f"Published: {entry.published}\n")
                f.write(f"Summary: {entry.summary}\n")

        logger.info(f"finished one time info from blockbeats {string_current_time}, file path: {string_txt_absolute_path}")
        logger.info(f"waiting for next time fetch")
        th.time_sleep(5, 'm')

if __name__ == "__main__":
    main()