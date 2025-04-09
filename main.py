import argparse
import os
import sys
import json
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

# 添加src目錄到Python路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from src.utils.logger import logger
from src.data.stock_data import get_stock_data, save_stock_data
from src.visualization.chart import create_stock_chart

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Microsoft JhengHei', 'PingFang HK', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False  # 用來正常顯示負號

def create_directories():
    """創建必要的目錄"""
    directories = ['logs', 'data/csv', 'data/json', 'data/charts']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"創建目錄：{directory}")

def process_single_stock(symbol, period):
    """處理單個股票"""
    result = get_stock_data(symbol, period)
    if result is None:
        return None

    df, period_name, stock_name = result

    # 保存數據
    csv_file, json_file = save_stock_data(df, symbol, period)

    # 創建圖表
    chart_file = create_stock_chart(df, symbol, period, stock_name, period_name)

    # 顯示數據統計
    logger.info("=== 數據統計 ===")
    logger.info(f"股票名稱：{stock_name}")
    logger.info(f"數據期間：{df['Date'].iloc[0]} 到 {df['Date'].iloc[-1]}")
    logger.info(f"起始價格：{df['Close'].iloc[0]:,.2f}")
    logger.info(f"最新價格：{df['Close'].iloc[-1]:,.2f}")
    total_change = ((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0] * 100)
    total_points = df['Close'].iloc[-1] - df['Close'].iloc[0]
    logger.info(f"期間漲跌幅：{total_change:,.2f}% ({total_points:+,.2f} 點)")

    # 計算平均成交量
    avg_volume = df['Volume'].mean()
    logger.info(f"平均成交量：{avg_volume:,.2f} 百萬股")

    logger.info("=== 最近5個交易日數據 ===")
    logger.info("日期\t\t收盤價\t\t漲跌幅(%)\t漲跌點數\t成交量(百萬股)")
    logger.info("-" * 80)
    for _, row in df.tail().iterrows():
        logger.info(f"{row['Date']}\t{row['Close']:,.2f}\t{row['Change']:+.2f}%\t{row['Points']:+.2f}\t{row['Volume']:,.2f}")

    return df, period_name, stock_name

def process_all_stocks(config_file='config.json'):
    """處理配置文件中列出的所有股票"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        stocks = config.get('stocks', [])
        default_period = config.get('default_period', '1m')

        if not stocks:
            logger.error(f"配置文件中沒有找到股票代碼")
            return

        logger.info(f"開始處理 {len(stocks)} 支股票...")
        for symbol in stocks:
            try:
                logger.info(f"處理股票：{symbol}")
                process_single_stock(symbol, default_period)
            except Exception as e:
                logger.error(f"處理股票 {symbol} 時發生錯誤：{str(e)}")
                continue

        logger.info("所有股票處理完成")
    except FileNotFoundError:
        logger.error(f"找不到配置文件：{config_file}")
    except json.JSONDecodeError:
        logger.error(f"配置文件格式錯誤：{config_file}")
    except Exception as e:
        logger.error(f"處理配置文件時發生錯誤：{str(e)}")

def main():
    parser = argparse.ArgumentParser(description='獲取股票歷史數據並生成圖表')
    parser.add_argument('--symbol', type=str, help='股票代碼（例如：2330, 0050）')
    parser.add_argument('--period', type=str, default='1m',
                      help='時間範圍（1w, 1m, 3m, 6m, 1y, 3y）')
    parser.add_argument('--config', type=str, default='config.json',
                      help='配置文件路徑')
    parser.add_argument('--all', action='store_true',
                      help='處理配置文件中的所有股票')

    args = parser.parse_args()

    # 創建必要的目錄
    create_directories()

    if args.all:
        process_all_stocks(args.config)
    elif args.symbol:
        process_single_stock(args.symbol, args.period)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
