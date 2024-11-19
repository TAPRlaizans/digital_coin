import requests
import feedparser
from datetime import datetime
import time
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
PARENT_PARENT_DIR = os.path.dirname(PARENT_DIR)
PARENT_PARENT_PARENT_DIR = os.path.dirname(PARENT_PARENT_DIR)
sys.path.append(BASE_DIR)
sys.path.append(PARENT_DIR)
sys.path.append(PARENT_PARENT_DIR)
sys.path.append(PARENT_PARENT_PARENT_DIR)
from module.time_module.time_module import Time_module

def fetch_rss_feed(url):
    response = requests.get(url)
    response.raise_for_status()  # 检查请求是否成功

    feed = feedparser.parse(response.content)
    return feed

def main():
    rss_url = "https://api.theblockbeats.news/v1/open-api/home-xml"  # 将此替换为你想请求的 RSS URL
    feed = fetch_rss_feed(rss_url)

    print(f"Feed Title: {feed.feed.title}")
    print(f"Feed Description: {feed.feed.description}")
    temp_index =0
    with open(f"./rss_reponse_{Time_module.get_current_timestamp()}.txt", "w+",encoding="utf-8") as f:
        for entry in feed.entries:
            # print(f"---------------context {temp_index}------------")
            temp_index +=1
            # print(f"\nTitle: {entry.title}")
            # print(f"Link: {entry.link}")
            # print(f"Published: {entry.published}")
            # print(f"Summary: {entry.summary}")
            f.write(f"---------------context {temp_index}------------")
            f.write(f"\nTitle: {entry.title}\n")
            f.write(f"Link: {entry.link}\n")
            f.write(f"Published: {entry.published}\n")
            f.write(f"Summary: {entry.summary}\n")

if __name__ == "__main__":
    main()