import requests
import pandas as pd
import numpy as np
from datetime import datetime
import time
import random
from deap import base, creator, tools, algorithms
import os

def get_symbols():
    Info = requests.get('https://fapi.binance.com/fapi/v1/exchangeInfo')
    symbols = [s['symbol'] for s in Info.json()['symbols'] 
               if s['contractType'] == 'PERPETUAL' and s['status'] == 'TRADING' and s['quoteAsset'] == 'USDT']
    symbols = [s for s in symbols if s.endswith('USDT')]
    return symbols

def get_klines(symbol='BTCUSDT', start='2024-01-01', end='2024-07-01', interval='1h'):
    klines = []
    start_time = int(time.mktime(datetime.strptime(start, "%Y-%m-%d").timetuple())) * 1000
    end_time = int(time.mktime(datetime.strptime(end, "%Y-%m-%d").timetuple())) * 1000
    base_url = 'https://fapi.binance.com/fapi/v1/klines'
    
    while start_time < end_time:
        url = f"{base_url}?symbol={symbol}&interval={interval}&startTime={start_time}&endTime={end_time}&limit=1000"
        data = requests.get(url).json()
        if not data:
            break
        klines += data
        start_time = data[-1][0] + 1
    
    df = pd.DataFrame(klines, columns=['time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df.set_index('time', inplace=True)
    df = df[['close']].astype(float)
    return df

def fetch_data(symbols, start_date, end_date):
    df_dict = {}
    for symbol in symbols:
        print(f"正在下载 {symbol} 的数据...")
        df_dict[symbol] = get_klines(symbol=symbol, start=start_date, end=end_date)
    
    df_close = pd.concat({symbol: df['close'] for symbol, df in df_dict.items()}, axis=1)
    df_close.dropna(how='all', inplace=True)
    return df_close

# 定义适应度函数
def evaluate(individual, df_close):
    symbol1, symbol2 = individual
    correlation = df_close[symbol1].corr(df_close[symbol2])
    return correlation,

# 自定义交叉操作
def cxTuple(ind1, ind2):
    return creator.Individual(ind1), creator.Individual(ind2)

# 自定义变异操作
def mutTuple(individual, symbols, indpb):
    if random.random() < indpb:
        idx = random.randint(0, len(individual)-1)
        new_symbol = random.choice(symbols)
        while new_symbol == individual[idx] or (idx == 0 and new_symbol == individual[1]) or (idx == 1 and new_symbol == individual[0]):  # 确保新的符号与原符号不同且不重复
            new_symbol = random.choice(symbols)
        individual = list(individual)
        individual[idx] = new_symbol
        individual = creator.Individual(tuple(individual))
    return individual,

# 相关性分析与NSGA-II实现
def nsga2_correlation_analysis(df_close):
    symbols = df_close.columns.tolist()
    pairs = [(symbols[i], symbols[j]) for i in range(len(symbols)) for j in range(i+1, len(symbols))]

    # 定义NSGA-II
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", tuple, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attr_pair", random.choice, pairs)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_pair)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("mate", cxTuple)
    toolbox.register("mutate", mutTuple, symbols=symbols, indpb=0.2)
    toolbox.register("select", tools.selNSGA2)
    toolbox.register("evaluate", evaluate, df_close=df_close)

    pop = toolbox.population(n=100)
    hof = tools.ParetoFront()

    algorithms.eaMuPlusLambda(pop, toolbox, mu=100, lambda_=200, cxpb=0.7, mutpb=0.2, ngen=40, stats=None, halloffame=hof, verbose=False)

    # 重新计算适应度
    for ind in pop:
        ind.fitness.values = toolbox.evaluate(ind)
    
    # 获取相关性系数并确保唯一性
    hof_pairs = list(set((ind[0], ind[1], ind.fitness.values[0]) for ind in pop if ind[0] != ind[1]))  # 确保不输出相同的币种对
    
    # 排序相关性系数
    sorted_pairs = sorted(hof_pairs, key=lambda x: x[2], reverse=True)
    
    return sorted_pairs

if __name__ == "__main__":
    try:
        del creator.FitnessMax
        del creator.Individual
    except AttributeError:
        pass

    start_date = '2024-01-01'
    end_date = '2024-07-01'

    symbols = get_symbols()

    df_close = fetch_data(symbols, start_date, end_date)
    
    sorted_pairs = nsga2_correlation_analysis(df_close)
    print("使用非支配排序遗传算法 II (NSGA-II)：")
    # 提取并排序相关性系数
    correlation_list = []
    for i in range(len(df_close.columns)):
        for j in range(i + 1, len(df_close.columns)):
            correlation_list.append((df_close.iloc[:, i].corr(df_close.iloc[:, j]), df_close.columns[i], df_close.columns[j]))
    
    correlation_list.sort(reverse=True, key=lambda x: x[0])

    result = []
    for correlation, symbol1, symbol2 in correlation_list:
        combine = f"{symbol1}, {symbol2}： {correlation:.4f}"
        result.append(combine)
    
    print("正相关性最高的前20组：")
    for res in result[:20]:
        print(res)
    
    print("负相关性最高的后20组：")
    for res in reversed(result[-20:]):
        print(res)
