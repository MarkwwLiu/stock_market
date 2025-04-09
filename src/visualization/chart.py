import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

# 添加src目錄到Python路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils.logger import logger

def get_date_ticks(df):
    """根據時間範圍返回適當的日期刻度"""
    dates = pd.to_datetime(df['Date'])
    return dates, [d.strftime('%Y-%m-%d') for d in dates]

def create_stock_chart(df, symbol, period, stock_name, period_name):
    """創建股票走勢圖"""
    # 創建子圖
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[2, 1])

    # 繪製走勢圖（上圖）
    plot_dates = pd.to_datetime(df['Date'])
    ax1.plot(plot_dates, df['Close'], marker='o', color='blue', label='收盤價')
    ax1.set_title(f'{stock_name} 近{period_name}走勢')
    ax1.set_ylabel('收盤價')
    ax1.legend()

    # 根據時間範圍調整日期刻度
    date_ticks, date_labels = get_date_ticks(df)
    ax1.set_xticks(date_ticks)
    ax1.set_xticklabels(date_labels, rotation=45)
    ax1.grid(True)

    # 繪製成交量圖（下圖）
    ax2.bar(plot_dates, df['Volume'], color='green', alpha=0.6)
    ax2.set_xlabel('日期')
    ax2.set_ylabel('成交量（百萬股）')
    ax2.set_xticks(date_ticks)
    ax2.set_xticklabels(date_labels, rotation=45)
    ax2.grid(True)

    # 調整圖表佈局，確保日期標籤不會被截斷
    plt.tight_layout()

    # 確保圖表目錄存在
    os.makedirs('data/charts', exist_ok=True)

    # 儲存圖表
    chart_filename = f'data/charts/{symbol.replace(".TW", "")}_chart_{period}.png'
    plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
    plt.close()  # 關閉圖形，釋放記憶體

    logger.info(f"圖表已儲存至：{chart_filename}")

    return chart_filename
