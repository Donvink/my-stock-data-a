import akshare as ak
import pandas as pd
from datetime import datetime
import os
import time

def fetch_with_retry(max_retries=5):
    """带重试机制的抓取逻辑"""
    for i in range(max_retries):
        try:
            print(f"尝试第 {i+1} 次抓取...")
            # 核心接口
            df = ak.stock_zh_a_spot_em()
            
            if df is not None and not df.empty:
                print("✅ 数据抓取成功！")
                return df
        except Exception as e:
            print(f"⚠️ 第 {i+1} 次抓取异常: {e}")
            time.sleep(5) # 等 5 秒再试
            
    print("❌ 所有重试均失败。")
    return None

def fetch_and_save():
    df = fetch_with_retry()
    
    if df is not None:
        os.makedirs("data", exist_ok=True)
        today = datetime.now().strftime("%Y%m%d")
        file_path = f"data/A_stock_{today}.csv"
        df.to_csv(file_path, index=False, encoding="utf-8-sig")
        print(f"💾 数据已存至: {file_path}")
    else:
        # 如果重试 5 次依然失败，强制脚本报错，让 GitHub Actions 显示红叉
        exit(1)

if __name__ == "__main__":
    fetch_and_save()
