from config_strategy_api import session

# Get symbols that are tradeable
def get_tradeable_symbols():
    print("111111111111")
    # Get available symbols
    sym_list = []
    print("222222222")
    symbols = session.query_symbol()
    print("33333333")
    if "ret_msg" in symbols.keys():
        if symbols["ret_msg"] == "OK":
            symbols = symbols["result"]
            for symbol in symbols:
                if symbol["quote_currency"] == "USDT" and symbol["status"] == "Trading": # symbol["maker_fee"]) < 0 removed as ByBit changed terms
                    sym_list.append(symbol)

    # Return ouput
    return sym_list
