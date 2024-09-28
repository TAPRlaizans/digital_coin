
import requests
import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from itertools import combinations
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

string_program_name = os.path.basename(__file__).split('.')[0]
string_program_output_name = string_program_name + "_output"
path_current = os.path.dirname(__file__)

from module.time_module.time_module import Time_module
from module.file.file import File
# proxy = {
#     'http': 'http://127.0.0.1:10100',
#     'https': '127.0.0.1:10100'
# }

def get_symbols():
    url = 'https://www.okx.com/api/v5/public/instruments?instType=SWAP'
    # response = requests.get(url, proxies=proxy)
    response = requests.get(url)
    data = response.json()
    symbols = [symbol['instId'] for symbol in data['data'] if 'USDT' in symbol['instId']]
    
    # 排除特定符号
    excluded_symbols = ['ETH-USDT-SWAP', 'BTC-USDT-SWAP', 'USDC-USDT-SWAP', 'TUSD-USDT-SWAP', 'FDUSD-USDT-SWAP','VENOM-USDT-SWAP']
    symbols = [symbol for symbol in symbols if symbol not in excluded_symbols]
    
    return symbols

def get_historical_klines(symbol, bar='1D', limit=100):
    url = f'https://www.okx.com/api/v5/market/candles?instId={symbol}&bar={bar}&limit={limit}'
    while True:
        try:
            # response = requests.get(url, proxies=proxy, timeout=10)
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # 如果响应状态码不是200, 引发HTTPError异常
            data = response.json()['data']
            # 转换为数据框并按时间排序
            df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'quote_volume', 'unknown1', 'unknown2'])
            df['close'] = df['close'].astype(float)
            df['timestamp'] = pd.to_numeric(df['timestamp'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df = df.sort_values('timestamp')
            return df[['timestamp', 'close']]
        except (requests.exceptions.RequestException, ValueError, KeyError) as e:
            print(f"Error fetching data for {symbol}. Retrying in 5 seconds...")
            time.sleep(5)  # 等待5秒后重试

# 计算相关性
def calculate_correlations(symbols):
    close_prices = {}
    for symbol in symbols:
        # print(f"Fetching data for {symbol}")
        df = get_historical_klines(symbol)
        if df is not None:
            close_prices[symbol] = df['close']
    
    close_prices_df = pd.DataFrame(close_prices).dropna(axis=1)  # 去掉包含 NaN 值的列
    correlations = {}
    
    for (symbol1, symbol2) in combinations(close_prices_df.columns, 2):
        if close_prices_df[symbol1].nunique() > 1 and close_prices_df[symbol2].nunique() > 1:  # 确保数据不是常数
            correlation, _ = pearsonr(close_prices_df[symbol1], close_prices_df[symbol2])
            correlations[(symbol1, symbol2)] = correlation
    
    return correlations


# 获取正相关和负相关的前40组
def get_top_correlations(correlations, top_n=40):
    sorted_correlations = sorted(correlations.items(), key=lambda x: x[1], reverse=True)
    top_positive = sorted_correlations[:top_n]
    top_negative = sorted(sorted_correlations, key=lambda x: x[1])[:top_n]
    return top_positive, top_negative

def proc():
    print(os.path.join(path_current, string_program_output_name))
    File.mkdirFile(os.path.join(path_current, string_program_output_name))

    print(f"process one time {Time_module.get_current_timestamp()}")
    print("processing ...")
    symbols = get_symbols()
    correlations = calculate_correlations(symbols)
    top_positive, top_negative = get_top_correlations(correlations)
    
    print("正相关的前40组:")
    temp_path_file = os.path.join(path_current, string_program_output_name, f"{Time_module.get_current_timestamp()}.txt")
    temp_path_file_only_pair = os.path.join(path_current, string_program_output_name, f"{Time_module.get_current_timestamp()}_only_pair.txt")
    with open(temp_path_file, "a", encoding="utf-8") as file:
        file.write("正相关的前40组:")
        for pair, corr in top_positive:
            file.write(f"\n{pair}: {corr}")
            print(f"{pair}: {corr}")
    
        print("\n负相关的前40组:")
        file.write("\n负相关的前40组:")
        for pair, corr in top_negative:
            file.write(f"\n{pair}: {corr}")
            print(f"{pair}: {corr}")
        
    with open(temp_path_file_only_pair, "a", encoding="utf-8") as file1:
        file1.write("正相关的前40组:")
        for pair, corr in top_positive:
            file1.write(f"\n{pair}")

        file1.write("\n负相关的前40组:")
        for pair, corr in top_negative:
            file1.write(f"\n{pair}")
    print("process done ...")

# 主函数
def main(time_interval):
    print(f"time_interval: {time_interval}")
    while True:
        try:
            proc()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)  # 等待5秒后重试
        time.sleep(time_interval)

if __name__ == "__main__":
    time_interval = 60*10  #秒
    main(time_interval)
