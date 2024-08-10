 #This example uses Python 2.7 and the python-request library.

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import datetime
import time
import os
import sys

# 获取当前脚本的路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取上两级目录的路径
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)

# 将上两级目录添加到系统路径中
sys.path.insert(0, grandparent_dir)
sys.path.insert(0, parent_dir)

gloabal_headers = {
'Accepts': 'application/json',
'X-CMC_PRO_API_KEY': '0a87431e-5b19-48be-8084-855ef00f1816',
}
air_drop_request_info={
    "url" : "https://pro-api.coinmarketcap.com/v1/cryptocurrency/airdrops",
    "parameters" : 
    {
    "start": 1,
    "limit": 100,
    "status": "ongoing",
    "id":1,
    "slug":"bitcoin",
    "symbol": "BTC"
}
}

  
def get_request(url, parameters=None, headers=None):
    session = Session()
    session.headers.update(gloabal_headers)
    response = None
    try:
        response = session.get(url, params=parameters)
        print(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    return response

# def get_current_timestamp():
#     now = datetime.now()
#     timestamp = now.strftime("%Y-%m-%d %H:%M")
#     return timestamp

def get_all_airdrop_info(airdrop_request_info):
    url=airdrop_request_info["url"]
    parameters=airdrop_request_info["parameters"]
    if url == None:
        print('Please provide url')
    
    if parameters == None:
        print('Please provide parameters')

    response = get_request(url, parameters, gloabal_headers)
    data = json.loads(response.text)

    current_timestamp = get_current_timestamp()
    file_name=f"airdrop_info_{current_timestamp}.json"
    with open(f'./{file_name}', 'w') as f:
        f.write(json.dumps(data, sort_keys=True, indent=4))

if __name__ == "__main__":
    get_all_airdrop_info(air_drop_request_info)