import mplfinance as mpf
import matplotlib.pyplot as plt

@staticmethod
def plot_candle_data(price, time):
    plt.plot(price, time)
    plt.title('bitcoin 1d klines') 
    plt.xlabel('时间')  
    plt.ylabel('价格')  
    plt.show()
    return True