import requests
import pprint

def get_all_coin_data(instType="SPOT",url = "https://www.okx.com/api/v5/market/tickers?instType=SWAP"):
    params = {
        'instType': instType,           # 产品类型
        'uly': '',                      # 标的指数
        'instFamily': ''                # 交易品种
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data
    
    
def get_listing_price(inst_id = "BTC-USDT",url = "https://www.okx.com/api/v5/market/candles"):
    params = {
        'instId': inst_id,  # 交易对ID，例如BTC-USDT
        'bar': '1D',        # 时间间隔，例如1D（一天）
        'limit': 1          # 限制结果数量
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'data' in data and data['data']:
        listing_price = data['data'][0][1]  # 获取开盘价
        return listing_price
    else:
        return None
    
def get_single_history_candle(inst_id = "BTC-USDT",url = "https://www.okx.com//api/v5/market/history-candles?instId=BTC-USDT"):
    params = {
        'instId': inst_id,  # 交易对ID，例如BTC-USDT
        "after": "",
        "before": "",
        "bar": "",
        "limit": ""
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

if __name__ == "__main__":
    # data = get_all_coin_data()
    # with open ("all_coin_data.txt", "w") as f:
    #     for item in data["data"]:
    #         string_temp=str(item["instId"])
    #         # print(string_temp.split('-')[0])
    #         f.write(string_temp.split('-')[0] + "\n")

    data1 = get_single_history_candle()
    print(data1)