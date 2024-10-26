import requests
import matplotlib.pyplot as plt
import time
import pandas as pd
import os

current_folder = os.path.dirname(os.path.abspath(__file__))

def write_to_csv(df, filename, output_folder=current_folder):
    df.to_csv(filename, index=False)

# 获取当前时间戳
current_time = int(time.time() * 1000)  # 转换为毫秒
start_time = int(time.mktime(time.strptime('2023-01-01', '%Y-%m-%d'))) * 1000  # 今年的1月1日
end_time = int(time.mktime(time.strptime('2023-09-30', '%Y-%m-%d'))) * 1000  # 今年的9月30日

# 获取第一个交易对的K线数据
symbol1 = 'CRVUSDT'
url1 = f'https://fapi.binance.com/fapi/v1/klines?symbol={symbol1}&interval=15m&startTime={start_time}&endTime={end_time}'
response1 = requests.get(url1)
data1 = response1.json()
print("----data1----")
print(data1)
print(len(data1))

# 获取第二个交易对的K线数据
symbol2 = 'HFTUSDT'
url2 = f'https://fapi.binance.com/fapi/v1/klines?symbol={symbol2}&interval=15m&startTime={start_time}&endTime={end_time}'
response2 = requests.get(url2)
data2 = response2.json()
print("----data2----")
# print(data1)
print(len(data2))

data = {
    f"{symbol1}": data1,
    f"{symbol2}": data2
}
pair_trading = pd.DataFrame(data)
write_to_csv(pair_trading, f"{symbol1}_{symbol2}.csv")
# 解析数据并提取收盘价
close_prices1 = [float(entry[4]) for entry in data1]
close_prices2 = [float(entry[4]) for entry in data2]

# 计算价格差
price_diff = [price2 - price1 for price2, price1 in zip(close_prices2, close_prices1)]

# 绘制价格差图表
plt.figure(figsize=(12, 6))
plt.plot(price_diff, label='Price Difference (BTCUSDT - ETHUSDT)', color='blue')
plt.axhline(y=0, color='red', linestyle='--', label='Zero Axis')
plt.legend()
plt.title('Price Difference between BTCUSDT and ETHUSDT')
plt.xlabel('Time')
plt.ylabel('Price Difference (USDT)')
plt.show()