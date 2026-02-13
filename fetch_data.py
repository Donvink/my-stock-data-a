import tushare as ts
import pandas as pd
import os
from datetime import datetime

# 初始化 Tushare (请确保已在 GitHub Secrets 设置 TUSH_TOKEN)
token = os.getenv("TUSH_TOKEN")
pro = ts.pro_api(token)

def get_market_analysis():
    # 1. 获取最新交易日 (Tushare 格式为 YYYYMMDD)
    # 如果是周末运行，会自动取最近一个交易日
    today = datetime.now().strftime('%Y%m%d')
    
    print(f"📊 开始分析 {today} 行情数据...")

    # --- A. 整体行情与指数 ---
    # 获取上证指数 (000001.SH)
    df_index = pro.index_daily(ts_code='000001.SH', start_date=today, end_date=today)
    if df_index.empty:
        # 如果还没收盘或当天非交易日，尝试获取上一交易日
        trade_cal = pro.trade_cal(exchange='', is_open='1', end_date=today, limit=1)
        today = trade_cal.iloc[0]['cal_date']
        df_index = pro.index_daily(ts_code='000001.SH', start_date=today, end_date=today)

    sz_index = df_index.iloc[0]['close']
    sz_chg = df_index.iloc[0]['pct_chg']

    # --- B. 涨跌家数与总成交额 ---
    df_daily = pro.daily(trade_date=today)
    total_amount = df_daily['amount'].sum() / 100000  # 单位：亿元
    
    up_count = len(df_daily[df_daily['pct_chg'] > 0])
    down_count = len(df_daily[df_daily['pct_chg'] < 0])
    flat_count = len(df_daily[df_daily['pct_chg'] == 0])

    # --- C. 涨停与跌停 (剔除ST) ---
    # 获取涨跌停列表 (limit_list_d 接口)
    df_limit = pro.limit_list_d(trade_date=today)
    # 获取基础信息用于剔除ST
    df_basic = pro.stock_basic(exchange='', list_status='L', fields='ts_code,name,industry')
    
    # 合并并剔除名称中含 ST 的股
    df_limit_merged = pd.merge(df_limit, df_basic, on='ts_code')
    df_limit_clean = df_limit_merged[~df_limit_merged['name'].str.contains('ST')]
    
    limit_up_count = len(df_limit_clean[df_limit_clean['limit'] == 'U'])
    limit_down_count = len(df_limit_clean[df_limit_clean['limit'] == 'D'])

    # --- D. 成交额前十个股 ---
    # 按照成交额排序并取前十
    top_10 = df_daily.sort_values(by='amount', ascending=False).head(10)
    # 合并基础信息（获取板块名称）
    top_10_report = pd.merge(top_10, df_basic, on='ts_code')
    
    # 格式化输出
    print(f"\n======= {today} A股市场分析报告 =======")
    print(f"📈 上证指数: {sz_index} ({sz_chg}%)")
    print(f"💰 全市场总成交额: {total_amount:.2f} 亿元")
    print(f"⚖️ 涨/跌/平家数: {up_count} / {down_count} / {flat_count}")
    print(f"🚫 涨停/跌停(非ST): {limit_up_count} / {limit_down_count}")
    print("\n🔝 成交额前十个股详情:")
    
    result_list = []
    for _, row in top_10_report.iterrows():
        item = {
            "名称": row['name'],
            "成交额(亿)": round(row['amount'] / 100000, 2),
            "涨幅": f"{row['pct_chg']}%",
            "所属板块": row['industry']
        }
        result_list.append(item)
        print(f"- {row['name']} | 成交额: {item['成交额(亿)']}亿 | 涨幅: {item['涨幅']} | 板块: {item['所属板块']}")
    
    return {
        "date": today,
        "summary": {
            "index": sz_index,
            "total_amount": total_amount,
            "up_down": (up_count, down_count),
            "limits": (limit_up_count, limit_down_count)
        },
        "top_10": result_list
    }

if __name__ == "__main__":
    get_market_analysis()