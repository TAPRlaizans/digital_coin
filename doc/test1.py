import requests
import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from itertools import combinations
import time

# 设置代理
# proxy = {}
# proxy = {"http": "http://127.0.0.1:6152", "https": "127.0.0.1:6152"}

# 获取币种列表
def get_symbols():
    response = requests.get(url="https://www.okx.com/api/v5/public/instruments?instType=SWAP")
    data = response.json()
    symbols = [symbol['instId'] for symbol in data['data'] if 'USDT' in symbol['instId']]

    # 排除部分币种
    excluded_symbols = ['ETH-USDT-SWAP', 'BTC-USDT-SWAP', 'MDS-USDT-SWAP', 'TUSD-USDT-SWAP', 'FOID-USDT-SWAP', 'USDC-USDT-SWAP']
    symbols = [symbol for symbol in symbols if symbol not in excluded_symbols]

    return symbols

# 获取历史K线数据
def get_historical_klines(symbol, bar='1m', limit=100):
    url = f"https://www.okx.com/api/v5/market/candles?instId={symbol}&bar={bar}&limit={limit}"
    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()['data']
            df = pd.DataFrame(data)
            df = df[[0, 1, 2, 3, 4, 5, 6]]
            df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'quote_volume']
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df = df.sort_values('timestamp')
            df.set_index('timestamp', inplace=True)
            df = df.astype(float)
            return df
        except (requests.exceptions.RequestException, ValueError, IndexError, KeyError) as e:
            print(f"Error fetching data for {symbol}: {e}. Retrying in 5 seconds...")
            time.sleep(5)

# 计算相关性
def calculate_correlations(symbols):
    close_prices = {}
    for symbol in symbols:
        df = get_historical_klines(symbol)
        close_prices[symbol] = df['close']

    close_prices_df = pd.DataFrame(close_prices).fillna(method='ffill').fillna(method='bfill')  # 删除有缺失值的列
    correlations = {}
    for (symbol1, symbol2) in combinations(close_prices_df.columns, 2):
        if close_prices_df[symbol1].nunique() > 1 and close_prices_df[symbol2].nunique() > 1:  # 避免值恒定不变的情况
            correlation, _ = pearsonr(close_prices_df[symbol1], close_prices_df[symbol2])
            correlations[(symbol1, symbol2)] = correlation

    return correlations

# 获取前n个相关性最大的币种对
def get_top_correlations(correlations, top_n=20):
    sorted_correlations = sorted(correlations.items(), key=lambda x: x[1], reverse=True)
    top_positive = sorted_correlations[:top_n]
    top_negative = sorted(sorted_correlations, key=lambda x: x[1])[:top_n]
    return top_positive, top_negative

if __name__ == "__main__":
    symbols = get_symbols()
    correlations = calculate_correlations(symbols)
    top_positive, top_negative = get_top_correlations(correlations)

    print("\n前20个正相关的币种对:")
    for pair, corr in top_positive:
        print(f"{pair}: {corr}")

    print("\n前20个负相关的币种对:")
    for pair, corr in top_negative:
        print(f"{pair}: {corr}")