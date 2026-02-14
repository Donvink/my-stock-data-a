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
            time.sleep(0.5) # 避免请求过快被封
            dt_pool_df = ak.stock_zt_pool_dtgc_em(date=date)
            time.sleep(0.5) # 避免请求过快被封
            zb_pool_df = ak.stock_zt_pool_zbgc_em(date=date)
            time.sleep(0.5) # 避免请求过快被封
            
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
                if i % 2 == 0:
                    # 首选：东方财富实时接口（数据最全，含代码、名称、涨跌幅、成交额等）
                    df = ak.stock_zh_a_spot_em()
                elif i % 2 == 1:
                    # 备选 1：新浪接口（在云服务器上极其稳定，虽数据字段略少，但基本行情都有）
                    print("⚠️ 尝试使用新浪稳健接口...")
                    df = ak.stock_zh_a_spot()
                
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
                time.sleep(0.5) # 避免请求过快被封
            print("⚠️ 回溯多天后仍未找到可用数据，无法确定最新日期。")
            return None
    except Exception as e:
        print(f"⚠️ 获取最新日期失败: {e}")
        return None

def get_stocks_info(df):
    """获取个股所属板块/概念信息"""
    industry_frequency = {} # 统计行业出现频次的字典
    # 确保 DataFrame 包含必要的列，如果缺失则添加空列
    for col in ['板块代码', '板块名称', '主营业务', '板块次数']:
        if col not in df.columns:
            df[col] = None
    for index, row in df.iterrows():
        code = row['代码']
        code = code[-6:] if len(code) > 6 else code # 确保代码是6位
        # 判断是否是科创板（688开头）或创业板（300开头），如果是则加上前缀
        if code.startswith('688'):
            code = 'SH' + code
        elif code.startswith('300'):
            code = 'SZ' + code
        else:
            code = 'SH' + code if code.startswith('6') else 'SZ' + code
        try:
            # info_df = ak.stock_individual_info_em(symbol=code)    # 东方财富
            info_df = ak.stock_individual_basic_info_xq(symbol=code) # 雪球
            # print(info_df)
            info_dict = info_df.set_index('item')['value'].to_dict()
            ind_code = info_dict.get('affiliate_industry').get('ind_code')
            ind_name = info_dict.get('affiliate_industry').get('ind_name')
            df.at[index, '板块代码'] = ind_code
            df.at[index, '板块名称'] = ind_name
            df.at[index, '主营业务'] = info_dict.get('main_operation_business')
            
            # 统计行业出现频次的字典，优先获取出现频次较高的板块信息
            if ind_code is not None:
                industry_frequency[ind_code] = industry_frequency.get(ind_code, 0) + 1
                df.at[index, '板块次数'] = industry_frequency[ind_code]
            time.sleep(0.5) # 避免请求过快被封
        except Exception as e:
            print(f"⚠️ 获取 {code} 板块信息失败: {e}")
    return True

def get_top_amount_stocks(df, top_n=20, date="20260213", save_dir='data'):
    """获取成交额前 N 的个股信息"""
    file_path = f"{save_dir}/top_amount_stocks_{date}.csv"
    top_stocks_df = load_local_csv(file_path)
    if top_stocks_df is None:
        try:
            top_stocks_df = df.sort_values(by='成交额', ascending=False).head(top_n).copy()

            top_stocks_df.reset_index(drop=True, inplace=True)
            top_stocks_df['成交额(亿元)'] = (top_stocks_df['成交额'] / 1e8).round(2)
            # top_stocks_df['竞价涨幅(%)'] = ((top_stocks_df['今开'] - top_stocks_df['昨收']) / top_stocks_df['昨收'] * 100).round(2)
            # top_stocks_df['实体涨幅(%)'] = ((top_stocks_df['最新价'] - top_stocks_df['今开']) / top_stocks_df['今开'] * 100).round(2)

            top_stocks_df = top_stocks_df[['代码', '名称', '最新价', '涨跌幅', '成交额(亿元)']]

            get_stocks_info(top_stocks_df)
        except Exception as e:
            print(f"⚠️ 获取成交额前 N 的个股信息失败: {e}")
            return None
    
    print("-" * 30)
    print(f"📈 成交量前 {top_n} 个股信息:")
    print(top_stocks_df)
    print('-' * 30)

    # 保存到文件
    top_stocks_df.to_csv(file_path, index=False, encoding="utf-8-sig")

    return top_stocks_df

def get_industry_summary(date="20260213", save_dir='data'):
    """获取行业板块信息"""
    file_path = f"{save_dir}/industry_summary_{date}.csv"

    # 1. 各大指数摘要数据
    industry_summary_df = load_local_csv(file_path)
    if industry_summary_df is None:
        try:
            industry_summary_df = ak.stock_board_industry_summary_ths()
            # print(industry_summary_df)
        except Exception as e:
            print(f"⚠️ 获取行业板块数据失败: {e}")
            return None

    # 取top 5 行业板块数据
    industry_summary_df = industry_summary_df.head(5).copy()

    industry_summary_df.to_csv(file_path, index=False, encoding="utf-8-sig")
    
    print("-" * 30)
    # print(industry_summary_df[['代码', '名称', '最新价', '涨跌幅', '成交额(亿元)']])
    # industry_summary_df = industry_summary_df[['板块名称', '板块代码', '涨跌幅', '上涨家数', '下跌家数', '领涨股票', '领涨股票-涨跌幅']]
    print(industry_summary_df)
    print("-" * 30)
    return industry_summary_df

def get_concept_summary(date="20260213", save_dir='data'):
    """获取概念板块信息"""
    file_path = f"{save_dir}/concept_summary_{date}.csv"

    concept_summary_df = load_local_csv(file_path)
    if concept_summary_df is None:
        try:
            concept_summary_df = ak.stock_board_concept_name_em()
            # print(concept_summary_df)
        except Exception as e:
            print(f"⚠️ 获取概念板块数据失败: {e}")
            return None

    # 取top 5 板块数据
    concept_summary_df = concept_summary_df.head(5).copy()

    concept_summary_df.to_csv(file_path, index=False, encoding="utf-8-sig")
    
    print("-" * 30)
    # print(industry_summary_df[['代码', '名称', '最新价', '涨跌幅', '成交额(亿元)']])
    print(concept_summary_df)
    print("-" * 30)
    return concept_summary_df

def get_concept_cons(df, date="20260213", save_dir='data', top_n=10):
    """获取概念板块成分股信息"""
    all_concept_cons = [] # 用于存储所有概念板块成分股数据

    num_concepts = df.shape[0]
    for i in range(num_concepts):
        file_path = f"{save_dir}/concept_cons_{i}_{date}.csv"
        concept_cons_df = load_local_csv(file_path)
        if concept_cons_df is not None:
            all_concept_cons.append(concept_cons_df)

    if len(all_concept_cons) < num_concepts:
        all_concept_cons = []
        try:
            for index, row in df.iterrows():
                concept_cons_df = ak.stock_board_concept_cons_em(symbol=row['板块名称'])
                # 取前top_n个成分股数据
                concept_cons_df = concept_cons_df.head(top_n).copy()
                concept_cons_df['所属板块'] = row['板块名称']
                all_concept_cons.append(concept_cons_df)
                # print(concept_cons_df)
                concept_cons_df.to_csv(file_path, index=False, encoding="utf-8-sig")
                time.sleep(0.5) # 避免请求过快被封
        except Exception as e:
            print(f"⚠️ 获取概念板块成分股数据失败: {e}")
            return None
    
    print("-" * 30)
    all_concept_cons_df = pd.concat(all_concept_cons, ignore_index=True)
    print(all_concept_cons_df)
    print("-" * 30)
    return all_concept_cons

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
    # TODO: 连板数据分析

    # 获取所有股票数据并保存
    all_stocks_df, up_count, down_count, flat_count = fetch_all_stock_data(date=latest_date, save_dir=save_dir, max_retries=3)

    # 成交量前二十的个股名称、成交额、涨幅、以及所属板块或者概念
    top_amount_stocks = get_top_amount_stocks(all_stocks_df, top_n=20, date=latest_date, save_dir=save_dir)
    # TODO: 以及板块详细数据

    # 涨幅前五板块中涨停个股、连板高度（几天几板、首板后涨幅）
    # # 同花顺-同花顺行业一览表
    # industry_summary_df = get_industry_summary(date=latest_date, save_dir=save_dir)
    
    # 东方财富-概念板块 实时行情数据
    concept_summary_df = get_concept_summary(date=latest_date, save_dir=save_dir)

    # 概念板块成分股数据
    concept_cons_df = get_concept_cons(concept_summary_df, date=latest_date, save_dir=save_dir)

    # 龙虎榜

    # 获取资讯

    # 分析报告

    return True
    

if __name__ == "__main__":
    fetch_and_save()
                                                                                                                    