import akshare as ak
import pandas as pd
from datetime import datetime
import os

def fetch_and_save():
    print("开始抓取 A 股实时行情...")
    try:
        df = ak.stock_zh_a_spot_em()
        if df is None or df.empty:
            print("未能获取到数据")
            return

        os.makedirs("data", exist_ok=True)
        # 建议使用固定名称 latest.csv，方便 Hugo 读取；
        # 或者保留日期名称以便留存历史。
        today = datetime.now().strftime("%Y%m%d")
        file_path = f"data/A_stock_{today}.csv"
        
        df.to_csv(file_path, index=False, encoding="utf-8-sig")
        print(f"✅ 数据保存成功: {file_path}")
        
    except Exception as e:
        print(f"❌ 抓取失败: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_and_save()
