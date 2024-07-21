from bigmodule import M

# <aistudiograph>

# @param(id="m5", name="initialize")
def m5_initialize_bigquant_run(context):  # type: ignore
    from bigtrader.finance.commission import PerOrder

    # 系统已经设置了默认的交易手续费和滑点，要修改手续费可使用如下函数
    context.set_commission(PerOrder(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))

# @param(id="m5", name="handle_data")
def m5_handle_data_bigquant_run(context, data):  # type: ignore
    import pandas as pd

    # 下一个交易日不是调仓日，则不生成信号
    if not context.rebalance_period.is_signal_date(data.current_dt.date()):
        return

    # 从传入的数据 context.data 中读取今天的信号数据
    today_df = context.data[context.data["date"] == data.current_dt.strftime("%Y-%m-%d")]
    target_instruments = set(today_df["instrument"])

    # 获取当前已持有股票
    holding_instruments = set(context.get_account_positions().keys())

    # 卖出不在目标持有列表中的股票
    for instrument in holding_instruments - target_instruments:
        context.order_target_percent(instrument, 0)
    # 买入目标持有列表中的股票
    for i, x in today_df.iterrows():
        position = 0.0 if pd.isnull(x.position) else float(x.position)
        context.order_target_percent(x.instrument, position)

# @module(position="-437,-854", comment="""使用基本信息对股票池过滤""", comment_collapsed=False)
m1 = M.cn_stock_basic_selector.v6(  # type: ignore
    exchanges=["上交所", "深交所", "北交所"],
    list_sectors=["主板", "创业板", "科创板"],
    indexes=["中证500", "上证指数", "创业板指", "深证成指", "上证50", "科创50", "沪深300", "中证1000", "中证100", "深证100"],
    st_statuses=["正常", "ST", "*ST"],
    margin_tradings=["两融标的", "非两融标的"],
    sw2021_industries=["农林牧渔", "采掘", "基础化工", "钢铁", "有色金属", "建筑建材", "机械设备", "电子", "汽车", "交运设备", "信息设备", "家用电器", "食品饮料", "纺织服饰", "轻工制造", "医药生物", "公用事业", "交通运输", "房地产", "金融服务", "商贸零售", "社会服务", "信息服务", "银行", "非银金融", "综合", "建筑材料", "建筑装饰", "电力设备", "国防军工", "计算机", "传媒", "通信", "煤炭", "石油石化", "环保", "美容护理"],
    drop_suspended=True,
    m_name="m1"
)

# @module(position="-315,-727", comment="""因子特征""", comment_collapsed=False)
m2 = M.input_features_dai.v29(  # type: ignore
    input_1=m1.data,
    mode="表达式",
    expr="""
c_rank(float_market_cap) AS score_market_cap
momentum_5
score_market_cap - momentum_5 AS score
""",
    expr_filters="",
    expr_tables="cn_stock_prefactors",
    extra_fields="date, instrument",
    order_by="date, instrument",
    expr_drop_na=True,
    extract_data=False,
    m_name="m2"
)

# @module(position="-207,-592", comment="""持股数量、打分到仓位""", comment_collapsed=False)
m3 = M.score_to_position.v3(  # type: ignore
    input_1=m2.data,
    score_field="score DESC",
    hold_count=50,
    position_expr="1 AS position",
    total_position=1,
    extract_data=False,
    m_name="m3"
)

# @module(position="-98,-463", comment="""抽取预测数据""", comment_collapsed=False)
m4 = M.extract_data_dai.v17(  # type: ignore
    sql=m3.data,
    start_date="2021-01-01",
    start_date_bound_to_trading_date=True,
    end_date="2024-04-29",
    end_date_bound_to_trading_date=True,
    before_start_days=90,
    debug=False,
    m_name="m4"
)

# @module(position="43,-350", comment="""交易，日线，设置初始化函数和K线处理函数，以及初始资金、基准等""", comment_collapsed=False)
m5 = M.bigtrader.v20(  # type: ignore
    data=m4.data,
    start_date="2021-01-01",
    end_date="2024-04-29",
    initialize=m5_initialize_bigquant_run,
    handle_data=m5_handle_data_bigquant_run,
    capital_base=1000000,
    frequency="daily",
    product_type="股票",
    rebalance_period_type="月度交易日",
    rebalance_period_days="1",
    rebalance_period_roll_forward=True,
    backtest_engine_mode="标准模式",
    before_start_days=0,
    volume_limit=1,
    order_price_field_buy="open",
    order_price_field_sell="open",
    benchmark="沪深300指数",
    plot_charts=True,
    debug=False,
    backtest_only=False,
    m_name="m5"
)
# </aistudiograph>