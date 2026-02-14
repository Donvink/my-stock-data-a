import akshare as ak
import time



# 个股信息查询-东方财富
# info_df = ak.stock_individual_info_em(symbol='300017')
# print(info_df)
# stock_individual_basic_info_xq_df = ak.stock_individual_basic_info_xq(symbol="SZ002837")
# print(stock_individual_basic_info_xq_df)


# 个股行情报价 - 东方财富
# stock_bid_ask_em_df = ak.stock_bid_ask_em(symbol="000001")
# print(stock_bid_ask_em_df)

# 股票指数实时行情数据-东财
# index_df = ak.stock_zh_index_spot_em()
# print(index_df)

# # shenzhen stock summary: 证券类别统计
# stock_szse_summary_df = ak.stock_szse_summary(date="20260213")
# print(stock_szse_summary_df)
# print("-----------------------------")
# print("-----------------------------")

# # 上海证券交易所-每日概况
# stock_sse_deal_daily_df = ak.stock_sse_deal_daily(date="20260213")
# print(stock_sse_deal_daily_df)
# print("-----------------------------")
# print("-----------------------------")

# 个股信息查询-雪球
# stock_individual_basic_info_xq_df = ak.stock_individual_basic_info_xq(symbol="SH601127")
# print(stock_individual_basic_info_xq_df)
# print("-----------------------------")
# print("-----------------------------")


# # 实时行情数据-新浪
# stock_zh_a_spot_df = ak.stock_zh_a_spot()
# print(stock_zh_a_spot_df)
# print("-----------------------------")
# print("-----------------------------")


# 个股实时行情数据-雪球
# stock_individual_spot_xq_df = ak.stock_individual_spot_xq(symbol="SH600000")
# print(stock_individual_spot_xq_df)
# print("-----------------------------")
# print("-----------------------------")


# # 个股历史行情数据-新浪
# stock_zh_a_daily_qfq_df = ak.stock_zh_a_daily(symbol="sz000001", start_date="20260113", end_date="20260213", adjust="qfq")
# print(stock_zh_a_daily_qfq_df)
# print("-----------------------------")
# print("-----------------------------")


# # 分时数据-新浪
# stock_zh_a_minute_df = ak.stock_zh_a_minute(symbol='sh600751', period='1', adjust="qfq")
# print(stock_zh_a_minute_df)


# # 科创板实时行情数据-新浪
# stock_zh_kcb_spot_df = ak.stock_zh_kcb_spot()
# print(stock_zh_kcb_spot_df)
# # 历史行情数据
# stock_zh_kcb_daily_df = ak.stock_zh_kcb_daily(symbol="sh688399", adjust="hfq")
# print(stock_zh_kcb_daily_df)


# # 主营介绍-同花顺
# stock_zyjs_ths_df = ak.stock_zyjs_ths(symbol="688981")
# print(stock_zyjs_ths_df)


# # 资金流向：同花顺
# # 个股资金流：symbol="即时"; choice of {“即时”, "3日排行", "5日排行", "10日排行", "20日排行"}
# print("-----------个股资金流------------------")
# stock_fund_flow_individual_df = ak.stock_fund_flow_individual(symbol="即时")
# print(stock_fund_flow_individual_df)
# time.sleep(3)
# print("-----------------------------")
# print("------------概念资金流-----------------")
# stock_fund_flow_concept_df = ak.stock_fund_flow_concept(symbol="即时")
# print(stock_fund_flow_concept_df)
# time.sleep(3)
# print("-----------------------------")
# print("------------大单追踪-----------------")
# stock_fund_flow_big_deal_df = ak.stock_fund_flow_big_deal()
# print(stock_fund_flow_big_deal_df)
# time.sleep(3)
# print("-----------------------------")


# # 板块行情-新浪；
# # indicator="新浪行业"; choice of {"新浪行业", "启明星行业", "概念", "地域", "行业"}
# stock_industry_sina_df = ak.stock_sector_spot(indicator="行业")
# print(stock_industry_sina_df)
# print("-----------------------------")

# # 板块详情-新浪
# # sector="hangye_ZL01"; 通过 ak.stock_sector_spot 返回数据的 label 字段选择 sector
# stock_sector_detail_df = ak.stock_sector_detail(sector="hangye_ZL01")
# print(stock_sector_detail_df)

# # 基金持股-新浪
# stock_fund_stock_holder_df = ak.stock_fund_stock_holder(symbol="601318")
# print(stock_fund_stock_holder_df)

# # 机构持股详情-新浪
# # quarter="20201"; 从 2005 年开始, {"一季报":1, "中报":2 "三季报":3 "年报":4}, e.g., "20191", 其中的 1 表示一季报; "20193", 其中的 3 表示三季报;
# stock_institute_hold_detail_df = ak.stock_institute_hold_detail(stock="300003", quarter="20201")
# print(stock_institute_hold_detail_df)


# # 涨跌投票-百度股市通
# stock_zh_vote_baidu_df = ak.stock_zh_vote_baidu(symbol="000001", indicator="指数") # 或"股票"
# print(stock_zh_vote_baidu_df)


# 龙虎榜-每日详情-新浪
# stock_lhb_detail_daily_sina_df = ak.stock_lhb_detail_daily_sina(date="20260213")
# print(stock_lhb_detail_daily_sina_df)


# # 龙虎榜-个股上榜统计-新浪
# # symbol="5"; choice of {"5": 最近 5 天; "10": 最近 10 天; "30": 最近 30 天; "60": 最近 60 天;}
# stock_lhb_ggtj_sina_df = ak.stock_lhb_ggtj_sina(symbol="5")
# print(stock_lhb_ggtj_sina_df)


# # 同花顺-同花顺行业一览表
# stock_board_industry_summary_ths_df = ak.stock_board_industry_summary_ths()
# print(stock_board_industry_summary_ths_df)


# # 股票热度
# # 1. 股票热度-雪球
# # 1.1 关注排行榜
# stock_hot_follow_xq_df = ak.stock_hot_follow_xq(symbol="本周新增")
# print(stock_hot_follow_xq_df)
# print("-----------------------------")

# # 1.2 讨论排行榜
# stock_hot_tweet_xq_df = ak.stock_hot_tweet_xq(symbol="本周新增")
# print(stock_hot_tweet_xq_df)
# print("-----------------------------")

# # 1.3 交易排行榜
# stock_hot_deal_xq_df = ak.stock_hot_deal_xq(symbol="本周新增")
# print(stock_hot_deal_xq_df)
# print("-----------------------------")



# # # 2. 股票热度-东财
# # # 2.1 人气榜
# stock_hot_rank_em_df = ak.stock_hot_rank_em()
# print(stock_hot_rank_em_df)

# # 2.2 飙升榜-A股
# stock_hot_up_em_df = ak.stock_hot_up_em()
# print(stock_hot_up_em_df)

# # 2.3 个股人气榜-实时变动
# stock_hot_rank_detail_realtime_em_df = ak.stock_hot_rank_detail_realtime_em(symbol="SZ000665")
# print(stock_hot_rank_detail_realtime_em_df)

# # 2.4 热门关键词
# stock_hot_keyword_em_df = ak.stock_hot_keyword_em(symbol="SZ000665")
# print(stock_hot_keyword_em_df)


# 涨停板行情
# # 涨停股池 - 东方财富
# stock_zt_pool_em_df = ak.stock_zt_pool_em(date='20260213')
# print(stock_zt_pool_em_df)

# # 昨日涨停股池
# stock_zt_pool_previous_em_df = ak.stock_zt_pool_previous_em(date='20260213')
# print(stock_zt_pool_previous_em_df)

# # 强势股池
# stock_zt_pool_strong_em_df = ak.stock_zt_pool_strong_em(date='20260213')
# print(stock_zt_pool_strong_em_df)

# # 炸板股池
# stock_zt_pool_zbgc_em_df = ak.stock_zt_pool_zbgc_em(date='20260213')
# print(stock_zt_pool_zbgc_em_df)

# # 跌停股池
# stock_zt_pool_dtgc_em_df = ak.stock_zt_pool_dtgc_em(date='20260213')
# print(stock_zt_pool_dtgc_em_df)

# 赚钱效应分析
# 描述: 乐咕乐股网-赚钱效应分析数据
# 限量: 单次返回当前赚钱效应分析数据
# 说明：
# 涨跌比：即沪深两市上涨个股所占比例，体现的是市场整体涨跌，占比越大则代表大部分个股表现活跃。
# 涨停板数与跌停板数的意义：涨停家数在一定程度上反映了市场的投机氛围。当涨停家数越多，则市场的多头氛围越强。真实涨停是非一字无量涨停。真实跌停是非一字无量跌停。
# stock_market_activity_legu_df = ak.stock_market_activity_legu()
# print(stock_market_activity_legu_df)

# 东方财富-概念板块 实时行情数据
# stock_board_concept_name_em_df = ak.stock_board_concept_name_em()
# print(stock_board_concept_name_em_df)

# 东方财富-概念板块 成分股数据
# stock_board_concept_cons_em_df = ak.stock_board_concept_cons_em(symbol="Kimi概念")
# print(stock_board_concept_cons_em_df)


# 资讯
# # 全球财经快讯 - 东方财富
# stock_info_global_em_df = ak.stock_info_global_em()
# print(stock_info_global_em_df)

# # 全球财经快讯-新浪财经
# stock_info_global_sina_df = ak.stock_info_global_sina()
# print(stock_info_global_sina_df)

# # 快讯-富途牛牛
# stock_info_global_futu_df = ak.stock_info_global_futu()
# print(stock_info_global_futu_df)

# # 全球财经直播-同花顺财经
# stock_info_global_ths_df = ak.stock_info_global_ths()
# print(stock_info_global_ths_df)

# # 电报-财联社
# stock_info_global_cls_df = ak.stock_info_global_cls(symbol="全部")
# print(stock_info_global_cls_df)


# 技术指标 https://akshare.akfamily.xyz/data/stock/stock.html#id423
# 数据接口一览 https://akshare.akfamily.xyz/tutorial.html


