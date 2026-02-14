import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import os
import time


def load_local_csv(file_path=""):
    """从本地 CSV 文件加载数据"""
    if os.path.exists(file_path):
        # print(f"📂 发现本地缓存，正在读取: {file_path}")
        df = pd.read_csv(file_path, dtype={'代码': str}) # 强制代码列为字符串，防止 000001 变成 1
        return df
    else:
        # print(f"⚠️ 本地文件不存在: {file_path}")
        return None

def stock_summary(date="20260213", save_dir='data'):
    """获取大盘数据"""
    file_path = f"{save_dir}/index_{date}.csv"

    # 1. 各大指数摘要数据
    index_df = load_local_csv(file_path)
    if index_df is None:
        try:
            # index_df = ak.stock_zh_index_spot_em()
            index_df = ak.stock_zh_index_spot_sina()
            # print(index_df)
        except Exception as e:
            print(f"⚠️ 获取指数数据失败: {e}")
            return None

    target_indices = ["sh000001", "sz399001"]

    # 2. 筛选出两只指数
    result = index_df[index_df['代码'].isin(target_indices)].copy()

    # 3. 数据清理：将字符串转为数值
    result['成交额'] = pd.to_numeric(result['成交额'])
    result['涨跌幅'] = pd.to_numeric(result['涨跌幅'])

    # 4. 计算汇总成交额
    total_amount = result['成交额'].sum()

    # 5. 构造“汇总”行数据
    summary_row = {
        '代码': 'Total',
        '名称': '沪深总成交额',
        '最新价': None,  # 汇总行不需要最新价
        '成交额': total_amount,
        '涨跌幅': None  # 两个指数的涨幅不能直接相加，所以填 None 或保持为空
    }

    # 6. 将汇总行追加到 DataFrame 中
    # 使用 pd.DataFrame 转换一下再连接
    result = pd.concat([result, pd.DataFrame([summary_row])], ignore_index=True)

    # 7. 格式化输出：将成交额转为“亿元”更直观
    result['成交额(亿元)'] = (result['成交额'] / 1e8).round(2)
    result.to_csv(file_path, index=False, encoding="utf-8-sig")
    
    print("-" * 30)
    print(result[['代码', '名称', '最新价', '涨跌幅', '成交额(亿元)']])
    print("-" * 30)
    return total_amount

def stock_zt_dt_pool(date="20260213", save_dir='data'):
    """获取涨停/跌停个股数据"""
    zt_file_path = f"{save_dir}/zt_pool_{date}.csv"
    dt_file_path = f"{save_dir}/dt_pool_{date}.csv"
    zb_file_path = f"{save_dir}/zb_pool_{date}.csv"

    # 1. 各大指数摘要数据
    zt_pool_df = load_local_csv(zt_file_path)
    dt_pool_df = load_local_csv(dt_file_path)
    zb_pool_df = load_local_csv(zb_file_path)
    if zt_pool_df is None or dt_pool_df is None or zb_pool_df is None:
        try:
            zt_pool_df = ak.stock_zt_pool_em(date=date)
            dt_pool_df = ak.stock_zt_pool_dtgc_em(date=date)
            zb_pool_df = ak.stock_zt_pool_zbgc_em(date=date)
            
            zt_pool_df.to_csv(zt_file_path, index=False, encoding="utf-8-sig")
            # print(f"✅ 成功获取涨停板数据，保存至: {zt_file_path}")
            dt_pool_df.to_csv(dt_file_path, index=False, encoding="utf-8-sig")
            # print(f"✅ 成功获取跌停板数据，保存至: {dt_file_path}")
            zb_pool_df.to_csv(zb_file_path, index=False, encoding="utf-8-sig")
            # print(f"✅ 成功获取炸板数据，保存至: {zb_file_path}")
        except Exception as e:
            print(f"⚠️ 获取涨停板数据失败: {e}")
            return None, None, None
            
    zt_stocks = len(zt_pool_df)
    dt_stocks = len(dt_pool_df)
    zb_stocks = len(zb_pool_df)

    print("-" * 30)
    print(f"📊 {date} 涨停股数量: {zt_stocks}，跌停股数量: {dt_stocks}，炸板股数量: {zb_stocks}")
    print("-" * 30)
    
    return zt_stocks, dt_stocks, zb_stocks

def fetch_all_stock_data(date='20260213', save_dir='data', max_retries=3):
    """尝试抓取所有股票数据，失败则重试"""
    file_path = f"{save_dir}/A_stock_{date}.csv"

    df = load_local_csv(file_path)
    if df is None:
        sucess = False
        for i in range(max_retries):
            try:
                print(f"尝试第 {i+1} 次抓取...")
                # 核心接口
                df = ak.stock_zh_a_spot_em()
                # df = ak.stock_zh_a_spot()
                # df = ak.stock_zh_a_hist_ths()
                
                if df is not None and not df.empty:
                    df.to_csv(file_path, index=False, encoding="utf-8-sig")
                    print("✅ 数据抓取成功！")
                    print(f"💾 数据已存至: {file_path}")
                    sucess = True
                    break
            except Exception as e:
                print(f"⚠️ 第 {i+1} 次抓取异常: {e}")
                time.sleep(5) # 等 5 秒再试
        if not sucess:
            print("❌ 所有重试均失败。")
            # exit(1)
            return None, None, None, None
    
    # 计算涨跌个数
    df['涨跌'] = df['涨跌幅'].apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
    up_count = df[df['涨跌'] == 1].shape[0]
    down_count = df[df['涨跌'] == -1].shape[0]
    flat_count = df[df['涨跌'] == 0].shape[0]

    print("-" * 30)
    print(f"📈 上涨股数: {up_count}, 📉 下跌股数: {down_count}, 📊 持平股数: {flat_count}")
    print("-" * 30)

    return df, up_count, down_count, flat_count

def get_latest_date(max_try=20):
    """获取最新可用数据的日期"""
    today = datetime.now().strftime("%Y%m%d")
    try:
        zt_pool_df = ak.stock_zt_pool_em(date=today)
        if not zt_pool_df.empty:
            print(f"✅ 最新可用数据日期: {today}")
            return today
        else:
            for i in range(1, max_try + 1):
                check_date = (datetime.now() - timedelta(days=i)).strftime("%Y%m%d")
                zt_pool_df = ak.stock_zt_pool_em(date=check_date)
                if not zt_pool_df.empty:
                    print(f"✅ 最新可用数据日期: {check_date} (通过回溯 {i} 天找到)")
                    return check_date
            print("⚠️ 回溯多天后仍未找到可用数据，无法确定最新日期。")
            return None
    except Exception as e:
        print(f"⚠️ 获取最新日期失败: {e}")
        return None

def fetch_and_save():
    """主函数：获取数据并保存"""
    # latest_date = get_latest_date()
    latest_date = datetime.now().strftime("%Y%m%d")
    if latest_date is None:
        print("❌ 无法确定最新数据日期，脚本终止。")
        exit(1)
    os.makedirs("data", exist_ok=True)
    save_dir = f"data/{latest_date}"
    os.makedirs(save_dir, exist_ok=True)

    # 获取大盘数据并保存
    total_amount = stock_summary(date=latest_date, save_dir=save_dir)

    # 获取涨停数据并保存
    zt_stocks, dt_stocks, zb_stocks = stock_zt_dt_pool(date=latest_date, save_dir=save_dir)

    # 获取所有股票数据并保存
    df, up_count, down_count, flat_count = fetch_all_stock_data(date=latest_date, save_dir=save_dir, max_retries=3)

    # 成交量前十的个股名称、成交额、涨幅、以及所属板块或者概念


    # 涨幅前五板块以及板块中涨停个股、连板高度（几天几板、首板后涨幅）

    
    # 涨停池
    

    # 龙虎榜

    return True
    

if __name__ == "__main__":
    fetch_and_save()
                                                                                                                    