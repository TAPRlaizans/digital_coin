 #This example uses Python 2.7 and the python-request library.

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
PARENT_PARENT_DIR = os.path.dirname(PARENT_DIR)
sys.path.append(BASE_DIR)
sys.path.append(PARENT_DIR)
sys.path.append(PARENT_PARENT_DIR)
from module.time_module.time_module import Time_module

gloabal_headers = {
'Accepts': 'application/json',
'X-CMC_PRO_API_KEY': '0a87431e-5b19-48be-8084-855ef00f1816',
}
coin_id_request_info={
    "url" : "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map",
    "parameters" : 
    {
    "listing_status": "active",
    "start": 1,
    "limit": 500,
    "sort": "id",
    "symbol": "BTC",
    "aux": "platform,first_historical_data,last_historical_data,is_active"
}
}
  
def get_request(url, parameters=None, headers=None):
    session = Session()
    session.headers.update(gloabal_headers)
    response = None
    try:
        response = session.get(url, params=parameters)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    return response

def get_all_coin_id(coin_id_request_info):
    url=coin_id_request_info["url"]
    parameters=coin_id_request_info["parameters"]
    if url == None:
        print('Please provide url')
    
    if parameters == None:
        print('Please provide parameters')

    response = get_request(url, parameters, gloabal_headers)
    data = json.loads(response.text)

    current_timestamp = Time_module.get_current_timestamp()
    file_name="all_coin_id"
    with open(f'./{file_name}_{current_timestamp}.json', 'w') as f:
        f.write(json.dumps(data, sort_keys=True, indent=4))

if __name__ == "__main__":
    get_all_coin_id(coin_id_request_info)