import logging
import os
from datetime import datetime

# 設定 logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 設定控制台處理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(console_formatter)

# 設定文件處理器
log_filename = f'logs/stock_{datetime.now().strftime("%Y%m%d")}.log'
os.makedirs('logs', exist_ok=True)
file_handler = logging.FileHandler(log_filename, encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(file_formatter)

# 添加處理器到 logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
