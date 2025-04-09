# 股市資料分析工具

這是一個用於獲取和分析股票市場數據的Python工具。該工具可以獲取台股指數（TWII）、台股個股以及美股數據，並生成CSV、JSON文件和趨勢圖。

## 功能特點

- 支持獲取台股指數（TWII）和台股個股數據
- 支持獲取美股數據（如：AAPL、GOOGL、MSFT等）
- 支持多種時間範圍：1週、1個月、3個月、6個月、1年、3年
- 自動計算漲跌幅和實際漲跌點數
- 自動計算成交量（以百萬股為單位）
- 生成高品質的趨勢圖，包含：
  - 股價走勢圖（含收盤價）
  - 成交量圖
- 支持批量處理多個股票代碼
- 自動處理非交易日（週末和假日）的數據缺失
- 詳細的日誌記錄

## 安裝需求

- Python 3.6+
- 需要安裝的套件：
  - yfinance
  - pandas
  - matplotlib
  - numpy

可以使用以下命令安裝所需套件：
```bash
pip install -r requirements.txt
```

## 使用方法

### 台股分析

```bash
# 分析台股指數
python main.py --symbol ^TWII --period 1m

# 分析台股個股
python main.py --symbol 2330 --period 1m
```

### 美股分析

```bash
# 分析美股個股（直接使用美股代碼）
python main.py --symbol AAPL --period 1m
python main.py --symbol GOOGL --period 1m
python main.py --symbol MSFT --period 1m

# 分析美股指數
python main.py --symbol ^GSPC --period 1m  # S&P 500
python main.py --symbol ^DJI --period 1m   # 道瓊工業指數
python main.py --symbol ^IXIC --period 1m  # 納斯達克指數
```

參數說明：
- `--symbol`：股票代碼
  - 台股：需要加上.TW後綴（如：2330.TW）
  - 美股：直接使用代碼（如：AAPL）
  - 指數：使用^開頭（如：^TWII、^GSPC）
- `--period`：時間範圍（可選：1w、1m、3m、6m、1y、3y）

### 批量處理多個股票

1. 編輯 `config.json` 文件，添加需要分析的股票代碼：
```json
{
    "stocks": [
        "^TWII",    // 台股指數
        "2330.TW",  // 台積電
        "AAPL",     // 蘋果公司
        "GOOGL",    // Google
        "MSFT",     // 微軟
        "^GSPC"     // S&P 500指數
    ],
    "default_period": "1m",
    "periods": ["1w", "1m", "3m", "6m", "1y", "3y"],
    "output_formats": ["csv", "json", "chart"]
}
```

2. 運行批量處理命令：
```bash
python main.py --all
```

## 輸出文件

### CSV文件
- 位置：`data/csv/{股票代碼}_data_{時間範圍}.csv`
- 包含欄位：
  - Date：日期
  - Close：收盤價
  - Volume：成交量（百萬股）
  - Change：漲跌幅（%）
  - Points：漲跌點數

### JSON文件
- 位置：`data/json/{股票代碼}_data_{時間範圍}.json`
- 包含與CSV文件相同的數據欄位

### 圖表文件
- 位置：`data/charts/{股票代碼}_chart_{時間範圍}.png`
- 圖表內容：
  - 上方：股價走勢圖（含收盤價）
  - 下方：成交量圖
- 特點：
  - 自動調整日期標籤密度
  - 高解析度輸出（300 DPI）
  - 清晰的圖例說明

### 日誌文件
- 位置：`logs/stock_{日期}.log`
- 記錄內容：
  - 數據獲取過程
  - 交易日和非交易日統計
  - 文件保存位置
  - 錯誤信息（如果有）

## 注意事項

1. 需要穩定的網絡連接以獲取數據
2. 台股在週末和國定假日不交易
3. 美股在週末和美國假日不交易
4. 數據來源為Yahoo Finance，可能有15分鐘延遲
5. 美股和台股的交易時間不同，請注意時差影響

## 未來計劃

- [ ] 添加技術指標（如MA、KD、MACD、RSI等）
- [ ] 支持更多數據來源
- [ ] 添加自動更新功能
- [ ] 添加回測功能
- [ ] 添加美股和台股的對比分析功能

## 數據來源

數據來源：Yahoo Finance
# stock_market
