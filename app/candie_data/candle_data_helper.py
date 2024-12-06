import requests

binance = {
    "api_key": "UJG2KRTWGhQu2NxRPrxTvkgNuzYqynyzUG7JUsnFPZd2ENvv4sgGaLS7CdSRGO35",
    "api_secret": "UJG2KRTWGhQu2NxRPrxTvkgNuzYqynyzUG7JUsnFPZd2ENvv4sgGaLS7CdSRGO35",
    "limits": 6
}

okx ={
    "api_key": "",
    "api_secret": "",
    "limits": 6
}

bybit = {
    "api_key": "upFLJW3jFMHLl76wyB",
    "api_secret": "85lMmWI1RMWIF77LKUCWmBuRajMGQUVx1hoN",
    "limits": 6
}

coinmarketcap = {
    "api_key": "0a87431e-5b19-48be-8084-855ef00f1816",
    "limits": 6
}

class CandleHelper(object):
    def get_candle_data_from_binance(trading_pair='BTCUSDT',
        interval = '1h',     
        limit = 20           
    ):
        headers = {'X-MBX-APIKEY': binance["api_key"]}
        string_url = 'https://data-api.binance.vision/api/v3/klines?symbol='
        complete_url = string_url + trading_pair
        response = requests.get(complete_url, headers=headers, params={"interval": "1h"})
        data = response.json()  
        return data