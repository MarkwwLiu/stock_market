import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import json
import sys
import os

# 添加src目錄到Python路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils.logger import logger

def get_date_range(period):
    """根據輸入的期間返回開始和結束日期"""
    end_date = datetime.now()

    if period == '1w':
        start_date = end_date - timedelta(days=7)
        period_name = '一週'
    elif period == '1m':
        start_date = end_date - timedelta(days=30)
        period_name = '一個月'
    elif period == '3m':
        start_date = end_date - timedelta(days=90)
        period_name = '三個月'
    elif period == '6m':
        start_date = end_date - timedelta(days=180)
        period_name = '六個月'
    elif period == '1y':
        start_date = end_date - timedelta(days=365)
        period_name = '一年'
    elif period == '3y':
        start_date = end_date - timedelta(days=365*3)
        period_name = '三年'
    else:
        try:
            days = int(period)
            start_date = end_date - timedelta(days=days)
            period_name = f'{days}天'
        except ValueError:
            logger.error(f"無效的期間參數: {period}")
            return None, None, None

    return start_date, end_date, period_name

def get_stock_data(symbol, period='1m'):
    """獲取股票或ETF的歷史數據"""
    # 判斷是否為美股代碼
    is_us_stock = not symbol.endswith('.TW') and not symbol.startswith('^')

    # 台灣股票代碼需要加上.TW後綴（如果不是美股且不是指數）
    if not is_us_stock and not symbol.startswith('^') and not symbol.endswith('.TW'):
        symbol = f"{symbol}.TW"

    # 獲取股票資訊
    stock = yf.Ticker(symbol)

    # 獲取日期範圍
    start_date, end_date, period_name = get_date_range(period)
    if start_date is None:
        return None, None, None

    # 獲取股票名稱
    try:
        stock_name = stock.info.get('longName', symbol)
    except:
        stock_name = symbol

    logger.info(f"正在獲取 {stock_name} {period_name}數據...")

    # 獲取歷史數據
    df = stock.history(start=start_date, end=end_date)

    # 保留收盤價和成交量
    df = df[['Close', 'Volume']]

    # 將索引（日期）重置為普通列
    df = df.reset_index()

    # 將日期格式轉換為更易讀的格式
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

    # 按日期排序（從舊到新）
    df = df.sort_values('Date')

    # 計算漲跌幅和實際漲跌點數
    df['Change'] = df['Close'].pct_change() * 100
    df['Change'] = df['Change'].round(2)
    df['Points'] = df['Close'].diff()
    df['Points'] = df['Points'].round(2)

    # 將成交量轉換為百萬股
    df['Volume'] = df['Volume'] / 1000000
    df['Volume'] = df['Volume'].round(2)

    # 計算交易日數量
    trading_days = len(df)

    # 計算日曆天數
    calendar_days = (pd.to_datetime(df['Date'].iloc[-1]) - pd.to_datetime(df['Date'].iloc[0])).days + 1

    # 計算非交易日數量
    non_trading_days = calendar_days - trading_days

    logger.info(f"交易日數量：{trading_days}天")
    logger.info(f"非交易日數量（假日）：{non_trading_days}天")
    logger.info("注意：股市在週末和假日不交易，因此這些日期的數據會缺失")

    return df, period_name, stock_name

def save_stock_data(df, symbol, period):
    """保存股票數據到CSV和JSON文件"""
    # 將數據保存到 CSV 文件
    output_filename = f'data/csv/{symbol.replace(".TW", "")}_data_{period}.csv'
    df.to_csv(output_filename, index=False)

    # 將數據保存到 JSON 文件
    json_filename = f'data/json/{symbol.replace(".TW", "")}_data_{period}.json'
    json_data = df.to_dict(orient='records')
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    return output_filename, json_filename
