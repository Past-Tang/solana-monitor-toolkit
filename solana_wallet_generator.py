# 导入ccxt库，用于连接加密货币交易所
import ccxt
# 导入pandas库，用于数据处理和分析
import pandas as pd
# 导入ta库，用于技术指标计算
import ta
# 导入time模块，用于时间控制和延时
import time

# 初始化Binance交易所实例
exchange = ccxt.binance()


def get_all_symbols():
    """获取交易所所有可用的交易对"""
    # 加载交易所市场数据
    markets = exchange.load_markets()
    # 提取所有交易对名称
    symbols = list(markets.keys())
    return symbols


def fetch_ohlcv(symbol, timeframe, limit=100):
    """获取指定交易对的K线数据"""
    # 从交易所获取OHLCV数据
    data = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    # 将数据转换为DataFrame
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    # 转换时间戳为可读格式
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    # 设置时间戳为索引
    df.set_index('timestamp', inplace=True)
    return df


def calculate_indicators(df):
    """计算技术指标：布林带和RSI"""
    # 计算布林带上轨
    df['bollinger_hband'] = ta.volatility.BollingerBands(df['close']).bollinger_hband()
    # 计算布林带下轨
    df['bollinger_lband'] = ta.volatility.BollingerBands(df['close']).bollinger_lband()
    # 计算相对强弱指数RSI
    df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()
    return df


def monitor_market_all_symbols(timeframe='5m'):
    """监控所有交易对的市场变化"""
    # 获取所有交易对
    symbols = get_all_symbols()
    # 持续监控循环
    while True:
        # 遍历所有交易对
        for symbol in symbols:
            try:
                # 获取K线数据
                df = fetch_ohlcv(symbol, timeframe)
                # 计算技术指标
                df = calculate_indicators(df)

                # 获取最新的价格和技术指标
                last_row = df.iloc[-1]
                close_price = last_row['close']
                upper_band = last_row['bollinger_hband']
                lower_band = last_row['bollinger_lband']
                rsi = last_row['rsi']

                # 检查是否达到天地线条件
                if close_price > upper_band:
                    print(f"{symbol}: Price is above the upper Bollinger Band. Potential top detected at {close_price}")
                elif close_price < lower_band:
                    print(
                        f"{symbol}: Price is below the lower Bollinger Band. Potential bottom detected at {close_price}")

                # 输出当前RSI值
                print(f"{symbol}: Current RSI: {rsi}")

            except Exception as e:
                # 处理数据获取异常
                print(f"Error fetching data for {symbol}: {e}")

        # 每5分钟检查一次
        time.sleep(300)


# 启动监控
monitor_market_all_symbols()
