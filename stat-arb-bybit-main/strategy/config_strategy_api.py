"""
    API Documentation
    https://bybit-exchange.github.io/docs/linear/#t-introduction
"""

# API Imports
from pybit import usdt_perpetual

# CONFIG
mode = "test"
timeframe = 100
kline_limit = 1000
z_score_window = 21

# LIVE API
api_key_mainnet = ""
api_secret_mainnet = ""

# TEST API
api_key_testnet = "upFLJW3jFMHLl76wyB"
api_secret_testnet = "85lMmWI1RMWIF77LKUCWmBuRajMGQUVx1hoN"

# SELECTED API
api_key = api_key_testnet if mode == "test" else api_key_mainnet
api_secret = api_secret_testnet if mode == "test" else api_secret_mainnet

# SELECTED URL
api_url = "https://api-testnet.bybit.com" if mode == "test" else "https://api.bybit.com"

# SESSION Activation
session = usdt_perpetual.HTTP(
    endpoint=api_url,
    api_key=api_key,
    api_secret=api_secret
)
