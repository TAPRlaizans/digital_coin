import requests

def get_all_coin_data(instType="SPOT",url = "https://www.okx.com/api/v5/market/tickers?instType=SWAP"):
    params = {
        'instType': instType,           # 产品类型
        'uly': '',                      # 标的指数
        'instFamily': ''                # 交易品种
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
