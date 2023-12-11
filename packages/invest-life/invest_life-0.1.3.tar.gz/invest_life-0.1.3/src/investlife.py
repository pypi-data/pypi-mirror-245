# -*- coding: utf-8 -*-

import requests, json
import pickle

# url
base_url = 'https://investlife.cn/data/'

# token
g_token = None

# 设置token
def set_token(token = None):
    global g_token
    g_token = token

# 设置headers
def get_headers():
    return {'Content-Type': 'application/json', 'token': g_token, 'appsource': 'python'}

def get_stock_list(listed_state = None, fields = None):
    """
    记录A股上市、退市股票交易代码、股票名称、上市状态等信息；

    输入参数：
    :param str listed_state : 上市状态
    :param str fields : 字段集合

    输出参数：
    :param str secu_abbr : 证券简称,
    :param str chi_name : 中文名称,
    :param str listed_state : 上市状态,
    :param str secu_code : 证券代码,
    :param str secu_market : 证券市场,
    :param str listed_sector : 上市板块,
    :param str hs_code : HS代码,

    结果输出:
         secu_abbr chi_name  listed_state \
0 平安银行 平安银行股份有限公司 上市
1 万科Ａ 万科企业股份有限公司 上市
…
    """
        
    headers = get_headers()
    url = base_url + 'get_stock_list'
    param = {'listed_state': listed_state, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    raise Exception(res.text)

def get_trading_calendar(secu_market = None, if_trading_day = None, if_week_end = None, if_month_end = None, start_date = None, end_date = None, fields = None):
    """
    交易日信息，包括每个日期是否是交易日，是否周、月最后一个交易日；最大可返回1年的交易日信息；

    输入参数：
    :param str secu_market : 证券市场，默认"83"
    :param str if_trading_day : 是否交易日
    :param str if_week_end : 是否周末
    :param str if_month_end : 是否月末
    :param str start_date : 开始日期，默认"last_year_today"
    :param str end_date : 截止日期，默认"now"
    :param str fields : 字段集合

    输出参数：
    :param str if_trading_day : 是否交易日,
    :param str if_week_end : 是否周末,
    :param str if_month_end : 是否月末,
    :param str secu_market : 证券市场,
    :param str trading_date : 日期,

    结果输出:
         if_trading_day if_week_end  if_month_end \
0 是 否 否
1 是 否 否
...
    """

    headers = get_headers()
    url = base_url + 'get_trading_calendar'

    param = {'secu_market': secu_market, 'if_trading_day': if_trading_day, 'if_week_end': if_week_end, 'if_month_end': if_month_end, 'start_date': start_date, 'end_date': end_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    raise Exception(res.text)

def get_ipo_list(start_date = None, secu_market = None, listed_sector = None, fields = None):
    """
    提供已上市新股代码，名称，发行数量、申购和配售等新股信息；

    输入参数：
    :param str start_date : 开始日期，默认"now"
    :param str secu_market : 上市市场
    :param str listed_sector : 上市板块
    :param str fields : 字段集合

    输出参数：
    :param str prod_name : 产品名称,
    :param str prod_code : 产品代码,
    :param str secu_code : 证券代码,
    :param str secu_market : 证券市场,
    :param str secu_abbr : 证券简称,
    :param str prospectus_date : 发行日期,
    :param str listed_date : 上市日期,
    :param float issue_price : 发行价(元),
    :param float diluted_pe_ratio : 发行市盈率(全面摊薄),
    :param float allot_max : 申购上限(股),
    :param int lot_rate_online : 发行中签率,
    :param float worth_value : 市值,
    :param float issue_vol : 发行数量(股),
    :param str indurstry : 所属行业,
    :param float naps : 每股净资产(元),
    :param int issue_amount : 发行数量,
    :param float lucky_rate : 配售中签率,
    :param float valid_apply_vol_online : 网上发行有效申购总量(股),
    :param int valid_apply_num_online : 网上发行有效申购户数(户),
    :param float valid_apply_vol_lp : 配售有效申购总量(股),
    :param int valid_apply_num_lp : 配售有效申购户数(户),
    :param float over_subs_times_online : 网上发行超额认购倍数(倍),
    :param float over_subs_times_lp : 配售超额认购倍数(倍),
    :param float listed_sector : 上市板块,
    :param float secu_category : 证券类型,
    :param str allocation_date : 中签号公布日,
    :param float esti_allot_max : 预估申购上限,
    :param float allot_min : 申购下限,
    :param float esti_issue_price : 预估发行价,
    :param float naps_after : 每股净资产(元),
    :param int issue_system_type : 发行制度类型,

    """

    headers = get_headers()
    url = base_url + 'get_ipo_list'

    param = {'start_date': start_date, 'secu_market': secu_market, 'listed_sector': listed_sector, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    raise Exception(res.text)

def get_company_profile(en_prod_code = None, fields = None):
    """
    获取公司的基本信息，包含公司名称、注册信息、公司属性、所在城市、联系电话、实际控制人等内容；

    输入参数：
    :param str en_prod_code : 股票代码，默认"600570.SH"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 股票代码,
    :param str chi_name : 公司中文名称,
    :param str eng_name : 公司英文名称,
    :param str company_pro : 公司属性,
    :param str establishment_date : 成立日期,
    :param str legal_repr : 法定代表人,
    :param str city_code : 城市,
    :param str reg_addr : 公司注册地址,
    :param str officeaddress : 公司办公地址,
    :param str officezip : 邮编,
    :param str tel : 联系电话,
    :param str email : 电子邮件,
    :param str website : 公司网址,
    :param str secu_affairs_repr : 公司披露人,
    :param str business_reg_number : 工商登记号,
    :param int regcapital : 注册资本,
    :param str state : 省份,
    :param str fax : 传真,
    :param str uniform_social_credit_code : 统一社会信用代码,
    :param int employee_sum : 员工总数,
    :param str controller_name : 实际控制人,

    """

    headers = get_headers()
    url = base_url + 'get_company_profile'

    param = {'en_prod_code': en_prod_code, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    raise Exception(res.text)

def get_stock_Info(en_prod_code = None, trading_date = None, fields = None):
    """
    获取股票的基本信息，包含股票交易代码、股票简称、上市时间、上市状态、所属概念板块等信息；

    输入参数：
    :param str en_prod_code : 内部编码，默认"600570.SH"
    :param str trading_date : 交易日期，默认"now"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 股票代码,
    :param str secu_abbr : 股票简称,
    :param str eng_name_abbr : 股票英文名称,
    :param str list_date : 上市时间,
    :param str secu_market : 上市地点,
    :param int par_value : 股票面值,
    :param str isin_code : ISIN代码,
    :param str hstock_code : 同公司H股代码,
    :param str hshare_abbr : 同公司H股简称,
    :param str bstock_code : 同公司B股代码,
    :param str bshare_abbr : 同公司B股简称,
    :param str secu_code : 证券编码,
    :param str listed_sector : 上市板块,
    :param str concept_board : 所属概念板块,
    :param str change_type : 证券存续状态,
    :param int sh_hk_flag : 是否沪港通标的,
    :param int sz_hk_flag : 是否深港通标的,
    :param str en_prod_code : 股票代码,

    """

    headers = get_headers()
    url = base_url + 'get_stock_Info'

    param = {'en_prod_code': en_prod_code, 'trading_date': trading_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    raise Exception(res.text)

def get_leader_profile(secu_code = None, position_type = None, fields = None):
    """
    高管基本信息，高管领导人简介、姓名、学历、职位、年度报酬等（包括科创板）；

    输入参数：
    :param str secu_code : 证券代码，默认"600570"
    :param str position_type : 职位类型，默认"1"
    :param str fields : 字段集合

    输出参数：
    :param str secu_code : 股票代码,
    :param str secu_abbr : 股票简称,
    :param str secu_market : 证券市场,
    :param str position_type : 职位类型,
    :param str leader_name : 领导人姓名,
    :param int position : 职位,
    :param str begin_date : 任职起始日,
    :param str birthday : 出生年月,
    :param str leader_degree : 学历程度,
    :param str newest_hold : 最新持股数,
    :param str shareholding_ratio : 持股比例,
    :param str end_date : 年度报酬报告期,
    :param int annual_reward : 年度报酬,

    """

    headers = get_headers()
    url = base_url + 'get_leader_profile'

    param = {'secu_code': secu_code, 'position_type': position_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    raise Exception(res.text)

def get_st_stock_list(secu_market = None, secu_category = None, listed_sector = None, fields = None):
    """
    当前ST及*ST的股票代码列表

    输入参数：
    :param str secu_market : 证券市场
    :param str secu_category : 证券类型
    :param str listed_sector : 上市板块
    :param str fields : 字段集合

    输出参数：
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str chi_name : 公司名称,
    :param str secu_market : 证券市场,
    :param str secu_category : 证券类型,
    :param str listed_sector : 上市板块,

    """

    headers = get_headers()
    url = base_url + 'get_st_stock_list'

    param = {'secu_market': secu_market, 'secu_category': secu_category, 'listed_sector': listed_sector, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    raise Exception(res.text)

def get_shszhk_stock_list(etfcomponent_type = None, fields = None):
    """
    ‘沪股通’和‘港股通（沪）’各自的成分股。 “深股通”和“港股通（深）”各自的成分股。 更新频率： 不定时更新

    输入参数：
    :param str etfcomponent_type : 成分股类别，默认"1"
    :param str fields : 字段集合

    输出参数：
    :param str etfcomponent_type : 成分股类别,
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str secu_category : 证券类别,
    :param str secu_market : 证券市场,
    :param str select_time : 入选股票时间,

    """

    headers = get_headers()
    url = base_url + 'get_shszhk_stock_list'

    param = {'etfcomponent_type': etfcomponent_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_quote_daily(en_prod_code = None, trading_date = None, adjust_way = 0, fields = None):
    """
    沪深日行情，包含昨收价、开盘价、最高价、最低价、收盘价、成交量、成交金额等数据；

    输入参数：
    :param str en_prod_code : 证券代码，默认"600570.SH"
    :param str trading_date : 交易日期，默认"now"
    :param int adjust_way : 复权方式，默认0
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证券代码,
    :param str trading_date : 交易日期,
    :param float prev_close_price : 前收盘价,
    :param float open_price : 开盘价,
    :param float high_price : 最高价,
    :param float low_price : 最低价,
    :param float close_price : 收盘价,
    :param str avg_price : 变动均价,
    :param float px_change : 价格涨跌,
    :param float px_change_rate : 涨跌幅,
    :param float turnover_ratio : 换手率,
    :param float business_balance : 成交额,
    :param float turnover_deals : 成交笔数,
    :param float amplitude : 振幅,
    :param float issue_price_change : 相对发行价涨跌,
    :param float issue_price_change_rate : 相对发行价涨跌幅（%）,
    :param str recently_trading_date : 最近交易日期,
    :param float ratio_adjust_factor : 复权因子,
    :param float business_amount : 成交数量,
    :param str up_down_status : 涨跌停状态,
    :param str turnover_status : 交易状态,

    """

    headers = get_headers()
    url = base_url + 'get_stock_quote_daily'

    param = {'en_prod_code': en_prod_code, 'trading_date': trading_date, 'adjust_way': adjust_way, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_quote_weekly(en_prod_code = None, trading_date = None, adjust_way = 0, fields = None):
    """
    沪深周行情，包含上周收价、周开盘价、周最高价、周最低价、周收盘价、周成交量、周成交金额等数据；

    输入参数：
    :param str en_prod_code : 证券代码，默认"600570.SH"
    :param str trading_date : 交易日期，默认"now"
    :param int adjust_way : 复权方式，默认0
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str trading_date : 交易日期,
    :param float week_prev_close_price : 周前收盘价,
    :param float week_open_price : 周开盘价,
    :param float week_high_price : 周最高价,
    :param float week_low_price : 周最低价,
    :param float week_close_price : 周收盘价,
    :param float week_max_close_price : 周最高收盘价,
    :param float week_min_close_price : 周最低收盘价,
    :param float week_avg_close_price : 周均价,
    :param float week_avg_business_balance : 周日均成交额,
    :param float week_avg_business_amount : 周日均成交量,
    :param float week_px_change : 周涨跌,
    :param float week_px_change_rate : 周涨跌幅（%）,
    :param float week_turnover_ratio : 周换手率（%）,
    :param float week_avg_turnover_ratio : 周日平均换手率（%）,
    :param float week_business_amount : 周成交量,
    :param float week_business_balance : 周成交额,
    :param float week_amplitude : 周振幅（%）,
    :param str week_high_price_date : 周最高价日,
    :param str week_low_price_date : 周最低价日,
    :param str week_max_close_price_date : 周最高收盘价日,
    :param str week_min_close_price_date : 周最低收盘价日,

    """

    headers = get_headers()
    url = base_url + 'get_stock_quote_weekly'

    param = {'en_prod_code': en_prod_code, 'trading_date': trading_date, 'adjust_way': adjust_way, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_quote_monthly(en_prod_code = None, trading_date = None, adjust_way = 0, fields = None):
    """
    沪深月行情，包含月前收盘价、月开盘价、月最高价、月最低价、月收盘价、月成交量、月成交金额等数据；

    输入参数：
    :param str en_prod_code : 证券代码，默认"600570.SH"
    :param str trading_date : 交易日期，默认"now"
    :param int adjust_way : 复权方式，默认0
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str trading_date : 交易日期,
    :param float month_prev_close_price : 月前收盘价,
    :param float month_open_price : 月开盘价,
    :param float month_high_price : 月最高价,
    :param float month_low_price : 月最低价,
    :param float month_close_price : 月收盘价,
    :param float month_max_close_price : 月最高收盘价,
    :param float month_min_close_price : 月最低收盘价,
    :param float month_avg_close_price : 月均价,
    :param float month_avg_business_balance : 月日均成交额,
    :param float month_avg_business_amount : 月日均成交量,
    :param float month_px_change : 月涨跌,
    :param float month_px_change_rate : 月涨跌幅（%）,
    :param float month_turnover_ratio : 月换手率（%）,
    :param float month_avg_turnover_ratio : 月日平均换手率（%）,
    :param float month_business_amount : 月成交量,
    :param float month_business_balance : 月成交额,
    :param float month_amplitude : 月振幅（%）,
    :param str month_high_price_date : 月最高价日,
    :param str month_low_price_date : 月最低价日,
    :param str month_max_close_price_date : 月最高收盘价日,
    :param str month_min_close_price_date : 月最低收盘价日,

    """

    headers = get_headers()
    url = base_url + 'get_stock_quote_monthly'

    param = {'en_prod_code': en_prod_code, 'trading_date': trading_date, 'adjust_way': adjust_way, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_quote_yearly(en_prod_code = None, trading_date = None, adjust_way = 0, fields = None):
    """
    沪深年行情信息，包含年前收盘价、年最高价、年最低价、年日均成交量、年涨跌幅等数据；

    输入参数：
    :param str en_prod_code : 证券代码，默认"600570.SH"
    :param str trading_date : 交易日期，默认"now"
    :param int adjust_way : 复权方式，默认0
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str trading_date : 交易日期,
    :param float year_prev_close_price : 年前收盘价,
    :param float year_open_price : 年开盘价,
    :param float year_high_price : 年最高价,
    :param float year_low_price : 年最低价,
    :param float year_close_price : 年收盘价,
    :param float year_max_close_price : 年最高收盘价,
    :param float year_min_close_price : 年最低收盘价,
    :param float year_avg_close_price : 年均价,
    :param float year_avg_business_balance : 年日均成交额,
    :param float year_avg_business_amount : 年日均成交量,
    :param float year_px_change : 年涨跌,
    :param float year_px_change_rate : 年涨跌幅（%）,
    :param float year_turnover_ratio : 年换手率（%）,
    :param float year_avg_turnover_ratio : 年日平均换手率（%）,
    :param float year_business_amount : 年成交量,
    :param str year_business_balance : 本年金额,
    :param float year_amplitude : 年振幅（%）,
    :param str year_high_price_date : 年最高价日,
    :param str year_low_price_date : 年最低价日,
    :param str year_max_close_price_date : 年最高收盘价日,
    :param str year_min_close_price_date : 年最低收盘价日,

    """

    headers = get_headers()
    url = base_url + 'get_stock_quote_yearly'

    param = {'en_prod_code': en_prod_code, 'trading_date': trading_date, 'adjust_way': adjust_way, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_money_flow(en_prod_code = None, trading_date = None, fields = None):
    """
    获取单个交易日，沪深股票在不同单笔成交金额区间的累计主买、主卖金额及成交量数据；

    输入参数：
    :param str en_prod_code : 证券代码，默认"600570.SH"
    :param str trading_date : 交易日期，默认"now"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证券代码,
    :param str trading_date : 交易日期,
    :param float turnover_in : 流入成交额,
    :param float turnover_out : 流出成交额,
    :param float net_turnover_in : 资金净流入额,
    :param float amount_in : 流入成交量,
    :param float amount_out : 流出成交量,
    :param float net_amount_in : 净流入量,
    :param float super_in : 超大单流入,
    :param float super_amount_in : 主动买入特大单成交量,
    :param float large_in : 大单流入,
    :param float large_amount_in : 主动买入大单成交量,
    :param float medium_in : 中单流入,
    :param float medium_amount_in : 主动买入中单成交量,
    :param float little_in : 小单流入,
    :param float little_amount_in : 主动买入小单成交量,
    :param float super_out : 超大单流出,
    :param float super_amount_out : 主动卖出特大单成交量,
    :param float large_out : 大单流出,
    :param float large_amount_out : 主动卖出大单成交量,
    :param float medium_out : 中单流出,
    :param float medium_amount_out : 主动卖出中单成交量,
    :param float little_out : 小单流出,
    :param float little_amount_out : 主动卖出小单成交量,

    """

    headers = get_headers()
    url = base_url + 'get_money_flow'

    param = {'en_prod_code': en_prod_code, 'trading_date': trading_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_suspension_list(en_prod_code = None, trading_date = None, fields = None):
    """
    上市公司股票停牌复牌信息；

    输入参数：
    :param str suspensiondate : 停牌日期，默认"now"
    :param str fields : 字段集合

    输出参数：
    :param str secu_code : 股票代码,
    :param str secu_abbr : 股票简称,
    :param str suspend_date : 停牌日期,
    :param str suspend_time : 停牌时间,
    :param str resumption_date : 复牌日期,
    :param str resumption_time : 复牌时间,
    :param str suspend_reason : 停牌原因,

    """

    headers = get_headers()
    url = base_url + 'get_suspension_list'

    param = {'en_prod_code': en_prod_code, 'trading_date': trading_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_shareholder_top10(secu_code = None, start_date = None, end_date = None, fields = None):
    """
    获取公司十大股东相关数据，包括主要股东构成及持股数量比例、持股性质；

    输入参数：
    :param str secu_code : 证券代码，默认"600570"
    :param str start_date : 开始日期，默认"last_year_today"
    :param str end_date : 截止日期，默认"now"
    :param str fields : 字段集合

    输出参数：
    :param str secu_market : 证券市场,
    :param str secu_code : 证券代码,
    :param float secu_abbr : 证券简称,
    :param float trading_date : 交易日期,
    :param float info_source : 信息来源,
    :param float hold_vols : 合计持有股份总数（万股）,
    :param float total_rates : 合计占总股本比例（%）,
    :param float controller_name : 实际控制人,
    :param float serial_number : 股东序号,
    :param float stock_holder_name : 股东名称,
    :param float stock_holder_kind : 股东性质,
    :param float share_character_statement : 股本性质,
    :param float hold_vol : 持股份总数（万股）,
    :param float total_rate : 占总股本比例(%),
    :param float hold_vol_change : 较上期持股变动股数(万股),
    :param float total_rate_change : 较上期变动比例(%),
    :param float aas_change_type : 变动类别,

    """

    headers = get_headers()
    url = base_url + 'get_shareholder_top10'

    param = {'secu_code': secu_code, 'start_date': start_date, 'end_date': end_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_float_shareholder_top10(secu_code = None, start_date = None, end_date = None, fields = None):
    """
    获取公司十大流通股东相关数据，包括主要股东构成及持股数量比例、持股性质；

    输入参数：
    :param str secu_code : 证券代码，默认"600570"
    :param str start_date : 开始日期，默认"last_year_today"
    :param str end_date : 截止日期，默认"now"
    :param str fields : 字段集合

    输出参数：
    :param str secu_market : 证券市场,
    :param str secu_code : 证券代码,
    :param float secu_abbr : 证券简称,
    :param float trading_date : 交易日期,
    :param float info_source : 信息来源,
    :param float hold_vols : 合计持有流通股总数(万股),
    :param float float_rates : 合计占总流通股本比例(%),
    :param float controller_name : 实际控制人,
    :param float serial_number : 股东序号,
    :param float stock_holder_name : 股东名称,
    :param float stock_holder_kind : 股东性质,
    :param float share_character_statement : 股本性质,
    :param float hold_vol : 持流通股总数(万股),
    :param float float_rate : 占总流通股比例(%),
    :param float hold_vol_change : 较上期持股变动股数(万股),
    :param float total_rate_change : 较上期变动比例(%),
    :param float aas_change_type : 变动类别,

    """

    headers = get_headers()
    url = base_url + 'get_float_shareholder_top10'

    param = {'secu_code': secu_code, 'start_date': start_date, 'end_date': end_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_lh_daily(trading_day = None, fields = None):
    """
    每日龙虎榜上榜股票的股票代码、成交金额、净买入额等数据；

    输入参数：
    :param str trading_day : 交易日期，默认"now"
    :param str fields : 字段集合

    输出参数：
    :param str closing_price : 最新价(元),
    :param str price_change_ratio : 涨跌幅,
    :param float stock_total : 最近一年上榜次数,
    :param float close_price : 昨收价(元),
    :param float business_balance : 成交金额(元),
    :param float business_amount : 成交量(股),
    :param float secu_abbr : 股票简称,
    :param float secu_code : 证券代码,
    :param float trading_day : 交易日期,
    :param float net_balance : 净买入额(元),
    :param float mark : 标签,

    """

    headers = get_headers()
    url = base_url + 'get_lh_daily'

    param = {'trading_day': trading_day, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_lh_stock(secu_code = None, trading_day = None, fields = None):
    """
    获取个股龙虎榜详情，包括成交数据、营业部买入和卖出数据等；

    输入参数：
    :param str secu_code : 证券代码，默认"600570.SH"
    :param str trading_date : 交易日期，默认"now"
    :param str fields : 字段集合

    输出参数：
    :param str secu_code : 证券代码,
    :param str trading_date : 交易日期,
    :param str secu_abbr : 证券简称,
    :param str stock_total : 最近一年上榜次数,
    :param str buy_total_rate : 买入总占比,
    :param str sale_total_rate : 卖出总占比,
    :param float net_balance : 净买入金额,
    :param str net_rate : 净买入占比,
    :param float business_balance : 成交金额,
    :param int business_amount : 成交数量,
    :param str abnormal_type : 上榜类型简称,
    :param str abnormal_code : 上榜类型对应代码,
    :param str type : 席位,
    :param float buy_rate : 买入金额占总金额比,
    :param float buy_balance : 买入金额,
    :param float sale_rate : 卖出金额占总金额比,
    :param float sale_balance : 卖出金额,
    :param str sales_department_name : 营业部简称,
    :param str list_date : 近十次上榜日期,

    """

    headers = get_headers()
    url = base_url + 'get_lh_stock'

    param = {'secu_code': secu_code, 'trading_day': trading_day, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_quote_minutes(en_prod_code = None, begin_date = None, end_date = None, fields = None):
    """
    取得上市股票列表，用于股票行情查询；

    输入参数：
    :param str en_prod_code : 聚源代码，默认"600570.SH"
    :param str begin_date : 起始日期，默认"lastday"
    :param str end_date : 结束日期，默认"now"
    :param str fields : 字段集合

    输出参数：
    :param str date : 日期,
    :param str time : 发生时间,
    :param float open : 开盘价(元),
    :param float high : 最高价(元),
    :param float low : 最低价(元),
    :param float close : 收盘价(元),
    :param float turnover_volume : 成交量,
    :param float turnover_value : 成交额,
    :param float change : 涨跌幅(元),
    :param float change_pct : 涨跌幅(%),

    """

    headers = get_headers()
    url = base_url + 'get_stock_quote_minutes'

    param = {'en_prod_code': en_prod_code, 'begin_date': begin_date, 'end_date': end_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_quote_realtime():
    """
    获取单个或者多个市场行情的最新状况

    Parameters
    ----------
    fs : Union[str, List[str]], optional
        行情名称或者多个行情名列表 可选值及示例如下

        - ``None``  沪深京A股市场行情
        - ``'沪深A股'`` 沪深A股市场行情
        - ``'沪A'`` 沪市A股市场行情
        - ``'深A'`` 深市A股市场行情
        - ``北A``   北证A股市场行情
        - ``'可转债'``  沪深可转债市场行情
        - ``'期货'``    期货市场行情
        - ``'创业板'``  创业板市场行情
        - ``'美股'``    美股市场行情
        - ``'港股'``    港股市场行情
        - ``'中概股'``  中国概念股市场行情
        - ``'新股'``    沪深新股市场行情
        - ``'科创板'``  科创板市场行情
        - ``'沪股通'``  沪股通市场行情
        - ``'深股通'``  深股通市场行情
        - ``'行业板块'``    行业板块市场行情
        - ``'概念板块'``    概念板块市场行情
        - ``'沪深系列指数'``    沪深系列指数市场行情
        - ``'上证系列指数'``    上证系列指数市场行情
        - ``'深证系列指数'``    深证系列指数市场行情
        - ``'ETF'`` ETF 基金市场行情
        - ``'LOF'`` LOF 基金市场行情


    Returns
    -------
    DataFrame
        单个或者多个市场行情的最新状况

    Raises
    ------
    KeyError
        当参数 ``fs`` 中含有不正确的行情类型时引发错误

    Examples
    --------
    >>> import efinance as ef
    >>> ef.stock.get_realtime_quotes()
            股票代码   股票名称     涨跌幅     最新价      最高      最低      今开     涨跌额    换手率    量比    动态市盈率     成交量           成交额   昨日收盘           总市值         流通市值      行情ID 市场类型
    0     688787    N海天  277.59  139.48  172.39  139.25  171.66  102.54  85.62     -    78.93   74519  1110318832.0  36.94    5969744000   1213908667  1.688787   沪A
    1     301045    N天禄  149.34   39.42   48.95    39.2   48.95   23.61  66.66     -    37.81  163061   683878656.0  15.81    4066344240    964237089  0.301045   深A
    2     300532   今天国际   20.04   12.16   12.16   10.69   10.69    2.03   8.85  3.02   -22.72  144795   171535181.0  10.13    3322510580   1989333440  0.300532   深A
    3     300600   国瑞科技   20.02   13.19   13.19   11.11   11.41     2.2  18.61  2.82   218.75  423779   541164432.0  10.99    3915421427   3003665117  0.300600   深A
    4     300985   致远新能   20.01   47.08   47.08    36.8    39.4    7.85  66.65  2.17    58.37  210697   897370992.0  39.23    6277336472   1488300116  0.300985   深A
    ...      ...    ...     ...     ...     ...     ...     ...     ...    ...   ...      ...     ...           ...    ...           ...          ...       ...  ...
    4598  603186   华正新材   -10.0   43.27   44.09   43.27   43.99   -4.81   1.98  0.48    25.24   27697   120486294.0  48.08    6146300650   6063519472  1.603186   沪A
    4599  688185  康希诺-U  -10.11   476.4  534.94  460.13   530.0   -53.6   6.02  2.74 -2088.07   40239  1960540832.0  530.0  117885131884  31831479215  1.688185   沪A
    4600  688148   芳源股份  -10.57    31.3   34.39    31.3    33.9    -3.7  26.07  0.56   220.01  188415   620632512.0   35.0   15923562000   2261706043  1.688148   沪A
    4601  300034   钢研高纳  -10.96   43.12   46.81   42.88    46.5   -5.31   7.45  1.77    59.49  323226  1441101824.0  48.43   20959281094  18706911861  0.300034   深A
    4602  300712   永福股份  -13.71    96.9  110.94    95.4   109.0   -15.4   6.96  1.26   511.21  126705  1265152928.0  112.3   17645877600  17645877600  0.300712   深A

    >>> ef.stock.get_realtime_quotes(['创业板','港股'])
        股票代码    股票名称    涨跌幅    最新价     最高     最低     今开    涨跌额   换手率     量比   动态市盈率       成交量         成交额   昨日收盘         总市值        流通市值       行情ID  市场类型
    0     00859  中昌国际控股  49.02   0.38   0.38   0.26   0.26  0.125  0.08  86.85   -2.83    938000    262860.0  0.255   427510287   427510287  128.00859  None
    1     01058    粤海制革  41.05   1.34   1.51    0.9   0.93   0.39  8.34   1.61  249.89  44878000  57662440.0   0.95   720945460   720945460  128.01058  None
    2     00713  世界(集团)  27.94   0.87    0.9   0.68   0.68   0.19  1.22  33.28    3.64   9372000   7585400.0   0.68   670785156   670785156  128.00713  None
    3     08668    瀛海集团  24.65  0.177  0.179  0.145  0.145  0.035   0.0   10.0   -9.78     20000      3240.0  0.142   212400000   212400000  128.08668  None
    4     08413    亚洲杂货  24.44   0.28   0.28   0.25   0.25  0.055  0.01   3.48  -20.76    160000     41300.0  0.225   325360000   325360000  128.08413  None
    ...     ...     ...    ...    ...    ...    ...    ...    ...   ...    ...     ...       ...         ...    ...         ...         ...        ...   ...
    5632  08429    冰雪集团 -16.75  0.174    0.2  0.166    0.2 -0.035  2.48   3.52  -21.58  11895000   2074645.0  0.209    83520000    83520000  128.08429  None
    5633  00524    长城天下 -17.56  0.108  0.118  0.103  0.118 -0.023  0.45  15.43   -6.55   5961200    649171.0  0.131   141787800   141787800  128.00524  None
    5634  08377    申酉控股 -17.71  0.395   0.46   0.39   0.46 -0.085  0.07   8.06   -5.07    290000    123200.0   0.48   161611035   161611035  128.08377  None
    5635  00108    国锐地产 -19.01   1.15   1.42   1.15   1.42  -0.27  0.07   0.78   23.94   2376000   3012080.0   1.42  3679280084  3679280084  128.00108  None
    5636  08237    华星控股  -25.0  0.024  0.031  0.023  0.031 -0.008  0.43   8.74   -2.01  15008000    364188.0  0.032    83760000    83760000  128.08237  None

    >>> ef.stock.get_realtime_quotes(['ETF'])
        股票代码         股票名称   涨跌幅    最新价     最高     最低     今开    涨跌额    换手率    量比 动态市盈率       成交量           成交额   昨日收盘          总市值         流通市值      行情ID 市场类型
    0    513050     中概互联网ETF  4.49  1.444  1.455  1.433  1.452  0.062   6.71  0.92     -  12961671  1870845984.0  1.382  27895816917  27895816917  1.513050   沪A
    1    513360        教育ETF  4.38    0.5  0.502  0.486  0.487  0.021  16.89   1.7     -   1104254    54634387.0  0.479    326856952    326856952  1.513360   沪A
    2    159766        旅游ETF  3.84  0.974  0.988   0.95   0.95  0.036  14.46  1.97     -    463730    45254947.0  0.938    312304295    312304295  0.159766   深A
    3    159865        养殖ETF   3.8  0.819  0.828  0.785  0.791   0.03  12.13  0.89     -   1405871   114254714.0  0.789    949594189    949594189  0.159865   深A
    4    516670      畜牧养殖ETF  3.76  0.856  0.864  0.825  0.835  0.031  24.08  0.98     -    292027    24924513.0  0.825    103803953    103803953  1.516670   沪A
    ..      ...          ...   ...    ...    ...    ...    ...    ...    ...   ...   ...       ...           ...    ...          ...          ...       ...  ...
    549  513060      恒生医疗ETF -4.12  0.861  0.905   0.86  0.902 -0.037  47.96  1.57     -   1620502   141454355.0  0.898    290926128    290926128  1.513060   沪A
    550  515220        煤炭ETF -4.46  2.226  2.394  2.194  2.378 -0.104  14.39  0.98     -   2178176   487720560.0  2.330   3369247992   3369247992  1.515220   沪A
    551  513000  日经225ETF易方达 -4.49  1.212  1.269   1.21  1.269 -0.057   5.02  2.49     -     25819     3152848.0  1.269     62310617     62310617  1.513000   沪A
    552  513880     日经225ETF -4.59  1.163  1.224  1.162  1.217 -0.056  16.93  0.94     -     71058     8336846.0  1.219     48811110     48811110  1.513880   沪A
    553  513520        日经ETF -4.76    1.2  1.217  1.196  1.217  -0.06   27.7  1.79     -    146520    17645828.0  1.260     63464640     63464640  1.513520   沪A


    Notes
    -----
    无论股票、可转债、期货还是基金。第一列表头始终叫 ``股票代码``

    """

    headers = get_headers()
    url = base_url + 'get_stock_quote_realtime'

    param = {}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_shszhk_capitalflow(exchange_kind = None, start_date = None, end_date = None, fields = None):
    """
    统计时间范围内沪港通、深港通等资金流向数据，以及领涨领跌股，涨跌幅，资金余额等数据信息。数据每日更新。包括科创板；

    输入参数：
    :param str exchange_kind : 市场类型，默认"1"
    :param str start_date : 开始日期，默认"five days ago"
    :param str end_date : 截止日期，默认"now"
    :param str fields : 字段集合

    输出参数：
    :param str trade_date : 交易日期,
    :param float surplus_quota : 剩余额度,
    :param float now_capital_inflow : 当日资金流入（元）,
    :param float sum_capital_inflow : 历史累计流入(亿元),
    :param float now_net_purchase_balance : 当日成交净买额（百万）,
    :param float buy_balance : 买入金额,
    :param float sell_balance : 卖出金额,
    :param str led_stock_code : 领涨股代码,
    :param str led_stock_name : 领涨股名称,
    :param str secu_market : 证券市场,
    :param float led_stock_chg : 领涨股涨跌幅(%),
    :param float currency : 货币单位,

    """

    headers = get_headers()
    url = base_url + 'get_shszhk_capitalflow'

    param = {'exchange_kind': exchange_kind, 'start_date': start_date, 'end_date': end_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text
    
def get_shszhk_deal_top10(exchange_kind = None, start_date = None, end_date = None, fields = None):
    """

    输入参数：
    :param str exchange_kind : 市场类型，默认"1"
    :param str start_date : 开始日期，默认"five days ago"
    :param str end_date : 截止日期，默认"now"
    :param str fields : 字段集合

    输出参数：
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str secu_market : 证券市场,
    :param str trade_date : 交易日期,
    :param float rank : 排名,
    :param float buy_balance : 买入金额(元),
    :param float sell_balance : 卖出金额(元),
    :param float net_purchase_balance : 净买额（元）,
    :param float currency : 货币单位,
    :param float close_price : 收盘价,
    :param float px_change_rate : 涨跌幅,
    :param float business_balance : 成交金额,

    """

    headers = get_headers()
    url = base_url + 'get_shszhk_deal_top10'

    param = {'exchange_kind': exchange_kind, 'start_date': start_date, 'end_date': end_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_shszhk_distribution(exchange_kind = None, start_date = None, end_date = None, fields = None):
    """
    展示沪港通、深港通的股票涨跌分布。数据每日更新。包括科创板；

    输入参数：
    :param str exchange_kind : 市场类型，默认"1"
    :param str start_date : 开始日期，默认"five days ago"
    :param str end_date : 截止日期，默认"now"
    :param str fields : 字段集合

    输出参数：
    :param str trade_date : 交易日期,
    :param float up_count : 上涨个数,
    :param float flat_count : 平盘家数,
    :param float down_count : 下跌个数,

    """

    headers = get_headers()
    url = base_url + 'get_shszhk_distribution'

    param = {'exchange_kind': exchange_kind, 'start_date': start_date, 'end_date': end_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_shszhk_change_top10(exchange_kind = None, trading_data = None, fields = None):
    """
    按交易日统计沪港通、深港通等十大涨幅股列表，成交金额，换手率，涨跌幅数据等；

    输入参数：
    :param str exchange_kind : 市场类型，默认"1"
    :param str trading_data : 开始日期，默认"now"
    :param str fields : 字段集合

    输出参数：
    :param str trading_data : 交易日,
    :param str rank : 排名,
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str secu_market : 证券市场,
    :param float close_price : 收盘价,
    :param float px_change_rate : 涨跌幅,
    :param float turnover_value : 成交额,
    :param float turnover_ratio : 换手率,
    :param float total_mv : A股总市值,
    :param float pe_lyr : 市盈率,
    :param float float_value : A股流通市值(元),
    :param float pe_ttm : 滚动市盈率,

    """

    headers = get_headers()
    url = base_url + 'get_shszhk_change_top10'

    param = {'exchange_kind': exchange_kind, 'trading_data': trading_data, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_quote_stocklist(fields = None):
    """
    股票代码列表(用于行情查询)

    输入参数：
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证券代码(带后缀),
    :param str secu_code : 证券代码(不带后缀),
    :param str secu_abbr : 证券简称,

    """

    headers = get_headers()
    url = base_url + 'get_quote_stocklist'

    param = {'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_quote_daily_list(en_prod_code = None, begin_date = None, end_date = None, adjust_way = None):
    """

    输入参数：
    :param str en_prod_code : 证券代码
    :param str begin_date : 开始日期
    :param str end_date : 截止日期
    :param str adjust_way : 复权方式

    输出参数：
    :param str trading_date : 交易日,
    :param float prev_close_price : 前收盘价,
    :param float open_price : 开盘价,
    :param float high_price : 最高价,
    :param float low_price : 最低价,
    :param float close_price : 收盘价,
    :param float avg_price : 均价,
    :param float px_change : 涨跌,
    :param float px_change_rate : 涨跌幅,
    :param float amplitude : 振幅,
    :param float turnover_ratio : 换手率,
    :param float business_balance : 成交金额(元),
    :param float turnover_volume : 成交量(股),
    :param float issue_price_change : 距首发价涨幅,
    :param float issue_price_change_rate : 距首发价涨跌幅,

    """

    headers = get_headers()
    url = base_url + 'get_stock_quote_daily_list'

    param = {'en_prod_code': en_prod_code, 'begin_date': begin_date, 'end_date': end_date, 'adjust_way': adjust_way}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_index_quote(en_prod_code = None, trading_date = None):
    """

    输入参数：
    :param str en_prod_code : 证劵代码
    :param str trading_date : 交易日期

    输出参数：
    :param str en_prod_code : 证劵代码,
    :param str trading_date : 交易日期,
    :param float close_price : 收盘价,

    """
    
    headers = get_headers()
    url = base_url + 'get_index_quote'

    param = {'en_prod_code': en_prod_code, 'trading_date': trading_date}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_industry_category(en_prod_code = None, level = 0, fields = None):
    """
    股票在证监会行业、标普行业、中信行业等多个行业信息；

    输入参数：
    :param str en_prod_code : 证券代码，默认"600570.SH"
    :param int level : 交易日期，默认0
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 股票代码,
    :param int level : 等级,
    :param str industry_name_csrc : 证监会行业名称,
    :param str industry_code_csrc : 证监会行业代码,
    :param str industry_name_gics : GICS行业行业名称,
    :param str industry_code_gics : GICS行业行业代码,
    :param str industry_name_sw : 申万行业名称,
    :param str industry_code_sw : 申万行业代码,
    :param str industry_name_citic : 中信行业名称,
    :param str industry_code_citic : 中信行业代码,

    """

    headers = get_headers()
    url = base_url + 'get_industry_category'

    param = {'en_prod_code': en_prod_code, 'level': level, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_index_constituent(index_stock_code = None, fields = None):
    """
    主要指数的成份构成情况，包括成份证券的市场代码、入选日期等数据；

    输入参数：
    :param str index_stock_code : 指数代码，默认"399300"
    :param str fields : 字段集合

    输出参数：
    :param str index_stock_code : 指数代码,
    :param str index_secu_abbr : 指数简称,
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str secu_market : 成份股市场,
    :param str secu_category : 证券类别,
    :param str in_date : 入选日期,

    """

    headers = get_headers()
    url = base_url + 'get_index_constituent'

    param = {'index_stock_code': index_stock_code, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_org_hold(secu_code = None, org_type = None, end_date = None, fields = None):
    """
    根据报告期查询个股机构持仓明细与加仓数据；

    输入参数：
    :param str secu_code : 证券代码，默认"600570"
    :param str org_type : 机构类型
    :param str end_date : 报告期查询日，默认"2021-03-31"
    :param str fields : 字段集合

    输出参数：
    :param str secu_market : 证券市场,
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str end_date : 报告期,
    :param str sh_name : 股东名称,
    :param str org_type : 机构类型,
    :param str hold_a_sum : 持流通A股数量(万股),
    :param str hold_a_sum_rate : 占流通A股比例(%),
    :param float a_shares_rate : 占A股比例(%),
    :param str hold_a_sum_up : 加仓数量(万股),
    :param str hold_a_sum_up_rate : 加仓比例(%),
    :param str hold_a_sum_up_type : 加仓类型,
    :param float market_value : 市值(万元),

    """

    headers = get_headers()
    url = base_url + 'get_org_hold'

    param = {'secu_code': secu_code, 'org_type': org_type, 'end_date': end_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_holder_num(en_prod_code = None, report_date = None, fields = None):
    """
    公司股东户数的基本情况，包括股东户数，户均持股数量，户均持股比例等数据；

    输入参数：
    :param str en_prod_code : 证券代码，默认"600570.SH"
    :param str report_date : 报告期，默认"2021-03-31"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 内部编码,
    :param str report_date : 申报日期,
    :param str sh_num : 股东总户数,
    :param int average_hold_sum : 户均持股数量,
    :param float average_hold_sum_proportion : 户均持股比例,
    :param float proportion_change : 相对上一报告期户均持股比例差值,
    :param float avg_hold_sum_gr_quarter : 户均持股数季度增长率,
    :param float proportion_gr_quarter : 户均持股比例季度增长率,
    :param float avg_hold_sum_gr_half_a_year : 户均持股数年增长率,
    :param float proportion_gr_half_a_year : 户均持股比例年增长率,

    """

    headers = get_headers()
    url = base_url + 'get_holder_num'

    param = {'en_prod_code': en_prod_code, 'report_date': report_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_restricted_schedule(en_prod_code = None, trading_date = None, query_direction = None, fields = None):
    """
    收录上市公司因为股权分置改革、定向增发、公开增发等原因所限售的股票的具体解禁时间及相关明细数据；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str trading_date : 交易日期，默认"now"
    :param str query_direction : 查询方向，默认"0"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str trading_date : 交易日期,
    :param str start_date_for_circulating : 限售解禁日期,
    :param float new_circulation_a_shares : 新增流通A股数量,
    :param float new_circulation_a_shares_rate : 新增流通A股占已流通A股比例,
    :param float accu_circulation_a_shares : 已流通A股数量,
    :param float non_circulation_a_shares : 未流通A股数量,
    :param str new_circulation_a_shares_type : 新增流通A股类型,

    """

    headers = get_headers()
    url = base_url + 'get_restricted_schedule'

    param = {'en_prod_code': en_prod_code, 'trading_date': trading_date, 'query_direction': query_direction, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_holder_pledge(en_prod_code = None, trading_date = None, serial_number = None, fields = None):
    """
    统计股东股权质押明细，包括质押股东名称、质押股数、占总股本比例等字段，支持同时输入多个股票代码；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str trading_date : 交易日期，默认"now"
    :param str serial_number : 股东序号
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str trading_date : 交易日期,
    :param str pledge_stock_holder_name : 质押股东名称,
    :param float pledge_involved_sum : 质押涉及股数,
    :param float pct_of_frozen_pledger : 占冻结质押方持股数比例,
    :param float pct_of_total_shares : 占总股本比例,
    :param str publ_date : 股权质押公告日期,

    """

    headers = get_headers()
    url = base_url + 'get_holder_pledge'

    param = {'en_prod_code': en_prod_code, 'trading_date': trading_date, 'serial_number': serial_number, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_holder_increase(date_type = None, symbols = None, listed_sector = None, secu_market = None, share_holder_type = None, state_type = None, start_date = None, end_date = None, fields = None):
    """
    统计上市公司董事、监事、高级管理人员、股东持有本公司股份变动情况分析，可与高管持股进行合并；

    输入参数：
    :param str date_type : 日期范围类型，默认"1"
    :param str symbols : 股票代码
    :param str listed_sector : 上市板块
    :param str secu_market : 市场类型
    :param str share_holder_type : 股东类型
    :param float state_type : 增减持类型
    :param str start_date : 公告日开始日期，默认"last_year_today"
    :param str end_date : 公告日查询截止日期，默认"now"
    :param str fields : 输出字段集合

    输出参数：
    :param str id : 记录ID,
    :param str holder_name : 股东姓名,
    :param str leader_name : 领导人姓名,
    :param float involved_vol : 变动数量(股),
    :param float pct_chan_ratio : 变动后持股占总股本比例,
    :param float pct_of_total_shares : 变动数量占总股本比例(%),
    :param float price_change_ratio : 累计涨跌幅(%),
    :param str publ_date : 公告日期,
    :param str secu_abbr : 股票简称,
    :param str secu_market : 交易市场,
    :param str secu_code : 股票代码,
    :param float state_type : 增持类型,
    :param float trade_price : 交易价格,
    :param float trade_balance : 交易金额(单位：元),
    :param str listed_sector : 上市板块,
    :param str tran_date : 股权正式变动日期/过户日期（变动截止日）,
    :param str holder_type : 股东类别,
    :param str relation_description : 与领导人关系,
    :param float involved_chan_vol : 变动后持股数量(股),

    """

    headers = get_headers()
    url = base_url + 'get_holder_increase'

    param = {'date_type': date_type, 'symbols': symbols, 'listed_sector': listed_sector, 'secu_market': secu_market, 'share_holder_type': share_holder_type, 'state_type': state_type, 'start_date': start_date, 'end_date': end_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_pledge_repo(secu_code = None, end_date = None, fields = None):
    """
    1.本表记录的证券范围包括Ａ股股票，不含基金、债券；质押数量包括场内质押和场外质押，深市不包括场内股票质押式回购交易
    成功申报违约处置后对应交易的质押证券数量。 2.数据范围：2016.11-至今 3.信息来源：中国证券登记结算有限责任公司；

    输入参数：
    :param str secu_code : 股票代码，默认"600570"
    :param str end_date : 截止日期，默认"now"
    :param str fields : 字段集合

    输出参数：
    :param float pledge_ratio : 质押比例(%),
    :param str secu_code : 股票代码,
    :param str secu_abbr : 证券简称,
    :param str end_date : 截止日期,
    :param float non_pled_volume : 无限售股份质押数量(万股),
    :param float res_pled_volume : 有限售股份质押数量(万股),
    :param float total_share_a : A股总股本(万股),
    :param float pledge_num : 质押笔数,

    """

    headers = get_headers()
    url = base_url + 'get_pledge_repo'

    param = {'secu_code': secu_code, 'end_date': end_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_pledge(secu_code = None, start_date = None, end_date = None, fields = None):
    """
    获取个股股权质押解押明细数据汇总以及所占总股本比例。提供2010-01-01起数据；

    输入参数：
    :param str secu_code : 证券代码
    :param str start_date : 开始日期，默认"half year ago"
    :param str end_date : 截止日期，默认"now"
    :param str fields : 字段集合

    输出参数：
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str secu_market : 证券市场,
    :param str info_publ_date : 公告日期,
    :param float involved_sum_br_count : 涉及股数_前复权汇总,
    :param float proportion_totalshares : 占总股本比例,

    """
    
    headers = get_headers()
    url = base_url + 'get_stock_pledge'

    param = {'secu_code': secu_code, 'start_date': start_date, 'end_date': end_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_block_trade(secu_code = None, start_date = None, end_date = None, fields = None):
    """
    上市公司最新股本结构变动情况数据，展示大宗交易明细，可返回列表数据，可以通过股票代码集查询；

    输入参数：
    :param str secu_code : 证券代码，默认"600570"
    :param str start_date : 开始日期，默认"yesterday"
    :param str end_date : 截止日期，默认"now"
    :param str fields : 字段集合

    输出参数：
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str secu_market : 证券市场,
    :param str listed_sector : 上市板块,
    :param str secu_category : 证券类型,
    :param str info_source : 信息来源,
    :param str trade_date : 交易日期,
    :param float close_price : 昨收盘,
    :param float premium_ratio : A股溢价率(%),
    :param float trade_price : 成交价单位元/股,
    :param float involved_vol : 成交量单位万/股,
    :param str receiver_name : 买方营业部,
    :param str transferer_name : 卖方营业部,

    """
    
    headers = get_headers()
    url = base_url + 'get_block_trade'

    param = {'secu_code': secu_code, 'start_date': start_date, 'end_date': end_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_margin_trading(en_prod_code = None, trading_date = None, fields = None):
    """
    统计交易所公布的融资融券每日详细数据，包括融券余额、融资余额、融资买入额、融资偿还额、融券偿还额、融券偿还量等指标，
    支持同时输入多个股票代码；

    输入参数：
    :param str en_prod_code : 内部编码，默认"600570.SH"
    :param str trading_date : 交易日期，默认"2020-12-31"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 内部编码,
    :param str trading_date : 交易日期,
    :param float finance_balance : 融资余额,
    :param float security_balance : 融券余额,
    :param float finance_buy_balance : 融资买入额,
    :param float finance_refund_balance : 融资偿还额,
    :param float security_buy_balance : 融券卖出额,
    :param float security_refund_balance : 融券偿还额,
    :param float security_sell_amount : 融券卖出量,
    :param float security_refund_amount : 融券偿还量,
    :param float security_amount : 融券余量,
    :param float finance_security_balance : 融资融券余额,

    """
    
    headers = get_headers()
    url = base_url + 'get_margin_trading'

    param = {'en_prod_code': en_prod_code, 'trading_date': trading_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_interval_margin_trading(en_prod_code = None, begin_date = None, end_date = None, fields = None):
    """
    统计交易所公布的融资融券某个时间区间的数据，包含区间融资买入额、区间融资偿还额、区间融券偿还量、区间融券卖出额、区间
    融券偿还额等指标，支持同时；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str begin_date : 起始日期，默认"five years ago"
    :param str end_date : 截止日期，默认"now"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str begin_date : 起始日期,
    :param str end_date : 截止日期,
    :param float inter_finance_buy_balance : 区间融资买入额,
    :param float inter_finance_refund_balance : 区间融资偿还额,
    :param float inter_avg_finance_balance : 区间融资余额均值,
    :param float inter_security_sell_amount : 区间融券卖出量,
    :param float inter_security_refund_amount : 区间融券偿还量,
    :param float inter_security_buy_balance : 区间融券卖出额,
    :param float inter_security_refund_balance : 区间融券偿还额,
    :param float inter_avg_security_amount : 区间融券余量均值,
    :param float inter_avg_security_balance : 区间融券余额均值,
    :param float avg_finance_security_balance : 区间融资融券余额均值,

    """
    
    headers = get_headers()
    url = base_url + 'get_interval_margin_trading'

    param = {'en_prod_code': en_prod_code, 'begin_date': begin_date, 'end_date': end_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_margin_trade_detail(symbols = None, date_type = None, start_date = None, end_date = None, fields = None):
    """
    查询股票代码范围内的融资融券历史交易明细统计，包括融资买入，卖出，偿还等基本详细数据；

    输入参数：
    :param str symbols : 股票代码，默认"600570.SH"
    :param str date_type : 日期类型，默认"1"
    :param str start_date : 开始日期，默认"last_year_today"
    :param str end_date : 截止日期，默认"now"
    :param str fields : 输出字段集合

    输出参数：
    :param str secu_abbr : 证券简称,
    :param str secu_code : 证券代码,
    :param str trading_date : 交易日期,
    :param float trading_balance : 融资融券交易总金额（元）,
    :param float secu_in_total_rate : 融券占交易所融券余额比（%）,
    :param float security_net_amount : 融券净卖出,
    :param float security_refund_amount : 融券偿还量（股）,
    :param float security_sell_amount : 融券卖出量（股）,
    :param float security_balance : 融券余额（元）,
    :param float security_amount : 融券余量（股）,
    :param float fina_in_float_rate : 融资余额占流通市值比例(%),
    :param float secu_in_float_rate : 融券余额占流通市值比例(%),
    :param float fina_in_total_rate : 融资占交易所融资余额比（%）,
    :param float finance_buy_balance : 融资买入额（元）,
    :param float finance_net_balance : 融资净买入,
    :param float finance_refund_balance : 融资偿还额（元）,
    :param float finance_balance : 融资余额（元）,

    """
    
    headers = get_headers()
    url = base_url + 'get_margin_trade_detail'

    param = {'symbols': symbols, 'date_type': date_type, 'start_date': start_date, 'end_date': end_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_margin_trade_total(date_type = None, start_date = None, end_date = None, fields = None):
    """
    按市场以及融资融券的4钟类型进行交易历史总量统计，包含融资余额统计信息、融资买入额统计信息、融券余额统计信息、融资融
    券余额统计信息；

    输入参数：
    :param str date_type : 日期类型，默认"1"
    :param str start_date : 开始日期，默认"last_year_today"
    :param str end_date : 截止日期，默认"now"
    :param str fields : 输出字段集合

    输出参数：
    :param str trading_date : 交易日期,
    :param float sh_finance_balance : 沪融资余额,
    :param float sh_finance_buy_balance : 沪融资买入额,
    :param float sh_security_balance : 沪融券余额,
    :param float sh_trading_balance : 沪融资融券余额,
    :param float sz_finance_balance : 深融资余额,
    :param float sz_finance_buy_balance : 深融资买入额,
    :param float sz_security_balance : 深融券余额,
    :param float sz_trading_balance : 深融资融券余额,
    :param float tol_finance_balance : 沪深融资余额,
    :param float tol_finance_buy_balance : 沪深融资买入额,
    :param float tol_security_balance : 沪深融券余额,
    :param float tol_trading_balance : 沪深融资融券余额,

    """
    
    headers = get_headers()
    url = base_url + 'get_margin_trade_total'

    param = {'date_type': date_type, 'start_date': start_date, 'end_date': end_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_dividend(en_prod_code = None, report_date = None, fields = None):
    """
    统计上市公司历次分红基本信息，包括每股送转，每股转增股本、每股股利等指标，支持同时输入多个股票代码或报告期；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param float per_ending_original_cost : 每股送转,
    :param float per_bonus_share_ratio : 每股送股比例,
    :param float per_tran_add_share_ratio : 每股转增股比例,
    :param float cash_divi_rmb : 派现(含税/人民币元),
    :param float actual_cash_divi_rmb : 实派(税后/人民币元),
    :param str pre_disclosure_date : 预披露公告日,
    :param str advance_date : 预约日期,
    :param str announcement_date : 决案公告日,
    :param str divi_impl_date : 分红实施公告日,
    :param str right_reg_date : 股权登记日,
    :param str ex_divi_date : 除权除息日,
    :param str bonus_share_list_date : 送转股上市日,
    :param str payout_date : 股息到帐日期/红利发放日,
    :param str final_trade_date : 最后交易日,
    :param str procedure_desc : 分红方案进度,
    :param str divi_object : 分红对象,
    :param str if_dividend : 是否分红,

    """
    
    headers = get_headers()
    url = base_url + 'get_stock_dividend'

    param = {'en_prod_code': en_prod_code, 'report_date': report_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_additional(en_prod_code = None, year = None, issue_type = None, fields = None):
    """
    统计公司历次增发明细信息，包括增发方案内容、进程、实施进度、承销商等信息，支持同时输入多个股票代码或查询年度；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str year : 年度，默认"2021"
    :param str issue_type : 认购方式，默认"0"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str year : 年度,
    :param str spo_event_procedure : 事件进程,
    :param str issue_purpose : 增发目的,
    :param str issue_price : 增发价格,
    :param float issue_vol : 增发数量,
    :param float ipo_proceeds : 增发新股募集资金总额,
    :param float net_proceeds : 增发新股募集资金净额,
    :param str advance_date : 预约日期,
    :param str shareholders_publ_date : 股东大会公告日,
    :param str prospectus_publ_date : 增发公告日,
    :param str sasac_approval_publ_date : 国资委通过公告日,
    :param str csrc_approval_publ_date : 证监会批准公告日,
    :param str list_announce_date : 增发新股上市公告日期,
    :param str price_adjusted_date : 最新发行价调整日,
    :param str online_issue_date : 上网公开发行日期,
    :param str otc_date : 向网下增发日期,
    :param str sni_list_date : 增发股份上市日期,
    :param str orig_holder_preferred_date : 老股东优先配售日期,
    :param str result_date : 发行结果公示日,
    :param str scheme_change_publ_date : 方案变动公告日,
    :param str scheme_change_statement : 方案变动说明,
    :param str scheme_change_type : 方案变动类型,
    :param float issue_price_ceiling : 发行价格上限,
    :param float issue_price_floor : 发行价格下限,
    :param float adjusted_issue_price : 调整后发行价格下降,
    :param float referring_price : 承销商指导价格,
    :param float underwriting_fee : 承销费用,
    :param float pe_ratio_before_issue : 增发市盈率（按增发前总股本）,
    :param float tailored_issue_vol_legal_person : 法人定向配售股数,
    :param float staq_net_issue_vol : STAQ/NET定向配售股数,
    :param float fund_issue_vol : 投资基金配售股数,
    :param float main_income_forecast : 主营业务收入预测,
    :param float net_profit_forecast : 净利润预测,
    :param float diluted_eps_forecast : 全面摊薄每股盈利预测,

    """
    
    headers = get_headers()
    url = base_url + 'get_stock_additional'

    param = {'en_prod_code': en_prod_code, 'year': year, 'issue_type': issue_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_additional_all(en_prod_code = None, trading_date = None, spo_process = None, fields = None):
    """
    统计股票上市以来增发概况，包括增发总次数、成功次数、失败次数、累计募集资金总额等指标；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str trading_date : 交易日期，默认"2020-12-31"
    :param str spo_process : 增发进程，默认"0"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str trading_date : 交易日期,
    :param float spo_num : 增发总次数,
    :param float spo_num_success : 增发已成功次数,
    :param float spo_num_fail : 增发已失败次数,
    :param float spo_num_going : 增发进行中次数,
    :param float accu_ipo_proceeds : 增发累计募集资金总额,
    :param float accu_net_proceeds : 增发累计募集资金净额,
    :param float accu_issue_cost : 增发累计费用总额,

    """
    
    headers = get_headers()
    url = base_url + 'get_stock_additional_all'

    param = {'en_prod_code': en_prod_code, 'trading_date': trading_date, 'spo_process': spo_process, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_allotment(en_prod_code = None, year = None, fields = None):
    """
    统计公司历次配股方案信息，支持同时输入多个股票代码和查询年度。

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str year : 年度，默认"2020"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str year : 年度,
    :param float actual_allot_ratio : 实际配股比例(10配X),
    :param float allot_price : 每股配股价格,
    :param float actual_allot_vol : 实际配股数量,
    :param float ipo_proceeds : 募集资金总额,
    :param str issue_cost : 发行费用总额,
    :param float allot_price_ceiling : 配股价格上限,
    :param float allot_price_floor : 配股价格下限,
    :param float base_vol : 配股股本基数,
    :param float transfer_allot_ratio : 转配比(10转配X),
    :param float planned_allot_ratio : 计划配股比例（10配X),
    :param float planned_allot_vol : 计划配股数量,
    :param float advance_date : 预约日期,
    :param str shareholders_publ_date : 股东大会公告日期,
    :param str allot_prospectus_publ_date : 配股公告日期,
    :param str right_reg_date : 股权登记日,
    :param str ex_right_date : 除权日,
    :param str allot_start_date : 配股交款起始日,
    :param str allot_end_date : 配股交款截止日,
    :param str fund_to_account_date : 资金到帐日,
    :param str allot_list_date : 配股上市日,

    """
    
    headers = get_headers()
    url = base_url + 'get_stock_allotment'

    param = {'en_prod_code': en_prod_code, 'year': year, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_asforecastabb(secu_code = None, forcast_type = None, forecast_object = None, egrowth_rate_floor = None, fields = None):
    """
    业绩预增列表

    输入参数：
    :param str secu_code : 证券代码
    :param str forcast_type : 业绩预计类型，默认"4"
    :param str forecast_object : 预告对象，默认"10,13"
    :param str egrowth_rate_floor : 预计幅度起始(%)大于，默认"20"
    :param str fields : 字段集合

    输出参数：
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str end_date : 截止日期,
    :param str forcast_type : 业绩预计类型,
    :param str forecast_object : 预告对象,
    :param str forcast_content : 业绩预计内容描述,
    :param str egrowth_rate_floor : 变动幅度下限,
    :param str egrowth_rate_ceiling : 变动幅度上限,
    :param str eprofit_floor : 预计净利润下限,
    :param str eprofit_ceiling : 预计净利润上限,
    :param float eearning_floor : 预计收入起始(元),
    :param float eearning_ceiling : 预计收入截止(元),

    """
    
    headers = get_headers()
    url = base_url + 'get_stock_asforecastabb'

    param = {'secu_code': secu_code, 'forcast_type': forcast_type, 'forecast_object': forecast_object, 'egrowth_rate_floor': egrowth_rate_floor, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_asunderweight(secu_code = None, fields = None):
    """
    首次减持计划列表

    输入参数：
    :param str secu_code : 证劵代码
    :param str fields : 字段集合

    输出参数：
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str sh_name : 股东名称,
    :param str serial_number : 股东序号,
    :param str event_info : 事件描述,
    :param str initial_info_publ_date : 首次信息发布日期,

    """
    
    headers = get_headers()
    url = base_url + 'get_stock_asunderweight'

    param = {'secu_code': secu_code, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_asoverweight(secu_code = None, fields = None):
    """
    统计公司历次配股方案信息，支持同时输入多个股票代码和查询年度。

    输入参数：
    :param str secu_code : 证劵代码
    :param str fields : 字段集合

    输出参数：
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str initial_info_publ_date : 首次信息发布日期,
    :param str sh_name : 股东名称,
    :param str serial_number : 股东序号,
    :param str add_hold_time : 增持时间描述,
    :param float add_hold_term : 增持实施期限,
    :param str end_date : 截止日期,
    :param str add_hold_price_statement : 增持价格描述,
    :param float add_hold_share_ceiling : 增持股份数量上限,
    :param float add_hold_ratio_ceiling : 增持比例上限-占总股本,
    :param float add_hold_share_min : 增持股份数量下限,
    :param float add_hold_ratio_min : 增持比例下限-占总股本,
    :param str add_hold_statement : 增持计划说明,

    """
    
    headers = get_headers()
    url = base_url + 'get_stock_asoverweight'

    param = {'secu_code': secu_code, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_asrighttransfer(secu_code = None, year = None, tran_mode = None, fields = None):
    """
    股权转让列表

    输入参数：
    :param str secu_code : 证券代码
    :param str year : 年度
    :param str tran_mode : 股权转让方式
    :param str fields : 字段集合

    输出参数：
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str info_publ_date : 发布日期,
    :param str tran_mode : 股权转让方式,
    :param float deal_price : 交易价格(元/股),
    :param float pledge_involved_sum : 涉及股数(股),
    :param float pct_of_total_shares : 占总股本比例(%),
    :param str transferer_name : 股权出让方名称,
    :param str tran_date : 过户日期,
    :param str receiver_name : 股权受让方名称,
    :param str if_snafter_tran : 是否第1大股东变更,

    """
    
    headers = get_headers()
    url = base_url + 'get_stock_asrighttransfer'

    param = {'secu_code': secu_code, 'year': year, 'tran_mode': tran_mode, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_asraising(tran_mode = None, fields = None):
    """
    举牌列表

    输入参数：
    :param str tran_mode : 股权转让方式
    :param str fields : 字段集合

    输出参数：
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str end_date : 截止日期,
    :param float after_rece : 举牌方持股比例,
    :param str receiver_name : 举牌方,
    :param str start_date : 开始日期,
    :param str date_rang : 周期,
    :param float pledge_involved_sum : 周期内累计交易股数(股),
    :param float pct_of_total_shares : 周期内累计占比,

    """
    
    headers = get_headers()
    url = base_url + 'get_stock_asraising'

    param = {'tran_mode': tran_mode, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_share_holders(en_prod_code = None, trading_date = None, unit = 0, fields = None):
    """

    输入参数：
    :param str en_prod_code : 股票代码
    :param str trading_date : 交易日期
    :param int unit : 单位
    :param str fields : 字段集合

    输出参数：
    :param str en_prod_code : 股票代码,
    :param str trading_date : 交易日期,
    :param float total_shares : 总股本,
    :param float a_shares : A股合计（股）,
    :param float non_restricted_a_shares : 其中：无限售条件的流通A股(股),
    :param float b_shares : B股合计（股）,
    :param float circulation_b_shares : 其中：流通B股（股）,

    """
    
    headers = get_headers()
    url = base_url + 'get_stock_share_holders'

    param = {'en_prod_code': en_prod_code, 'trading_date': trading_date, 'unit': unit, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_special_tradedate(secu_code = None, start_date = None, end_date = None, special_trade_type = None, fields = None):
    """

    输入参数：
    :param str secu_code : 证券代码
    :param str start_date : 开始日期
    :param str end_date : 截止日期

    :param str special_trade_type : 特别处理(或撤销)类别
    :param str fields : 字段集合

    输出参数：
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str special_trade_time : 特别处理(或撤销)实施日期,
    :param str special_trade_type : 特别处理(或撤销)类别,

    """
    
    headers = get_headers()
    url = base_url + 'get_stock_special_tradedate'

    param = {'secu_code': secu_code, 'start_date': start_date, 'end_date': end_date, 'special_trade_type': special_trade_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_org_rate(secu_code = None, rate_type = None, start_date = None, end_date = None, fields = None):
    """

    输入参数：
    :param str secu_code : 证券代码
    :param str rate_type : 评级类型
    :param str start_date : 开始日期
    :param str end_date : 截止日期
    :param str fields : 字段集合

    输出参数：
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str secu_market : 证券市场,
    :param str writing_date : 撰写日期,
    :param str org_name : 机构名称,
    :param str title : 标题,
    :param str author : 物权作者,
    :param str conclusion : 报告结论,
    :param str rate_type_name : 评级类型名称,
    :param str rate_type : 评级类型,

    """
    
    headers = get_headers()
    url = base_url + 'get_stock_org_rate'

    param = {'secu_code': secu_code, 'rate_type': rate_type, 'start_date': start_date, 'end_date': end_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_org_rate_sum(date_type = None, secu_code = None, fields = None):
    """

    输入参数：
    :param str date_type : 类型
    :param str secu_code : 证券代码
    :param str fields : 字段集合

    输出参数：
    :param str secu_market : 证券市场,
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str buy_sum : 买入额,
    :param str increase_sum : 增持评级合计,
    :param str neutral_sum : 中性评级合计,
    :param str reduce_sum : 减持评级合计,
    :param str sale_sum : 卖出额,
    :param str total_sum : 评级合计,

    """

    headers = get_headers()
    url = base_url + 'get_stock_org_rate_sum'

    param = {'date_type': date_type, 'secu_code': secu_code, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_investor_statistics(symbols = None, secu_market = None, listed_sector = None, start_date = None, end_date = None, event_id = None, fields = None):
    """
    输入参数：
    :param str symbols : 股票代码集
    :param str secu_market : 市场类型
    :param str listed_sector : 上市板类型
    :param str start_date : 开始日期
    :param str end_date : 截止日期
    :param str event_id : 事件ID
    :param str fields : 输出字段集合

    输出参数：
    :param str event_id : 事件ID,
    :param str inner_code : 证券内部代码,
    :param str secu_abbr : 股票简称,
    :param str secu_code : 股票代码,
    :param str secu_market : 交易市场,
    :param str publ_date : 信息发布日期,
    :param str title : 标题,
    :param str listed_sector : 上市板类型,
    :param str buy_num : 买方机构数量,
    :param str sell_num : 卖方机构数量,
    :param str parly_num : 参与本次调研机构数量,
    :param str survey_date : 调研日期,

    """
    
    headers = get_headers()
    url = base_url + 'get_stock_investor_statistics'

    param = {'symbols': symbols, 'secu_market': secu_market, 'listed_sector': listed_sector, 'start_date': start_date, 'end_date': end_date, 'event_id': event_id, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_investor_detail(symbols = None, secu_market = None, listed_sector = None, date_type = None, start_date = None, end_date = None, event_id = None, fields = None):
    """

    输入参数：
    :param str symbols : 股票代码集
    :param str secu_market : 市场类型
    :param str listed_sector : 上市板类型
    :param str date_type : 日期范围类型
    :param str start_date : 开始日期
    :param str end_date : 截止日期
    :param str event_id : 事件ID
    :param str fields : 输出字段集合

    输出参数：
    :param str event_id : 事件ID,
    :param str inner_code : 证券内部代码,
    :param str secu_abbr : 股票简称,
    :param str secu_code : 股票代码,
    :param str secu_market : 交易市场,
    :param str content : 主要内容,
    :param str publ_date : 信息发布日期,
    :param str title : 标题,
    :param str listed_sector : 上市板类型,
    :param str listing_creper : 上市公司接待人员,
    :param str place : 地点,
    :param 对象 participants : 参与单位及人员集合,

    """
    
    headers = get_headers()
    url = base_url + 'get_stock_investor_detail'

    param = {'symbols': symbols, 'secu_market': secu_market, 'listed_sector': listed_sector, 'date_type': date_type, 'start_date': start_date, 'end_date': end_date, 'event_id': event_id, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_financial_industry_list(secu_code = None, standard = None, first_industry_code = None, fields = None):
    """

    输入参数：
    :param str secu_code : 证券代码
    :param str standard : 行业划分标准
    :param str first_industry_code : 一级行业代码
    :param str fields : 字段集合

    输出参数：
    :param str secu_market : 证券市场,
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str first_industry_code : 一级行业代码,
    :param str first_industry_name : 一级行业名称,
    :param str second_industry_code : 二级行业代码,
    :param str second_industry_name : 二级行业名称,
    :param str third_industry_code : 三级行业代码,
    :param str third_industry_name : 三级行业名称,
    :param str fourth_industry_code : 四级行业代码,
    :param str furth_industry_name : 四级行业名称,

    """
    
    headers = get_headers()
    url = base_url + 'get_stock_financial_industry_list'

    param = {'secu_code': secu_code, 'standard': standard, 'first_industry_code': first_industry_code, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_industry_compare(secu_code = None, end_date = None, sort_field = None, sort_type = None, second_industry_code = None, fields = None):
    """

    输入参数：
    :param str secu_code : 证券代码
    :param str end_date : 报告期
    :param str sort_field : 排序字段
    :param str sort_type : 排序方式
    :param str second_industry_code : 行业代码
    :param str fields : 字段集合

    输出参数：
    :param str secu_market : 证券市场,
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str end_date : 报告期,
    :param str second_industry_code : 行业代码,
    :param str second_industry_name : 行业名称,
    :param float operating_revenue : 营业收入,
    :param float net_profit : 归属母公司股东的净利润,
    :param float profit_ps : 每股收益,
    :param float net_asset_ps : 每股净资产,
    :param float net_profit_rate : 净利润增长率,

    """
    
    headers = get_headers()
    url = base_url + 'get_stock_industry_compare'

    param = {'secu_code': secu_code, 'end_date': end_date, 'sort_field': sort_field, 'sort_type': sort_type, 'second_industry_code': second_industry_code, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_industry_avg(secu_code = None, second_industry_code = None, end_date = None, fields = None):
    """

    输入参数：
    :param str secu_code : 证券代码
    :param str second_industry_code : 行业代码
    :param str end_date : 报告期
    :param str fields : 字段集合

    输出参数：
    :param str end_date : 报告期,
    :param str second_industry_code : 行业代码,
    :param str second_industry_name : 行业名称,
    :param float industry_operating_reenue_avg : 行业平均营业收入,
    :param float industry_net_profit_avg : 行业平均归属母公司股东的净利润,
    :param float industry_profit_ps_avg : 行业平均每股收益,
    :param float industry_netasset_ps_avg : 行业平均每股净资产,
    :param float industry_net_profit_rate_avg : 净利润增长率（行业平均）,

    """

    headers = get_headers()
    url = base_url + 'get_stock_industry_avg'

    param = {'secu_code': secu_code, 'second_industry_code': second_industry_code, 'end_date': end_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_industry_region_list(type = None, fields = None):
    """

    输入参数：
    :param str type : 类型
    :param str fields : 输出字段集

    输出参数：
    :param str type : 类型,
    :param str first_level_name : 一级名称,
    :param str first_level_code : 一级代码,
    :param 对象 level2_obj_list : 二级名称和代码,

    """
    
    headers = get_headers()
    url = base_url + 'get_stock_industry_region_list'

    param = {'type': type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_schedule_disclosure(en_prod_code = None, report_date = None, fields = None):
    """
    统计上市公司定期报告的预计披露日期与实际披露日期，支持同时输入多个股票代码或报告期；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str report_date : 申报日期,
    :param str actual_date : 定期报告实际披露日期,
    :param str plan_date : 计划执行日期,

    """
    
    headers = get_headers()
    url = base_url + 'get_schedule_disclosure'

    param = {'en_prod_code': en_prod_code, 'report_date': report_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_key_indicator(secu_code = None, start_date = None, end_date = None, report_types = None, fields = None):
    """
    获取财务数据的关键指标信息，营业收入，市盈率、市净率、总资产等。（无数值科目不出参）包括科创板；

    输入参数：
    :param str secu_code : 证券代码，默认"600570.SH"
    :param str start_date : 开始日期，默认"two days ago"
    :param str end_date : 截止日期，默认"now"
    :param str report_types : 财报类型
    :param str fields : 字段集合

    输出参数：
    :param str secu_market : 证券市场,
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str end_date : 报告期,
    :param float operating_revenue : 营业收入(元),
    :param float total_asset : 总资产(元),
    :param float total_shareholder_equity : 股东权益(元),
    :param float se_without_mi : 归属母公司股东权益(元),
    :param float net_profit : 净利润(元),
    :param float np_parent_company_owners : 归属母公司股东的净利润(元),
    :param float net_profit_cut : 扣除非经常性损益后的净利润,
    :param float basic_eps : 每股收益(元),
    :param float roe_weighted : 净资产收益率_加权(%),
    :param float roe : 净资产收益率_摊薄(%),
    :param float net_asset_ps : 每股净资产(元),
    :param float basic_eps_cut : 扣非每股收益(元),
    :param float undivided_profit : 每股未分配利润(元),
    :param float pb_ttm : 市净率,
    :param float capital_surplus_fund_ps : 每股资本公积金(元),
    :param float accumulation_fund_ps : 每股公积金,
    :param float cash_flow_ps : 每股现金流净额(元),
    :param float net_oper_cash_flowps : 每股经营活动产生的现金流量净额(元),
    :param float gross_income_ratio : 销售毛利率(%),
    :param float inventory_trate : 存货周转率(次),
    :param float net_profit_yoy : 净利润同比增长率(%),
    :param float operating_revenue_grow_rate : 营业收入同比增长率(%),
    :param float debt_assets_ratio : 资产负债率(%),
    :param float pe_ttm : 市盈率(%),

    """
    
    headers = get_headers()
    url = base_url + 'get_stock_key_indicator'

    param = {'secu_code': secu_code, 'start_date': start_date, 'end_date': end_date, 'report_types': report_types, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_accounting_data(en_prod_code = None, report_date = None, report_type = None, fields = None):
    """
    反映上市公司的主要指标，收录同一公司在报告期末的四种财务报告，即未调整的合并报表、未调整的母公司报表、调整后的合并报
    表以及调整后的母公司报表，同一报告期每种类型报表当有多次调整时，展示最新的一条记录；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str report_type : 财报类型，默认"0"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str report_date : 申报日期,
    :param float basic_eps : 每股收益EPS-基本,
    :param float diluted_eps : 每股收益EPS-稀释,
    :param float basic_eps_cut : 每股收益EPS-扣除／基本,
    :param float diluted_eps_cut : 每股收益EPS-扣除／稀释,
    :param float np_parent_company_owners_t : 每股收益EPS-期末股本摊薄,
    :param float new_np_parent_company_owners_t : 每股收益EPS-最新股本摊薄,
    :param float net_profit_cut_t : 每股收益EPS-扣除/期末股本摊薄,
    :param float new_net_profit_cut_t : 每股收益EPS-扣除/最新股本摊薄,
    :param float eps_ttm : 每股收益EPS（TTM）,
    :param float roe : 净资产收益率ROE-摊薄（公布值）,
    :param float roe_weighted : 净资产收益率ROE-加权（公布值）,
    :param float roe_avg : 净资产收益率-平均,
    :param float roe_cut : 净资产收益率_扣除,摊薄,
    :param float roe_cut_weighted : 净资产收益率（扣除-加权）,
    :param float roe_cut_avg : 净资产收益率ROE（扣除-平均）,
    :param float roe_avg_year : 净资产收益率-年化,
    :param float net_profit_cut_sewi : 净资产收益率ROE-增发条件,
    :param float total_operating_revenue : 营业总收入,
    :param float invest_income : 投资收益,
    :param float financial_expense : 财务费用,
    :param float fair_value_change_income : 公允价值变动净收益,
    :param float operating_profit : 营业利润,
    :param float non_operating_income : 营业外收入,
    :param float non_operating_expense : 营业外支出,
    :param float total_profit : 利润总额,
    :param float income_tax_cost : 所得税费用,
    :param float uncertained_investment_losses : 未确认的投资损失,
    :param float net_profit : 净利润,
    :param float np_parent_company_owners : 归属于母公司所有者的净利润,
    :param float minority_profit : 少数股东损益,
    :param float net_operate_cash_flow : 经营活动产生的现金流量净额,
    :param float net_operate_cash_flow_ps : 每股经营活动产生的现金流量净额,
    :param float net_operate_cash_flow_ps_ttm : 每股经营活动产生的现金流量净额_TTM,
    :param float net_invest_cash_flow : 投资活动产生的现金流量净额,
    :param float net_finance_cash_flow : 筹资活动产生的现金流量净额,
    :param float cash_equivalent_increase : 现金及现金等价物净增加额,
    :param float exchan_rate_change_effect : 汇率变动对现金及现金等价物的影响,
    :param float end_period_cash_equivalent : 期末现金及现金等价物余额,
    :param float cash_equivalents : 货币资金,
    :param float trading_assets : 交易性金融资产,
    :param float interest_receivable : 应收利息,
    :param float dividend_receivable : 应收股利,
    :param float account_receivable : 应收账款,
    :param float other_receivable : 其他应收款,
    :param float inventories : 存货,
    :param float total_current_assets : 流动资产合计,
    :param float hold_for_sale_assets : 可供出售金融资产,
    :param float hold_to_maturity_investments : 持有至到期投资,
    :param float investment_property : 投资性房地产,
    :param float longterm_equity_invest : 长期股权投资,
    :param float intangible_assets : 无形资产,
    :param float total_non_current_assets : 非流动资产合计,
    :param float total_assets : 资产总计,
    :param float shortterm_loan : 短期借款,
    :param float trading_liability : 交易性金融负债,
    :param float salaries_payable : 应付职工薪酬,
    :param float dividend_payable : 应付股利,
    :param float taxs_payable : 应交税费,
    :param float other_payable : 其他应付款,
    :param float non_current_liability_in_one_year : 一年内到期的非流动负债,
    :param float total_current_liability : 流动负债合计,
    :param float total_non_current_liability : 非流动负债合计,
    :param float total_liability : 负债合计,
    :param float paidin_capital : 实收资本（或股本）,
    :param float capital_reserve_fund : 资本公积,
    :param float surplus_reserve_fund : 盈余公积,
    :param float retained_profit : 未分配利润,
    :param float se_without_mi : 归属母公司股东权益合计,
    :param float minority_interests : 少数股东权益,
    :param float total_shareholder_equity : 所有者权益合计,
    :param float total_liability_and_equity : 负债和所有者权益（或股东权益）总计,
    :param float naps : 每股净资产BPS,
    :param float se_without_mi_t : 每股净资产BPS（最新股本摊薄）,

    """
    
    headers = get_headers()
    url = base_url + 'get_accounting_data'

    param = {'en_prod_code': en_prod_code, 'report_date': report_date, 'report_type': report_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_financial_cashflow(secu_code = None, start_date = None, end_date = None, merge_type = None, fields = None):
    """
    现金流量表主要是反映出资产负债表中各个项目对现金流量的影响，可用于分析一家机构在短期内有没有足够现金去应付开销。1.
    经营活动、2.投资活动、3.筹资活动、4.现金及现金等价物、5.等价物增加、6.将净利润调节为经营活动现金流量、7.不涉及现金收支的投资和筹资活动、8.现金及现金等价物净变动情况；

    输入参数：
    :param str secu_code : 证券代码，默认"600570.SH"
    :param str start_date : 开始日期，默认"two days ago"
    :param str end_date : 截止日期，默认"now"
    :param str merge_type : 合并类型，默认"1"
    :param str fields : 字段集合

    输出参数：
    :param str secu_market : 证券市场,
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str company_type : 公司类型,
    :param str end_date : 截止日期,
    :param str report_type : 报告类型,
    :param str publ_date : 公告日期,
    :param float net_deposit_in_cb_and_ib : 存放中央银行和同业款项净增加额,
    :param float other_operate_cash_paid : 支付的其他与经营活动有关的现金,
    :param float original_compensation_paid : 支付原保险合同赔付款项的现金,
    :param float net_loan_and_advance_increase : 客户贷款及垫款净增加额,
    :param float net_deal_trading_assets : 处置交易性金融资产净增加额,
    :param float net_cash_for_reinsurance : 支付再保业务现金净额,
    :param float net_operate_cash_flow : 经营活动产生的现金流量净额,
    :param float policy_dividend_cash_paid : 支付保单红利的现金,
    :param float tax_levy_refund : 收到的税费返还,
    :param float interest_and_commission_cashin : 收取利息、手续费及佣金的现金,
    :param float all_taxes_paid : 支付的各项税款,
    :param float net_insurer_deposit_investment : 保户储金及投资款净增加额,
    :param float goods_and_services_cash_paid : 购买商品、接受劳务支付的现金,
    :param float other_cashin_related_operate : 收到其他与经营活动有关的现金,
    :param float subtotal_operate_cash_outflow : 经营活动现金流出小计,
    :param float staff_behalf_paid : 支付给职工以及为职工支付的现金,
    :param float commission_cash_paid : 支付手续费及佣金的现金,
    :param float net_original_insurance_cash : 收到原保险合同保费取得的现金,
    :param float net_deposit_increase : 客户存款和同业存放款项净增加额,
    :param float net_buy_back : 回购业务资金净增加额,
    :param float net_reinsurance_cash : 收到再保业务现金净额,
    :param float goods_sale_service_render_cash : 销售商品、提供劳务收到的现金,
    :param float net_lend_capital : 拆出资金净增加额,
    :param float net_borrowing_from_central_bank : 向中央银行借款净增加额,
    :param float net_borrowing_from_finance_co : 向其他金融机构拆入资金净增加额,
    :param float subtotal_operate_cash_inflow : 经营活动现金流入小计,
    :param float invest_cash_paid : 投资支付的现金,
    :param float other_cash_from_invest_act : 收到其他与投资活动有关的现金,
    :param float net_invest_cash_flow : 投资活动产生的现金流量净额,
    :param float subtotal_invest_cash_inflow : 投资活动现金流入小计,
    :param float invest_withdrawal_cash : 收回投资收到的现金,
    :param float subtotal_invest_cash_outflow : 投资活动现金流出小计,
    :param float invest_proceeds : 取得投资收益收到的现金,
    :param float net_cash_from_sub_company : 取得子公司及其他营业单位支付的现金净额,
    :param float fix_intan_other_asset_dispo_cash : 处置固定资产、无形资产和其他长期资产而收回的现金净额,
    :param float fix_intan_other_asset_acqui_cash : 购建固定资产、无形资产和其他长期资产所支付的现金,
    :param float other_cash_to_invest_act : 支付其他与投资活动有关的现金,
    :param float net_cash_deal_sub_company : 处置子公司及其他营业单位收到的现金净额,
    :param float impawned_loan_net_increase : 质押贷款净增加额,
    :param float subtotal_finance_cash_outflow : 筹资活动现金流出小计,
    :param float other_finance_act_payment : 支付的其他与筹资活动有关的现金,
    :param float subtotal_finance_cash_inflow : 筹资活动现金流入小计,
    :param float cash_from_bonds_issue : 发行债券收到的现金,
    :param float net_finance_cash_flow : 筹资活动产生的现金流量净额,
    :param float dividend_interest_payment : 分配股利、利润或偿付利息支付的现金,
    :param float borrowing_repayment : 偿还债务所支付的现金,
    :param float cash_from_invest : 吸收投资收到的现金,
    :param float cash_from_borrowing : 取得借款收到的现金,
    :param float other_finance_act_cash : 收到其他与筹资活动有关的现金,
    :param float exchan_rate_change_effect : 汇率变动对现金的影响,
    :param float end_period_cash_equivalent : 现金等价物的期末余额,
    :param float cash_equivalent_increase : 现金及现金等价物净增加额,
    :param float begin_period_cash : 减：货币资金的期初余额,
    :param float operate_payable_increase : 经营性应付项目的增加,
    :param float fixed_asset_depreciation : 固定资产折旧,
    :param float net_profit : 净利润,
    :param float assets_depreciation_reserves : 加:资产减值准备,
    :param float accrued_expense_added : 预提费用的增加（减：减少）,
    :param float minority_profit : 少数股东损益,
    :param float fix_intanther_asset_dispo_loss : 处置固定资产、无形资产和其他长期资产的损失,
    :param float invest_loss : 投资损失(减：收益),
    :param float others : 其他,
    :param float financial_expense : 财务费用,
    :param float operate_receivable_decrease : 经营性应收项目的减少（减：增加）,
    :param float deferred_expense_decreased : 待摊费用的减少（减：增加）,
    :param float defered_tax_asset_decrease : 递延所得税资产减少,
    :param float deferred_expense_amort : 长期待摊费用的摊销,
    :param float defered_tax_liability_increase : 递延所得税负债增加,
    :param float net_operate_cash_flow_notes : (附注)经营活动产生的现金流量净额,
    :param float intangible_asset_amortization : 无形资产摊销,
    :param float inventory_decrease : 存货的减少(减：增加),
    :param float fixed_asset_scrap_loss : 固定资产报废损失(减：收益),
    :param float loss_from_fair_value_changes : 公允价值变动损失,
    :param float fixed_assets_finance_leases : 融资租入固定资产,
    :param float debt_to_captical : 债务转为资本,
    :param float cbs_expiring_within_one_year : 一年内到期的可转换公司债券,
    :param float net_incr_in_cash_and_equivalents : (附注)现金及现金等价物净增加额,
    :param float cash_equivalents_at_beginning : 减:现金等价物的期初余额,
    :param float cash_at_beginning_of_year : 减:现金的期初余额,
    :param float cash_equivalents_at_end_of_year : 加:现金等价物的期末余额,
    :param float cash_at_end_of_year : 现金的期末余额,

    """
    
    headers = get_headers()
    url = base_url + 'get_financial_cashflow'

    param = {'secu_code': secu_code, 'start_date': start_date, 'end_date': end_date, 'merge_type': merge_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_financial_income(secu_code = None, start_date = None, end_date = None, merge_type = None, fields = None):
    """
    利润表是反映企业在一定会计期间经营成果的报表，包含1.X营业利润、2.X综合收益总额、3.X营业支出、4.X营业收入
    、每股收益、6.X特别收益/收入、7.X利润总额、8.X净利润，8大模块组成。（无数值科目不出参）包括科创板；

    输入参数：
    :param str secu_code : 证券代码，默认"600570"
    :param str start_date : 开始日期，默认"two days ago"
    :param str end_date : 截止日期，默认"now"
    :param str merge_type : 合并类型，默认"1"
    :param str fields : 字段集合

    输出参数：
    :param str secu_market : 证券市场,
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str company_type : 公司类型,
    :param str end_date : 截止日期,
    :param str report_type : 报告类型,
    :param str publ_date : 公告日期,
    :param float operating_profit : 营业利润,
    :param float non_operating_income : 加:营业外收入,
    :param float non_current_assetss_deal_loss : 其中：非流动资产处置净损失,
    :param float non_operating_expense : 减:营业外支出,
    :param float ci_parent_company_owners : 归属于母公司所有者的综合收益总额,
    :param float ci_minority_owners : 归属于少数股东的综合收益总额,
    :param float total_composite_income : 综合收益总额,
    :param float operating_tax_surcharges : 营业税金及附加,
    :param float operating_payout : 营业总支出,
    :param float amortization_premium_reserve : 减:摊回保险责任准备金,
    :param float financial_expense : 财务费用,
    :param float other_operating_cost : 其他业务成本,
    :param float operating_expense : 销售费用,
    :param float amortization_expense : 减:摊回赔付支出,
    :param float amortization_reinsurance_cost : 减:摊回分保费用,
    :param float administration_expense : 管理费用,
    :param float refunded_premiums : 退保金,
    :param float operating_cost : 营业成本,
    :param float premium_reserve : 提取保险责任准备金,
    :param float policy_dividend_payout : 保单红利支出,
    :param float asset_impairment_loss : 资产减值损失,
    :param float total_operating_cost : 营业总成本,
    :param float compensation_expense : 赔付支出,
    :param float reinsurance_cost : 分保费用,
    :param float insurance_commission_expense : 保险手续费及佣金支出,
    :param float premiums_income : 保险业务收入,
    :param float unearned_premium_reserve : 提取未到期责任准备金,
    :param float premiums_earned : 已赚保费,
    :param float total_operating_revenue : 营业总收入,
    :param float reinsurance : 减：分出保费,
    :param float net_subissue_secu_income : 其中：证券承销业务净收入,
    :param float other_operating_revenue : 其他营业收入,
    :param float operating_revenue : 营业收入,
    :param float net_proxy_secu_income : 其中：代理买卖证券业务净收入,
    :param float reinsurance_income : 其中:分保费收入,
    :param float net_commission_income : 手续费及佣金净收入,
    :param float net_interest_income : 利息净收入,
    :param float interest_income : 其中：利息收入,
    :param float commission_income : 其中：手续费及佣金收入,
    :param float interest_expense : 其中：利息支出,
    :param float commission_expense : 其中：手续费及佣金支出,
    :param float net_trust_income : 其中：受托客户资产管理业务净收入,
    :param float diluted_eps : 稀释每股收益,
    :param float basic_eps : 基本每股收益,
    :param float other_net_revenue : 非营业性收入,
    :param float invest_income_associates : 其中：对联营合营企业的投资收益,
    :param float invest_income : 投资净收益,
    :param float fair_value_change_income : 公允价值变动净收益,
    :param float exchange_income : 汇兑收益,
    :param float income_tax_cost : 减：所得税费用,
    :param float total_profit : 利润总额,
    :param float minority_profit : 少数股东损益,
    :param float net_profit : 净利润,
    :param float np_parent_company_owners : 归属于母公司所有者的净利润,

    """
    
    headers = get_headers()
    url = base_url + 'get_financial_income'

    param = {'secu_code': secu_code, 'start_date': start_date, 'end_date': end_date, 'merge_type': merge_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_financial_balance(secu_code = None, start_date = None, end_date = None, merge_type = None, fields = None):
    """
    资产负债表亦称财务状况表，表示企业在一定日期的财务状况，包含1.X金融类资产、2.X金融类负债、3.X流动资金、4.
    X流动负债、5.X非流动资产、6.X非流动负债、7.X所有者权益（或股东权益）7大模块组成 。（无数值科目不出参）包括科创板；

    输入参数：
    :param str secu_code : 证券代码，默认"600570"
    :param str start_date : 开始日期，默认"two days ago"
    :param str end_date : 截止日期，默认"now"
    :param str merge_type : 合并类型，默认"1"
    :param str fields : 字段集合

    输出参数：
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str secu_market : 证券市场,
    :param str company_type : 公司类型,
    :param str end_date : 截止日期,
    :param str report_type : 报告类型,
    :param str publ_date : 公告日期,
    :param float total_assets : 资产总计,
    :param float total_liability : 负债合计,
    :param float total_liability_and_equity : 负债和股东权益总计,
    :param float settlement_provi : 结算备付金,
    :param float client_provi : 客户备付金,
    :param float deposit_in_interbank : 存放同业款项,
    :param float r_metal : 贵金属,
    :param float lend_capital : 拆出资金,
    :param float derivative_assets : 衍生金融资产,
    :param float bought_sellback_assets : 买入返售金融资产,
    :param float loan_and_advance : 发放贷款和垫款,
    :param float insurance_receivables : 应收保费,
    :param float receivable_subrogation_fee : 应收代位追偿款,
    :param float reinsurance_receivables : 应收分保账款,
    :param float receivable_unearned_r : 应收分保未到期责任准备金,
    :param float receivable_claims_r : 应收分保未决赔款准备金,
    :param float receivable_life_r : 应收分保寿险责任准备金,
    :param float receivable_lt_health_r : 应收分保长期健康险责任准备金,
    :param float insurer_impawn_loan : 保户质押贷款,
    :param float fixed_deposit : 定期存款,
    :param float refundable_capital_deposit : 存出资本保证金,
    :param float refundable_deposit : 存出保证金,
    :param float independence_account_assets : 独立账户资产,
    :param float other_assets : 其他资产,
    :param float borrowing_from_centralbank : 向中央银行借款,
    :param float deposit_of_interbank : 同业及其他金融机构存放款项,
    :param float borrowing_capital : 拆入资金,
    :param float derivative_liability : 衍生金融负债,
    :param float sold_buyback_secu_proceeds : 卖出回购金融资产款,
    :param float deposit : 吸收存款,
    :param float proxy_secu_proceeds : 代理买卖证券款,
    :param float sub_issue_secu_proceeds : 代理承销证券款,
    :param float deposits_received : 存入保证金,
    :param float advance_insurance : 预收保费,
    :param float commission_payable : 应付手续费及佣金,
    :param float reinsurance_payables : 应付分保账款,
    :param float compensation_payable : 应付赔付款,
    :param float policy_dividend_payable : 应付保单红利,
    :param float insurer_deposit_investment : 保户储金及投资款,
    :param float unearned_premium_reserve : 未到期责任准备金,
    :param float outstanding_claim_reserve : 未决赔款准备金,
    :param float life_insurance_reserve : 寿险责任准备金,
    :param float lt_health_insurance_lr : 长期健康险责任准备金,
    :param float independence_liability : 独立账户负债,
    :param float other_liability : 其他负债,
    :param float cash_equivalents : 货币资金,
    :param float client_deposit : 客户资金存款,
    :param float trading_assets : 交易性金融资产,
    :param float bill_receivable : 应收票据,
    :param float dividend_receivable : 应收股利,
    :param float interest_receivable : 应收利息,
    :param float account_receivable : 应收账款,
    :param float other_receivable : 其他应收款,
    :param float advance_payment : 预付帐款,
    :param float inventories : 存货,
    :param float non_current_asset_in_one_year : 一年内到期的非流动资产,
    :param float other_current_assets : 其他流动资产,
    :param float total_current_assets : 流动资产合计,
    :param float shortterm_loan : 短期借款,
    :param float impawned_loan : 质押借款,
    :param float trading_liability : 交易性金融负债,
    :param float notes_payable : 应付票据,
    :param float accounts_payable : 应付账款,
    :param float advance_peceipts : 预收款项,
    :param float salaries_payable : 应付职工薪酬,
    :param float dividend_payable : 应付股利,
    :param float taxs_payable : 应交税费,
    :param float interest_payable : 应付利息,
    :param float other_payable : 其他应付款,
    :param float non_current_liability_in_one_year : 一年内到期的非流动负债,
    :param float other_current_liability : 其他流动负债,
    :param float total_current_liability : 流动负债合计,
    :param float hold_for_sale_assets : 可供出售金融资产,
    :param float hold_to_maturity_investments : 持有至到期投资,
    :param float investment_property : 投资性房地产,
    :param float longterm_equity_invest : 长期股权投资,
    :param float longterm_receivable_account : 长期应收款,
    :param float fixed_assets : 固定资产,
    :param float construction_materials : 工程物资,
    :param float constru_in_process : 在建工程,
    :param float fixed_assets_liquidation : 固定资产清理,
    :param float biological_assets : 生产性生物资产,
    :param float oil_gas_assets : 油气资产,
    :param float intangible_assets : 无形资产,
    :param float seat_costs : 交易席位费,
    :param float development_expenditure : 开发支出,
    :param float good_will : 商誉,
    :param float long_deferred_expense : 长期待摊费用,
    :param float deferred_tax_assets : 递延所得税资产,
    :param float other_non_current_assets : 其他非流动资产,
    :param float total_non_current_assets : 非流动资产合计,
    :param float longterm_loan : 长期借款,
    :param float bonds_payable : 应付债券,
    :param float longterm_account_payable : 长期应付款,
    :param float long_salaries_pay : 长期应付职工薪酬,
    :param float specific_account_payable : 专项应付款,
    :param float estimate_liability : 预计负债,
    :param float deferred_tax_liability : 递延所得税负债,
    :param float long_defer_income : 长期递延收益,
    :param float other_non_current_liability : 其他非流动负债,
    :param float total_non_current_liability : 非流动负债合计,
    :param float paidin_capital : 实收资本（或股本）,
    :param float other_equityinstruments : 其他权益工具,
    :param float capital_reserve_fund : 资本公积金,
    :param float surplus_reserve_fund : 盈余公积金,
    :param float retained_profit : 未分配利润,
    :param float treasury_stock : 减：库存股,
    :param float other_composite_income : 其他综合收益,
    :param float ordinary_risk_reserve_fund : 一般风险准备金,
    :param float foreign_currency_report_conv_diff : 外币报表折算差额,
    :param float specific_reserves : 专项储备,
    :param float se_without_mi : 归属母公司股东权益合计,
    :param float minority_interests : 少数股东权益,
    :param float total_shareholder_equity : 所有者权益合计,

    """
    
    headers = get_headers()
    url = base_url + 'get_financial_balance'

    param = {'secu_code': secu_code, 'start_date': start_date, 'end_date': end_date, 'merge_type': merge_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_financial_gene_qincome(en_prod_code = None, report_date = None, report_type = None, fields = None):
    """
    1.根据2007年新会计准则制定的一般企业利润表（单季度）模板，收录自公布季报以来公司的单季利润表情况。2.科目的计
    算方法：第一、三季度直接取公布值；第二季度数据＝半年度数据－第一季度数据；第四季度数据＝年度数据－前三季度数据。各期的原始数据均取合并后的最新数据（有调整的为最新调整后数据）；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str report_type : 财报类型，默认"0"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str report_date : 申报日期,
    :param float total_operating_revenue : 单季度.营业总收入,
    :param float operating_revenue : 单季度.营业收入,
    :param float interest_income : 单季度.利息收入,
    :param float commission_income : 单季度.手续费及佣金收入,
    :param float premiums_earned : 单季度.已赚保费,
    :param float other_operating_revenue : 单季度.其他营业收入,
    :param float total_operating_cost : 单季度.营业总成本,
    :param float operating_cost : 单季度.营业成本,
    :param float interest_expense : 单季度.利息支出,
    :param float commission_expense : 单季度.手续费及佣金支出,
    :param float operating_expense : 单季度.销售费用,
    :param float administration_expense : 单季度. 管理费用,
    :param float financial_expense : 单季度.财务费用,
    :param float operating_tax_and_surcharges : 单季度.营业税金及附加,
    :param float asset_impairment_loss : 单季度.资产减值损失,
    :param float other_operating_cost : 单季度.其他营业成本,
    :param float invest_income : 单季度.投资收益,
    :param float invest_income_from_associates : 单季度.对联营合营企业的投资收益,
    :param float fair_value_change_income : 单季度.公允价值变动净收益,
    :param float operating_profit : 单季度.营业利润,
    :param float non_operating_income : 单季度.营业外收入,
    :param float non_operating_expense : 单季度.营业外支出,
    :param float non_current_assetss_deal_loss : 单季度. 非流动资产处置净损失,
    :param float total_profit : 单季度.利润总额,
    :param float income_tax_cost : 单季度.所得税费用,
    :param float uncertained_investment_loss : 单季度.未确认的投资损失,
    :param float net_profit : 单季度.净利润,
    :param float np_from_parent_company_owners : 单季度.归属于母公司所有者的净利润,
    :param float minority_profit : 单季度.少数股东损益,

    """
    
    headers = get_headers()
    url = base_url + 'get_financial_gene_qincome'

    param = {'en_prod_code': en_prod_code, 'report_date': report_date, 'report_type': report_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_financial_bank_qincome(en_prod_code = None, report_date = None, report_type = None, fields = None):
    """
    1.根据2007年新会计准则制定的商业银行利润表（单季度）模板，收录自公布季报以来公司的单季利润表情况。2.科目的计
    算方法：第一、三季度直接取公布值；第二季度数据＝半年度数据－第一季度数据；第四季度数据＝年度数据－前三季度数据。各期的原始数据均取合并后的最新数据（有调整的为最新调整后数据）；

#### 基本信息

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str report_type : 财报类型，默认"0"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str report_date : 申报日期,
    :param float operating_revenue : 单季度.营业收入,
    :param float net_interest_income : 单季度.利息净收入,
    :param float interest_income : 单季度.利息收入,
    :param float interest_expense : 单季度.利息支出,
    :param float net_commission_income : 单季度.手续费及佣金净收入,
    :param float commission_income : 单季度.手续费及佣金收入,
    :param float commission_expense : 单季度.手续费及佣金支出,
    :param float invest_income : 单季度.投资收益,
    :param float invest_income_from_associates : 单季度.对联营合营企业的投资收益,
    :param float fair_value_change_income : 单季度.公允价值变动净收益,
    :param float exchange_income : 单季度.汇兑收益,
    :param float other_operating_income : 单季度.其他业务收入,
    :param float operating_payout : 单季度.营业支出,
    :param float operating_tax_and_surcharges : 单季度.营业税金及附加,
    :param float operating_and_admin_expense : 单季度.业务及管理费,
    :param float asset_impairment_loss : 单季度.资产减值损失,
    :param float other_operating_cost : 单季度.其他营业成本,
    :param float operating_profit : 单季度.营业利润,
    :param float non_operating_income : 单季度.营业外收入,
    :param float non_operating_expense : 单季度.营业外支出,
    :param float total_profit : 单季度.利润总额,
    :param float income_tax_cost : 单季度.所得税费用,
    :param float uncertained_investment_loss :  单季度.未确认的投资损失,
    :param float net_profit : 单季度.净利润,
    :param float np_from_parent_company_owners : 单季度.归属于母公司所有者的净利润,
    :param float minority_profit : 单季度.少数股东损益,

    """

    headers = get_headers()
    url = base_url + 'get_financial_bank_qincome'

    param = {'en_prod_code': en_prod_code, 'report_date': report_date, 'report_type': report_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_financial_secu_qincome(en_prod_code = None, report_date = None, report_type = None, fields = None):
    """
    1.根据2007年新会计准则制定的证券公司利润表（单季度）模板，收录自公布季报以来公司的单季利润表情况。2.科目的计
    算方法：第一、三季度直接取公布值；第二季度数据＝半年度数据－第一季度数据；第四季度数据＝年度数据－前三季度数据。各期的原始数据均取合并后的最新数据（有调整的为最新调整后数据）；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str report_type : 财报类型，默认"0"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str report_date : 申报日期,
    :param float operating_revenue : 单季度.营业收入,
    :param float net_commission_income : 单季度.手续费及佣金净收入,
    :param float net_proxy_secu_income : 单季度.代理买卖证券业务净收入,
    :param float net_sub_issue_secu_income : 单季度.证券承销业务净收入,
    :param float net_trust_income : 单季度.受托客户资产管理业务净收入,
    :param float net_interest_income : 单季度.利息净收入,
    :param float invest_income : 单季度.投资收益,
    :param float invest_income_from_associates : 单季度.对联营合营企业的投资收益,
    :param float fair_value_change_income : 单季度.公允价值变动净收益,
    :param float exchange_income : 单季度.汇兑收益,
    :param float other_operating_income : 单季度.其他业务收入,
    :param float operating_payout : 单季度.营业支出,
    :param float operating_tax_and_surcharges : 单季度.营业税金及附加,
    :param float operating_and_admin_expense : 单季度.业务及管理费,
    :param float asset_impairment_loss : 单季度.资产减值损失,
    :param float other_operating_cost : 单季度.其他营业成本,
    :param float operating_profit : 单季度.营业利润,
    :param float non_operating_income : 单季度.营业外收入,
    :param float non_operating_expense : 单季度.营业外支出,
    :param float total_profit : 单季度.利润总额,
    :param float income_tax_cost : 单季度.所得税费用,
    :param float net_profit : 单季度.净利润,
    :param float np_from_parent_company_owners : 单季度.归属于母公司所有者的净利润,
    :param float minority_profit : 单季度.少数股东损益,

    """
    
    headers = get_headers()
    url = base_url + 'get_financial_secu_qincome'

    param = {'en_prod_code': en_prod_code, 'report_date': report_date, 'report_type': report_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_financial_insu_qincome(en_prod_code = None, report_date = None, report_type = None, fields = None):
    """
    1.根据2007年新会计准则制定的保险公司利润表（单季度）模板，收录自公布季报以来公司的单季利润表情况。2.科目的计
    算方法：第一、三季度直接取公布值；第二季度数据＝半年度数据－第一季度数据；第四季度数据＝年度数据－前三季度数据。各期的原始数据均取合并后的最新数据（有调整的为最新调整后数据）；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str report_type : 财报类型，默认"0"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param float operating_revenue : 单季度.营业收入,
    :param float premiums_earned : 单季度.已赚保费,
    :param float premiums_income : 单季度.保险业务收入,
    :param float reinsurance_income : 单季度.分保费收入,
    :param float reinsurance : 单季度.分出保费,
    :param float unearned_premium_reserve : 单季度.提取未到期责任准备金,
    :param float invest_income : 单季度.投资收益,
    :param float invest_income_from_associates : 单季度.对联营合营企业的投资收益,
    :param float fair_value_change_income : 单季度.公允价值变动净收益,
    :param float exchange_income : 单季度.汇兑收益,
    :param float other_operating_income : 单季度.其他业务收入,
    :param float operating_payout : 单季度.营业支出,
    :param float refunded_premiums : 单季度.退保金,
    :param float compensation_expense : 单季度.赔付支出,
    :param float amortization_expense : 单季度.摊回赔付支出,
    :param float premium_reserve : 单季度.提取保险责任准备金,
    :param float amortization_premium_reserve : 单季度.摊回保险责任准备金,
    :param float policy_dividend_payout : 单季度.保单红利支出,
    :param float reinsurance_cost : 单季度.分保费用,
    :param float insurance_commission_expense : 单季度.保险手续费及佣金支出,
    :param float operating_tax_and_surcharges : 单季度.营业税金及附加,
    :param float operating_and_admin_expense : 单季度.业务及管理费,
    :param float amortization_reinsurance_cost : 单季度.摊回分保费用,
    :param float asset_impairment_loss : 单季度.资产减值损失,
    :param float other_operating_cost : 单季度.其他营业成本,
    :param float operating_profit : 单季度.营业利润,
    :param float non_operating_income : 单季度.营业外收入,
    :param float non_operating_expense : 单季度.营业外支出,
    :param float total_profit : 单季度.利润总额,
    :param float net_profit : 单季度.净利润,
    :param float np_from_parent_company_owners : 单季度.归属于母公司所有者的净利润,
    :param float minority_profit : 单季度.少数股东损益,

    """
    
    headers = get_headers()
    url = base_url + 'get_financial_insu_qincome'

    param = {'en_prod_code': en_prod_code, 'report_date': report_date, 'report_type': report_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_financial_gene_qcashflow(en_prod_code = None, report_date = None, report_type = None, fields = None):
    """
    1.根据2007年新会计准则制定的一般企业现金流量表（单季度）模板，收录自公布季报以来公司的单季现金流量表情况。2.
    科目的计算方法：第一、三季度直接取公布值；第二季度数据＝半年度数据－第一季度数据；第四季度数据＝年度数据－前三季度数据。各期的原始数据均取合并后的最新数据（有调整的为最新调整后数据）；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str report_type : 财报类型，默认"0"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str report_date : 申报日期,
    :param float goods_sale_and_service_render_cash : 单季度.销售商品、提供劳务收到的现金,
    :param float tax_levy_refund : 单季度.收到的税费返还,
    :param float other_cashin_related_operate : 单季度.收到其他与经营活动有关的现金,
    :param float subtotal_operate_cash_inflow : 单季度.经营活动现金流入小计,
    :param float goods_and_services_cash_paid : 单季度.购买商品、接受劳务支付的现金,
    :param float staff_behalf_paid : 单季度.支付给职工以及为职工支付的现金,
    :param float all_taxes_paid : 单季度.支付的各项税费,
    :param float other_operate_cash_paid : 单季度.支付其他与经营活动有关的现金,
    :param float subtotal_operate_cash_outflow : 单季度.经营活动现金流出小计,
    :param float net_operate_cash_flow : 单季度.经营活动产生的现金流量净额,
    :param float invest_withdrawal_cash : 单季度.收回投资收到的现金,
    :param float invest_proceeds : 单季度.取得投资收益收到的现金,
    :param float fix_intan_other_asset_dispo_cash : 单季度.处置固定资产、无形资产和其他长期资产收回的现金净额,
    :param float net_cash_deal_subcompany : 单季度.处置子公司及其他营业单位收到的现金净额,
    :param float other_cash_from_invest_act : 单季度.收到其他与投资活动有关的现金,
    :param float subtotal_invest_cash_inflow : 单季度.投资活动现金流入小计,
    :param float fix_intan_other_asset_acqui_cash : 单季度.购建固定资产、无形资产和其他长期资产支付的现金,
    :param float invest_cash_paid : 单季度.投资支付的现金,
    :param float net_cash_from_sub_company : 单季度.取得子公司及其他营业单位支付的现金净额,
    :param float impawned_loan_net_increase : 单季度.质押贷款净增加额,
    :param float other_cash_to_invest_act : 单季度.支付其他与投资活动有关的现金,
    :param float subtotal_invest_cash_outflow : 单季度.投资活动现金流出小计,
    :param float net_invest_cash_flow : 单季度.投资活动产生的现金流量净额,
    :param float cash_from_invest : 单季度.吸收投资收到的现金,
    :param float cash_from_bonds_issue : 单季度.发行债券收到的现金,
    :param float cash_from_borrowing : 单季度.取得借款收到的现金,
    :param float other_finance_act_cash : 单季度.收到其他与筹资活动有关的现金,
    :param float subtotal_finance_cash_inflow : 单季度.筹资活动现金流入小计,
    :param float borrowing_repayment : 单季度.偿还债务支付的现金,
    :param float dividend_interest_payment : 单季度.分配股利、利润或偿付利息支付的现金,
    :param float other_finance_act_payment : 单季度.支付其他与筹资活动有关的现金,
    :param float subtotal_finance_cash_outflow : 单季度.筹资活动现金流出小计,
    :param float net_finance_cash_flow : 单季度.筹资活动产生的现金流量净额,
    :param float exchange_rate_change_effect : 单季度.汇率变动对现金及现金等价物的影响,
    :param float cash_equivalent_increase : 单季度.现金及现金等价物净增加额,

    """
    
    headers = get_headers()
    url = base_url + 'get_financial_gene_qcashflow'

    param = {'en_prod_code': en_prod_code, 'report_date': report_date, 'report_type': report_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_financial_bank_qcashflow(en_prod_code = None, report_date = None, report_type = None, fields = None):
    """
    1.根据2007年新会计准则制定的商业银行现金流量表（单季度）模板，收录自公布季报以来公司的单季现金流量表情况。2.
    科目的计算方法：第一、三季度直接取公布值；第二季度数据＝半年度数据－第一季度数据；第四季度数据＝年度数据－前三季度数据。各期的原始数据均取合并后的最新数据（有调整的为最新调整后数据）；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str report_type : 财报类型，默认"0"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str report_date : 申报日期,
    :param float net_deposit_increase : 单季度.客户存款和同业存放款项净增加额,
    :param float net_borrowing_from_central_bank : 单季度.向中央银行借款净增加额,
    :param float net_borrowing_from_finance_co : 单季度.向其他金融机构拆入资金净增加额,
    :param float interest_and_commission_cashin : 单季度.收取利息、手续费及佣金的现金,
    :param float other_cashin_related_operate : 单季度.收到其他与经营活动有关的现金,
    :param float subtotal_operate_cash_inflow : 单季度.经营活动现金流入小计,
    :param float net_loan_and_advance_increase : 单季度.客户贷款及垫款净增加额,
    :param float net_deposit_in_cb_and_ib : 单季度.存放中央银行和同业款项净增加额,
    :param float net_lend_capital : 单季度.拆出资金净增加额,
    :param float commission_cash_paid : 单季度.支付手续费及佣金的现金,
    :param float staff_behalf_paid : 单季度.支付给职工以及为职工支付的现金,
    :param float all_taxes_paid : 单季度.支付的各项税费,
    :param float other_operate_cash_paid : 单季度.支付其他与经营活动有关的现金,
    :param float subtotal_operate_cash_outflow : 单季度.经营活动现金流出小计,
    :param float net_operate_cash_flow : 单季度.经营活动产生的现金流量净额,
    :param float invest_withdrawal_cash : 单季度.收回投资收到的现金,
    :param float invest_proceeds : 单季度.取得投资收益收到的现金,
    :param float fix_intan_other_asset_dispo_cash : 单季度.处置固定资产、无形资产和其他长期资产收回的现金净额,
    :param float net_cash_deal_subcompany : 单季度.处置子公司及其他营业单位收到的现金净额,
    :param float other_cash_from_invest_act : 单季度.收到其他与投资活动有关的现金,
    :param float subtotal_invest_cash_inflow : 单季度.投资活动现金流入小计,
    :param float fix_intan_other_asset_acqui_cash : 单季度.购建固定资产、无形资产和其他长期资产支付的现金,
    :param float invest_cash_paid : 单季度.投资支付的现金,
    :param float net_cash_from_sub_company : 单季度.取得子公司及其他营业单位支付的现金净额,
    :param float other_cash_to_invest_act : 单季度.支付其他与投资活动有关的现金,
    :param float subtotal_invest_cash_outflow : 单季度.投资活动现金流出小计,
    :param float net_invest_cash_flow : 单季度.投资活动产生的现金流量净额,
    :param float cash_from_invest : 单季度.吸收投资收到的现金,
    :param float cash_from_bonds_issue : 单季度.发行债券收到的现金,
    :param float cash_from_borrowing : 单季度.取得借款收到的现金,
    :param float other_finance_act_cash : 单季度.收到其他与筹资活动有关的现金,
    :param float subtotal_finance_cash_inflow : 单季度.筹资活动现金流入小计,
    :param float borrowing_repayment : 单季度.偿还债务支付的现金,
    :param float dividend_interest_payment : 单季度.分配股利、利润或偿付利息支付的现金,
    :param float other_finance_act_payment : 单季度.支付其他与筹资活动有关的现金,
    :param float subtotal_finance_cash_outflow : 单季度.筹资活动现金流出小计,
    :param float net_finance_cash_flow : 单季度.筹资活动产生的现金流量净额,
    :param float exchange_rate_change_effect : 单季度.汇率变动对现金及现金等价物的影响,
    :param float cash_equivalent_increase : 现金及现金等价物净增加额,

    """
    
    headers = get_headers()
    url = base_url + 'get_financial_bank_qcashflow'

    param = {'en_prod_code': en_prod_code, 'report_date': report_date, 'report_type': report_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_financial_secu_qcashflow(en_prod_code = None, report_date = None, report_type = None, fields = None):
    """
    1.根据2007年新会计准则制定的证券公司现金流量表（单季度）模板，收录公布季报以来公司的单季现金流量表情况。2.科
    目的计算方法：第一、三季度直接取公布值；第二季度数据＝半年度数据－第一季度数据；第四季度数据＝年度数据－前三季度数据，各期的原始数据均取合并后的最新数据（有调整的为最新调整后数据）；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str report_type : 财报类型，默认"0"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str report_date : 申报日期,
    :param float net_deal_trading_assets : 单季度.处置交易性金融资产净增加额,
    :param float interest_and_commission_cashin : 单季度.收取利息、手续费及佣金的现金,
    :param float net_borrowing_from_finance_co : 单季度.拆入资金净增加额,
    :param float other_cashin_related_operate : 单季度.收到其他与经营活动有关的现金,
    :param float subtotal_operate_cash_inflow : 单季度.经营活动现金流入小计,
    :param float commission_cash_paid : 单季度.支付手续费及佣金的现金,
    :param float net_lend_capital : 单季度.拆出资金净增加额,
    :param float staff_behalf_paid : 单季度.支付给职工以及为职工支付的现金,
    :param float all_taxes_paid : 单季度.支付的各项税费,
    :param float other_operate_cash_paid : 单季度.支付其他与经营活动有关的现金,
    :param float subtotal_operate_cash_outflow : 单季度.经营活动现金流出小计,
    :param float net_operate_cash_flow : 单季度.经营活动产生的现金流量净额,
    :param float invest_withdrawal_cash : 单季度.收回投资收到的现金,
    :param float invest_proceeds : 单季度.取得投资收益收到的现金,
    :param float fix_intan_other_asset_dispo_cash : 单季度.处置固定资产、无形资产和其他长期资产收回的现金净额,
    :param float net_cash_deal_subcompany : 单季度.处置子公司及其他营业单位收到的现金净额,
    :param float other_cash_from_invest_act : 单季度.收到其他与投资活动有关的现金,
    :param float subtotal_invest_cash_inflow : 单季度.投资活动现金流入小计,
    :param float fix_intan_other_asset_acqui_cash : 单季度.购建固定资产、无形资产和其他长期资产支付的现金,
    :param float invest_cash_paid : 单季度.投资支付的现金,
    :param float net_cash_from_sub_company : 单季度.取得子公司及其他营业单位支付的现金净额,
    :param float other_cash_to_invest_act : 单季度.支付其他与投资活动有关的现金,
    :param float subtotal_invest_cash_outflow : 单季度.投资活动现金流出小计,
    :param float net_invest_cash_flow : 单季度.投资活动产生的现金流量净额,
    :param float cash_from_invest : 单季度.吸收投资收到的现金,
    :param float cash_from_bonds_issue : 单季度.发行债券收到的现金,
    :param float cash_from_borrowing : 单季度.取得借款收到的现金,
    :param float other_finance_act_cash : 单季度.收到其他与筹资活动有关的现金,
    :param float subtotal_finance_cash_inflow : 单季度.筹资活动现金流入小计,
    :param float borrowing_repayment : 单季度.偿还债务支付的现金,
    :param float dividend_interest_payment : 单季度.分配股利、利润或偿付利息支付的现金,
    :param float other_finance_act_payment : 单季度.支付其他与筹资活动有关的现金,
    :param float subtotal_finance_cash_outflow : 单季度.筹资活动现金流出小计,
    :param float net_finance_cash_flow : 单季度.筹资活动产生的现金流量净额,
    :param float exchange_rate_change_effect : 单季度.汇率变动对现金及现金等价物的影响,
    :param float cash_equivalent_increase : 单季度.现金及现金等价物净增加额,

    """

    headers = get_headers()
    url = base_url + 'get_financial_secu_qcashflow'

    param = {'en_prod_code': en_prod_code, 'report_date': report_date, 'report_type': report_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_financial_insu_qcashflow(en_prod_code = None, report_date = None, report_type = None, fields = None):
    """
    根据2007年新会计准则制定的保险公司现金流量表（单季度）模板，收录自公布季报以来公司的单季现金流量表情况。2.科目
    的计算方法：第一、三季度直接取公布值；第二季度数据＝半年度数据－第一季度数据；第四季度数据＝年度数据－前三季度数据。各期的原始数据均取合并后的最新数据（有调整的为最新调整后数据）；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str report_type : 财报类型，默认"0"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str report_date : 申报日期,
    :param float net_original_insurance_cash : 单季度.收到原保险合同保费取得的现金,
    :param float net_reinsurance_cash : 单季度.收到再保业务现金净额,
    :param float net_insurer_deposit_investment : 单季度.保户储金及投资款净增加额,
    :param float tax_levy_refund : 单季度.收到的税费返还,
    :param float other_cashin_related_operate : 单季度.收到其他与经营活动有关的现金,
    :param float subtotal_operate_cash_inflow : 单季度.经营活动现金流入小计,
    :param float commission_cash_paid : 单季度.支付手续费及佣金的现金,
    :param float original_compensation_paid : 单季度.支付原保险合同赔付款项的现金,
    :param float net_cash_for_reinsurance : 单季度.支付再保业务现金净额,
    :param float policy_dividend_cash_paid : 单季度.支付保单红利的现金,
    :param float staff_behalf_paid : 单季度.支付给职工以及为职工支付的现金,
    :param float all_taxes_paid : 单季度.支付的各项税费,
    :param float other_operate_cash_paid : 单季度.支付其他与经营活动有关的现金,
    :param float subtotal_operate_cash_outflow : 单季度.经营活动现金流出小计,
    :param float net_operate_cash_flow : 单季度.经营活动产生的现金流量净额,
    :param float invest_withdrawal_cash : 单季度.收回投资收到的现金,
    :param float invest_proceeds : 单季度.取得投资收益收到的现金,
    :param float fix_intan_other_asset_dispo_cash : 单季度.处置固定资产、无形资产和其他长期资产收回的现金净额,
    :param float net_cash_deal_subcompany : 单季度.处置子公司及其他营业单位收到的现金净额,
    :param float other_cash_from_invest_act : 单季度.收到其他与投资活动有关的现金,
    :param float subtotal_invest_cash_inflow : 单季度.投资活动现金流入小计,
    :param float fix_intan_other_asset_acqui_cash : 单季度.购建固定资产、无形资产和其他长期资产支付的现金,
    :param float invest_cash_paid : 单季度.投资支付的现金,
    :param float net_cash_from_sub_company : 单季度.取得子公司及其他营业单位支付的现金净额,
    :param float impawned_loan_net_increase : 单季度.质押贷款净增加额,
    :param float other_cash_to_invest_act : 单季度.支付其他与投资活动有关的现金,
    :param float subtotal_invest_cash_outflow : 单季度.投资活动现金流出小计,
    :param float net_invest_cash_flow : 单季度.投资活动产生的现金流量净额,
    :param float cash_from_invest : 单季度.吸收投资收到的现金,
    :param float cash_from_bonds_issue : 单季度.发行债券收到的现金,
    :param float cash_from_borrowing : 单季度.取得借款收到的现金,
    :param float other_finance_act_cash : 单季度.收到其他与筹资活动有关的现金,
    :param float subtotal_finance_cash_inflow : 单季度.筹资活动现金流入小计,
    :param float borrowing_repayment : 单季度.偿还债务支付的现金,
    :param float dividend_interest_payment : 单季度.分配股利、利润或偿付利息支付的现金,
    :param float other_finance_act_payment : 单季度.支付其他与筹资活动有关的现金,
    :param float subtotal_finance_cash_outflow : 单季度.筹资活动现金流出小计,
    :param float net_finance_cash_flow : 单季度.筹资活动产生的现金流量净额,
    :param float exchange_rate_change_effect : 单季度.汇率变动对现金及现金等价物的影响,
    :param float cash_equivalent_increase : 单季度.现金及现金等价物净增加额,

    """
    
    headers = get_headers()
    url = base_url + 'get_financial_insu_qcashflow'

    param = {'en_prod_code': en_prod_code, 'report_date': report_date, 'report_type': report_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_performance_forecast(en_prod_code = None, report_date = None, forecast_object = None, fields = None):
    """
    统计上市公司对未来报告期本公司业绩的预计情况，包括业绩预计类型、预计内容、具体预计值等，并收录了实际指标和研究员的一
    致性预测值；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str forecast_object : 预告对象，默认"0"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str report_date : 申报日期,
    :param str result_statement : 业绩预告摘要,
    :param str forcast_type : 业绩预告类型,
    :param str publ_date : 业绩预告日期,
    :param str forcast_content : 业绩预告内容,
    :param float eprofit_ceiling : 预计净利润上限,
    :param float eprofit_floor : 预计净利润下限,
    :param float egrowth_rate_ceiling : 变动幅度上限,
    :param float egrowth_rate_floor : 变动幅度下限,
    :param float eeps_ceiling : 预计每股收益上限,
    :param float eeps_floor : 预计每股收益下限,
    :param float basic_eps : 去年同期每股收益,
    :param float np_yoy_consistent_forecast : 一致预期净利润增幅,

    """
    
    headers = get_headers()
    url = base_url + 'get_performance_forecast'

    param = {'en_prod_code': en_prod_code, 'report_date': report_date, 'forecast_object': forecast_object, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_performance_letters(en_prod_code = None, report_date = None, fields = None):
    """
    收录上市公司在业绩快报中披露的主要财务数据和指标；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str report_date : 申报日期,
    :param str period_mark : 业绩快报类型,
    :param str publ_date : 业绩快报披露日,
    :param float operating_revenue : 营业收入,
    :param float operating_profit : 营业利润,
    :param float total_profit : 利润总额,
    :param float np_parent_company_owners : 归属母公司股东的净利润,
    :param float net_profit_cut : 扣除非经常性损益后的净利润,
    :param float net_operate_cash_flow : 经营活动现金流量净额,
    :param float basic_eps : 每股收益-基本,
    :param float roe : 净资产收益率-摊薄,
    :param float roe_weighted : 净资产收益率-加权,
    :param float net_asset_ps : 每股净资产,
    :param float net_operate_cash_flow_ps : 每股经营活动现金流量净额,
    :param float total_assets : 总资产,
    :param float se_without_mi : 归属上市公司股东的所有者权益,
    :param float total_shares : 总股本,
    :param float operating_revenue_yoy : 主营业务收入同比,
    :param float gross_profit_yoy : 主营业务利润同比,
    :param float operating_profit_yoy : 营业利润同比,
    :param float np_parent_company_owners_yoy : 归属母公司净利润同比,
    :param float net_profit_cut_yoy : 扣除非经常性损益后净利润同比,
    :param float basic_eps_yoy : 每股收益(摊薄) 同比,
    :param float roe_weighted_yoy : 净资产收益率(加权) 同比,
    :param float net_asset_ps_to_opening : 每股净资产较期初比,
    :param float total_assets_to_opening : 总资产较期初比,
    :param float se_without_mi_to_opening : 归属母公司股东权益较期初比,

    """
    
    headers = get_headers()
    url = base_url + 'get_performance_letters'

    param = {'en_prod_code': en_prod_code, 'report_date': report_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_performance_letters_q(en_prod_code = None, report_date = None, fields = None):
    """
    通过上市公司在业绩快报中披露的主要财务数据和指标，计算单季度主要财务指标；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str report_date : 申报日期,
    :param float operating_revenue_d : 营业收入（单季度）,
    :param float operating_profit_d : 营业利润（单季度）,
    :param float total_profit_d : 利润总额（单季度）,
    :param float np_parent_company_owners_d : 归属母公司股东的净利润（单季度）,
    :param float net_profit_cut_d : 扣除非经常性损益净利润（单季度）,
    :param float operating_revenue_div : 主营业务收入单季度同比,
    :param float operating_profit_div : 营业利润单季度同比,
    :param float total_profit_div : 利润总额单季度同比,
    :param float np_parent_company_owners_div : 归属母公司股东的净利润单季度同比,
    :param float net_profit_cut_div : 扣除非经常性损益后净利润单季度同比,
    :param float operating_revenue_mom : 主营业务收入单季度环比,
    :param float operating_profit_mom : 营业利润单季度环比,
    :param float total_profit_mom : 利润总额单季度环比,
    :param float np_parent_company_owners_mom : 归属母公司股东的净利润单季度环比,
    :param float net_profit_cut_div_mom : 扣除非经常性损益后净利润单季度环比,

    """
    
    headers = get_headers()
    url = base_url + 'get_performance_letters_q'

    param = {'en_prod_code': en_prod_code, 'report_date': report_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_main_composition(en_prod_code = None, report_date = None, classification = None, order = None, fields = None):
    """
    按报告期统计上市公司主营业务构成情况，支持同时输入多个股票代码或报告期；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str classification : 分类，默认"0"
    :param str order : 页内记录排序规则，默认"0"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str report_date : 申报日期,
    :param str main_oper_income : 主营业务收入金额占比,
    :param str moi_project : 主营构成（按行业）-项目名称,
    :param float moi_main_oper_income : 主营构成（按行业）-项目收入,
    :param float moi_main_oper_cost : 主营构成（按行业）-项目成本,
    :param float moi_moc : 主营构成（按行业）-项目利润,
    :param str mop_project : 主营构成（按产品）-项目名称,
    :param float mop_main_oper_income : 主营构成（按产品）-项目收入,
    :param float mop_main_oper_cost : 主营构成（按产品）-项目成本,
    :param float mop_moc : 主营构成（按产品）-项目利润,
    :param str mor_project : 主营构成（按地区）-项目名称,
    :param float mor_main_oper_income : 主营构成（按地区）-项目收入,
    :param float mor_main_oper_cost : 主营构成（按地区）-项目成本,
    :param float mor_moc : 主营构成（按地区）-项目利润,

    """
    
    headers = get_headers()
    url = base_url + 'get_main_composition'

    param = {'en_prod_code': en_prod_code, 'report_date': report_date, 'classification': classification, 'order': order, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_trading_parties(en_prod_code = None, report_date = None, report_type = None, fields = None):
    """
    统计公司向前5名供应商的采购情况及向前5名客户的销售情况等，支持同时输入多个股票代码或报告期；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str report_type : 财报类型，默认"1"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str report_date : 申报日期,
    :param float operating_revenue_top5_customers : 营业收入-前5名客户,
    :param float operating_revenue_rate_top5_customers : 营业收入占比-前5名客户,
    :param float main_oper_income_rate_top5_customers : 主营业务收入占比-前5名客户,
    :param float purchase_top5_supplier : 采购额-前5名供应商,
    :param float purchase_rate_top5_supplier : 采购额占比-前5名供应商,
    :param float main_oper_cost_rate_top5_supplier : 主营业务成本占比-前5名供应商,

    """

    headers = get_headers()
    url = base_url + 'get_trading_parties'

    param = {'en_prod_code': en_prod_code, 'report_date': report_date, 'report_type': report_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_audit_opinion(en_prod_code = None, report_date = None, fields = None):
    """
    中介机构对公司季度、半年度、年度经营情况的评价，包括公司招股以来的历次纪录，支持同时输入多个股票代码或报告期；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str report_date : 申报日期,
    :param str accounting_firm : 审计单位,
    :param str signature_accountant : 签字注册会计师,
    :param str audit_opinion_type : 审计意见,

    """
    
    headers = get_headers()
    url = base_url + 'get_audit_opinion'

    param = {'en_prod_code': en_prod_code, 'report_date': report_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_per_share_index(en_prod_code = None, report_date = None, report_type = None, fields = None):
    """
    根据报告期公布的财务科目数据衍生而来的每股指标，若某个报告期的数据有多次调整，则该表展示最新合并调整数据；若某报告期
    暂未披露调整后数据，则展示调整前的合并数据，支持同时输入多个股票代码和报告期；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str report_type : 财报类型，默认"0"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str report_date : 申报日期,
    :param float basic_eps : 每股收益EPS-基本,
    :param float diluted_eps : 每股收益EPS-稀释,
    :param float basic_eps_cut : 每股收益EPS-扣除／基本,
    :param float diluted_eps_cut : 每股收益EPS-扣除／稀释,
    :param float naps : 每股净资产BPS,
    :param float net_operate_cash_flow_ps : 每股经营活动产生的现金流量净额,
    :param float np_parent_company_owners_t : 每股收益EPS-期末股本摊薄,
    :param float new_np_parent_company_owners_t : 每股收益EPS-最新股本摊薄,
    :param float net_profit_cut_t : 每股收益EPS-扣除/期末股本摊薄,
    :param float new_net_profit_cut_t : 每股收益EPS-扣除/最新股本摊薄,
    :param float eps_ttm : 每股收益EPS（TTM）,
    :param float se_without_mi_t : 每股净资产BPS（最新股本摊薄）,
    :param float net_operate_cash_flow_ps_ttm : 每股经营活动产生的现金流量净额_TTM,
    :param float total_operating_revenue_ps : 每股营业总收入,
    :param float operating_revenue_ps : 每股营业收入,
    :param float operating_revenue_ps_ttm : 每股营业收入（TTM）,
    :param float ebit_ps : 每股息税前利润,
    :param float capital_surplus_fund_ps : 每股资本公积,
    :param float surplus_reserve_fund_ps : 每股盈余公积,
    :param float undivided_profit : 每股未分配利润,
    :param float retained_earnings_ps : 每股留存收益,
    :param float cash_flowps : 每股现金流量净额,
    :param float cash_flowps_ttm : 每股现金流量净额（TTM）,
    :param float enterprise_fcf_ps : 每股企业自由现金流量,
    :param float shareholder_fcf_ps : 每股股东自由现金流量,

    """
    
    headers = get_headers()
    url = base_url + 'get_per_share_index'

    param = {
'en_prod_code': en_prod_code, 'report_date': report_date, 'report_type': report_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_profitability(en_prod_code = None, report_date = None, report_type = None, fields = None):
    """
    根据报告期公布的财务科目数据衍生而来盈利能力相关指标，若某个报告期的数据有多次调整，则该表展示最新合并调整数据；若某
    报告期暂未披露调整后数据，则展示调整前的合并数据，支持同时输入多个股票代码和报告期；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str report_type : 财报类型，默认"0"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param float roe : 净资产收益率ROE-摊薄（公布值）,
    :param float roe_weighted : 净资产收益率ROE-加权（公布值）,
    :param float roe_avg : 净资产收益率-平均,
    :param float roe_cut : 净资产收益率_扣除,摊薄,
    :param float roe_cut_weighted : 净资产收益率（扣除-加权）,
    :param float roe_cut_avg : 净资产收益率ROE（扣除-平均）,
    :param float roe_avg_year : 净资产收益率-年化,
    :param float net_profit_cut_sewi : 净资产收益率ROE-增发条件,
    :param float total_assets : 总资产报酬率,
    :param float total_assets_year : 总资产报酬率-年化,
    :param float roa : 总资产净利率ROA,
    :param float roa_year : 总资产净利率-年化,
    :param float roic : 投入资本回报率,
    :param float roic_ttm : 投入资本回报率（TTM）,
    :param float rop : 人力投入回报率,
    :param float net_profit_ratio : 销售净利率,
    :param float gross_income_ratio : 销售毛利率,
    :param float sales_cost_ratio : 销售成本率,
    :param float period_costs_rate : 销售期间费用率,
    :param float total_profit_cost_ratio : 成本费用利润率,
    :param float np_to_tor : 净利润／营业总收入,
    :param float operating_profit_to_tor : 营业利润／营业总收入,
    :param float ebit_to_tor : 息税前利润／营业总收入,
    :param float ebitda : 息税折旧摊销前利润,
    :param float t_operating_cost_to_tor : 营业总成本／营业总收入,
    :param float operating_expense_rate : 销售费用／营业总收入,
    :param float admini_expense_rate : 管理费用／营业总收入,
    :param float financial_expense_rate : 财务费用／营业总收入,
    :param float asset_impa_loss_to_tor : 资产减值损失／营业总收入,
    :param float asset_impa_loss_or : 资产减值损失／营业利润,
    :param float roe_ttm : 净资产收益率ROE（TTM）,
    :param float roa_ebit_ttm : 总资产收益率ROA（TTM）,
    :param float roa_ttm : 总资产净利率（TTM）,
    :param float net_profit_ratio_ttm : 销售净利率_TTM,
    :param float gross_income_ratio_ttm : 销售毛利率（TTM）,
    :param float period_costs_rate_ttm : 销售期间费用率_TTM,
    :param float np_to_tor_ttm : 净利润／营业总收入_TTM,
    :param float operating_profit_to_tor_ttm : 营业利润／营业总收入_TTM,
    :param float ebit_to_tor_ttm : 息税前利润／营业总收入_TTM,
    :param float t_operating_cost_to_tor_ttm : 营业总成本／营业总收入_TTM,
    :param float operating_expense_rate_ttm : 销售费用／营业总收入_TTM,
    :param float admini_expense_rate_ttm : 管理费用／营业总收入_TTM,
    :param float financial_expense_rate_ttm : 财务费用／营业总收入_TTM,
    :param float asset_impa_loss_to_tor_ttm : 资产减值损失／营业总收入_TTM,
    :param float asset_impa_loss_or_ttm : 资产减值损失／营业利润（TTM）,

    """
    
    headers = get_headers()
    url = base_url + 'get_profitability'

    param = {
'en_prod_code': en_prod_code, 'report_date': report_date, 'report_type': report_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_growth_capacity(en_prod_code = None, report_date = None, report_type = None, fields = None):
    """
    获根据报告期公布的财务科目数据衍生出的衡量成长能力的相关指标，主要从同比角度分析，展示同比增长率。若某个报告期的数据
    有多次调整，则该表展示最新合并调整数据；若某报告期暂未披露调整后数据，则展示调整前的合并数据，支持同时输入多个股票代码和报告期；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str report_type : 财报类型，默认"0"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str report_date : 申报日期,
    :param float basic_eps : 每股收益-基本（同比增长率）,
    :param float diluted_eps : 每股收益-稀释（同比增长率）,
    :param float net_operate_cash_flow_ps : 每股经营活动产生的现金流量净额（同比增长率）,
    :param float total_operating_revenue : 营业总收入（同比增长率）,
    :param float operating_revenue : 营业收入（同比增长率）,
    :param float operating_cost : 营业成本（同比增长率）,
    :param float gross_profit : 毛利（同比增长率）,
    :param float operating_profit : 营业利润（同比增长率）,
    :param float total_profit : 利润总额（同比增长率）,
    :param float net_profit : 净利润（同比增长率）,
    :param float np_parent_company_owners : 归属母公司股东的净利润（同比增长率）,
    :param float np_parent_non_recu : 归属母公司股东的净利润扣除非经常损益（同比增长率）,
    :param float net_operate_cash_flow : 经营活动产生的现金流量净额（同比增长率）,
    :param float roe : 净资产收益率（同比增长率）,
    :param float goods_sale_service_render_cash : 销售商品、提供劳务收到的现金（同比增长率）,
    :param float goods_and_services_cash_paid : 购买商品、接受劳务支付的现金（同比增长率）,
    :param float staff_behalf_paid : 支付给职工以及为职工支付的现金（同比增长率）,
    :param float net_profit_cashcover : 净利润现金含量（同比增长率）,
    :param float se_without_mi : 净资产（同比增长率）,
    :param float total_liability : 总负债（同比增长率）,
    :param float total_assets : 总资产（同比增长率）,
    :param float cash_equivalent_increase : 现金净流量（同比增长率）,

    """

    headers = get_headers()
    url = base_url + 'get_growth_capacity'

    param = {
'en_prod_code': en_prod_code, 'report_date': report_date, 'report_type': report_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_du_pont_analysis(en_prod_code = None, report_date = None, report_type = None, fields = None):
    """
    根据报告期公布的财务科目数据，利用杜邦分析方法衍生衡量公司主要财务分析指标，若某个报告期的数据有多次调整，则该表展示
    最新合并调整数据；若某报告期暂未披露调整后数据，则展示调整前的合并数据，支持同时输入多个股票代码和报告期；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str report_type : 财报类型，默认"0"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str report_date : 申报日期,
    :param float np_parent_sew : 权益净利率ROE,
    :param float net_profit_ratio : 销售净利率,
    :param float operating_ni_to_tp : 净利润/利润总额,
    :param float total_profit_ebit : 利润总额/息税前利润,
    :param float ebit_to_tor : 息税前利润／营业总收入,
    :param float operating_revenue_ta : 资产周转率,
    :param float equity_multipler : 权益乘数,
    :param float np_parent_company_owners_ratio : 归属于母公司股东的净利润占比,

    """
    
    headers = get_headers()
    url = base_url + 'get_du_pont_analysis'

    param = {
'en_prod_code': en_prod_code, 'report_date': report_date, 'report_type': report_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_deri_fin_indicators(en_prod_code = None, report_date = None, report_type = None, fields = None):
    """
    统计由上市公司的主要会计科目（合并报表）衍生出来的数据，三大财务报表中任意报表在某报告期的数据经历调整/修订，则该表
    相关字段展示每个历史调整数据；未经历调整/修订的报表相关字段则沿用未调整数据，支持同时输入多个股票代码和报告期；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str report_type : 财报类型，默认"0"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str report_date : 申报日期,
    :param float interest_free_curr_liabilities : 无息流动负债,
    :param float interest_free_non_curr_liabilities : 无息非流动负债,
    :param float interest_bear_debt : 带息债务,
    :param float net_debt : 净债务,
    :param float total_paid_in_capital : 全部投入资本,
    :param float working_capital : 营运资本,
    :param float net_working_capital : 净营运资本,
    :param float net_tangible_assets : 有形资产净值,
    :param float retained_earnings : 留存收益,
    :param float non_recurring_profit_loss : 非经常性损益,
    :param float net_profit_cut : 扣除非经常性损益后的净利润,
    :param float gross_profit : 毛利,
    :param float net_income_from_operating : 经营活动净收益,
    :param float net_income_from_value_change : 价值变动净收益,
    :param float ebit : 息税前利润,
    :param float ebitda : 息税折旧摊销前利润,
    :param float total_operating_revenue_ttm : 营业总收入(TTM),
    :param float total_operating_cost_ttm : 营业总成本(TTM),
    :param float operating_revenue_ttm : 营业收入(TTM),
    :param float operating_cost_ttm : 营业成本-非金融类(TTM),
    :param float operating_payout_ttm : 营业支出-金融类(TTM),
    :param float gross_profit_ttm : 毛利(TTM),
    :param float operating_expense_ttm : 销售费用(TTM),
    :param float administration_expense_ttm : 管理费用(TTM),
    :param float financial_expense_ttm : 财务费用(TTM),
    :param float asset_impairment_loss_ttm : 资产减值损失(TTM),
    :param float net_income_from_operating_ttm : 经营活动净收益(TTM),
    :param float net_income_from_value_change_ttm : 价值变动净收益(TTM),
    :param float operating_profit_ttm : 营业利润(TTM),
    :param float net_non_operating_income_ttm : 营业外收支净额(TTM),
    :param float ebit_ttm : 息税前利润(TTM),
    :param float total_profit_ttm : 利润总额(TTM),
    :param float net_profit_ttm : 净利润TTM,
    :param float np_parent_company_owners_ttm : 归属于母公司所有者的净利润TTM,
    :param float free_cash_flow_to_firm : 企业自由现金流量FCFF,
    :param float free_cash_flow_to_equity : 股权自由现金流量FCFE,
    :param float current_accrued_da : 当期计提折旧与摊销,
    :param float sale_service_render_cash_ttm : 销售商品提供劳务收到的现金(TTM),
    :param float net_operate_cash_flow_ttm : 经营活动现金净流量(TTM),
    :param float net_invest_cash_flow_ttm : 投资活动现金净流量(TTM),
    :param float net_finance_cash_flow_ttm : 筹资活动现金净流量(TTM),
    :param float net_cash_flow_ttm : 现金净流量(TTM),

    """

    headers = get_headers()
    url = base_url + 'get_deri_fin_indicators'

    param = {
'en_prod_code': en_prod_code, 'report_date': report_date, 'report_type': report_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_q_financial_indicator(en_prod_code = None, report_date = None, report_type = None, fields = None):
    """
    本表收录自公布公司的单季主要财务指标，第一、三季度直接取公布值；第二季度数据＝半年度数据－第一季度数据；第四季度数据
    ＝年度数据－前三季度数据。各期的原始数据均取合并后的最新数据（有调整的为最新调整后数据），支持同时输入多个股票代码和报告期；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str report_date : 申报日期，默认"2020-12-31"
    :param str report_type : 财报类型，默认"0"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str report_date : 申报日期,
    :param float eps : 单季度.每股收益EPS,
    :param float net_profit_cut : 扣除非经常性损益后的净利润,
    :param float net_income_from_operating : 单季度.经营活动净收益,
    :param float net_income_from_value_change : 单季度.价值变动净收益,
    :param float np_f_se_without_mi : 单季度.净资产收益率ROE,
    :param float net_profit_nrp_swe : 单季度.净资产收益率（扣除非经常损益） ,
    :param float roa : 单季度.总资产净利率ROA,
    :param float net_profit_ratio : 单季度.销售净利率,
    :param float gross_income_ratio : 单季度.销售毛利率,
    :param float t_operating_cost_to_tor : 营业总成本／营业总收入,
    :param float operating_profit_to_tor : 营业利润／营业总收入,
    :param float np_to_tor : 单季度.净利润/营业总收入,
    :param float operating_expense_rate : 单季度.销售费用/营业总收入,
    :param float admini_expense_rate : 单季度.管理费用/营业总收入,
    :param float financial_expense_rate : 单季度.财务费用/营业总收入,
    :param float asset_impa_loss_or : 单季度.资产减值损失/营业利润,
    :param float operating_ni_to_tp : 单季度.经营活动净收益/利润总额 ,
    :param float value_change_ni_to_tp : 单季度.价值变动净收益/利润总额,
    :param float np_cut_to_tp : 单季度.扣除非经常损益后的净利润/净利润 ,
    :param float sale_service_cash_to_or : 单季度.销售商品提供劳务收到的现金/营业收入,
    :param float cash_rate_of_sales : 单季度.经营活动产生的现金流量净额/营业收入,
    :param float net_operate_cash_flow_rate : 单季度.经营活动产生的现金流量净额占比,
    :param float net_invest_cash_flow_rate : 单季度.投资活动产生的现金流量净额占比,
    :param float net_finance_cash_flow_rate : 单季度.筹资活动产生的现金流量净额占比,
    :param float oper_cycle : 营业周期,
    :param float inventory_turnover_rate : 存货周转率,
    :param float inventory_turnover_days : 存货周转天数,
    :param float accounts_receivables_turnover_rate : 应收帐款周转率,
    :param float accounts_receivables_turnover_days : 应收帐款周转天数,
    :param float total_asset_turnover_rate : 总资产周转率,
    :param float current_assets_turnover_rate : 流动资产周转率,
    :param float fixed_asset_turnover_rate : 固定资产周转率,
    :param float eps_yoy : 单季度.每股收益EPS同比增长率 ,
    :param float eps_mom : 单季度.每股收益EPS环比增长率 ,
    :param float total_operating_revenue_yoy : 单季度.营业总收入同比增长率,
    :param float total_operating_revenue_mom : 单季度.营业总收入环比增长率,
    :param float operating_revenue_yoy : 单季度.营业收入同比增长率,
    :param float operating_revenue_mom : 单季度.营业收入环比增长率,
    :param float operating_cost_yoy : 单季度.营业成本同比增长率,
    :param float operating_cost_mom : 单季度.营业成本环比增长率,
    :param float gross_profit_yoy : 单季度.毛利同比增长率,
    :param float gross_profit_mom : 单季度.毛利环比增长率,
    :param float operating_profit_yoy : 单季度.营业利润同比增长率 ,
    :param float operating_profit_mom : 单季度.营业利润环比增长率 ,
    :param float net_profit_yoy : 单季度.净利润同比增长率 ,
    :param float net_profit_mom : 单季度.净利润环比增长率 ,
    :param float np_parent_company_cut_yoy : 单季度.归属母公司股东的净利润同比增长率,
    :param float np_parent_company_cut_mom : 单季度.归属母公司股东的净利润环比增长率,
    :param float net_profit_cut_yoy : 单季度.扣除非经常性损益后的净利润同比增长率,
    :param float net_profit_cut_mom : 单季度.扣除非经常性损益后的净利润环比增长率,
    :param float cash_equivalent_increase_yoy : 单季度.现金净流量同比增长率,
    :param float cash_equivalent_increase_mom : 单季度.现金净流量环比增长率,
    :param float net_operate_cash_flow_yoy : 单季度.经营性现金净流量同比增长率,
    :param float net_operate_cash_flow_mom : 单季度.经营性现金净流量环比增长率,

    """
    
    headers = get_headers()
    url = base_url + 'get_q_financial_indicator'

    param = {
'en_prod_code': en_prod_code, 'report_date': report_date, 'report_type': report_type, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_valuation_info(en_prod_code = None, trading_date = None, year = None, fields = None):
    """
    利用定期报告中披露的财务指标对上市公司做估值分析，主要包括股息率、市净率、市销率、市现率等额指标，支持同时输入多个股
    票代码；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str trading_date : 交易日期，默认"2020-12-31"
    :param str year : 年度，默认"2020"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str trading_date : 交易日期,
    :param float total_market_value : 总市值,
    :param float total_market_value2 : 总市值2,
    :param float total_market_value_zjh : 总市值（证监会算法）,
    :param float pe_ttm : 市盈率PE（TTM）,
    :param float pe_ttm_deduct_non_recurring_profit : 市盈率PE（TTM,扣除非经常性损益）,
    :param float pe_rate_lyr : 市盈率（最新年报，LYR）,
    :param float pb_lf : 市净率PB（最新财报，LF）,
    :param float ps_ttm : 市销率PS（TTM）,
    :param float ps_lyr : 市销率PS（最新年报，LYR）,
    :param float pcf_oper_cashflow_ttm : 市现率PCF（经营现金流TTM）,
    :param float pcf_net_cashflow_ttm : 市现率PCF（现金净流量TTM）,
    :param float pcf_oper_cashflow_lyr : 市现率PCF（经营现金流LYR）,
    :param float pcf_net_cashflow_lyr : 市现率PCF（经营净流量LYR）,
    :param float dividend_rate : 股息率（年初至最新报告期）,
    :param float total_cash_divi_com_rate_rmb : 股息率（近12个月）,
    :param float total_cash_divi_com_rate_rmb2 : 股息率,

    """
    
    headers = get_headers()
    url = base_url + 'get_valuation_info'

    param = {
'en_prod_code': en_prod_code, 'trading_date': trading_date, 'year': year, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_corporation_value(en_prod_code = None, trading_date = None, fields = None):
    """
    统计上市公司A股市值、B股市值、企业价值等指标，支持同时输入多个股票代码；

    输入参数：
    :param str en_prod_code : 证劵代码，默认"600570.SH"
    :param str trading_date : 交易日期，默认"2020-12-31"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 证劵代码,
    :param str trading_date : 交易日期,
    :param float enterprise_value1 : 企业价值（含货币资金）,
    :param float enterprise_value2 : 企业价值（剔除货币资金）,
    :param float enterprise_times : 企业倍数,
    :param float total_market_value : 总市值（不可回测）,
    :param float a_shares_market_value : A股市值（含限售股）,
    :param float a1_shares_market_value : A股市值（不含限售股）,
    :param float b_shares_market_value : B股市值（含限售股，交易币种）,
    :param float b_shares_market_value_rmb : B股市值（含限售股，人民币）,
    :param float b1_shares_market_value : B股市值（不含限售股，交易币种）,
    :param float b1_shares_market_value_rmb : B股市值（不含限售股，人民币）,

    """
    
    headers = get_headers()
    url = base_url + 'get_corporation_value'

    param = {
'en_prod_code': en_prod_code, 'trading_date': trading_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_main_composition(secu_code = None, start_date = None, end_date = None, classification = None, fields = None):
    """

    输入参数：
    :param str secu_code : 证券代码
    :param str start_date : 开始日期
    :param str end_date : 截止日期
    :param str classification : 分类
    :param str fields : 字段集合

    输出参数：
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str secu_market : 证券市场,
    :param str end_date : 报告期,
    :param str classification : 分类,
    :param str project : 经营项目名称,
    :param float main_oper_income : 主营业务收入,
    :param float main_oper_cost : 主营业务成本,
    :param float gross_profit : 毛利,
    :param float main_income_grow_rate_yoy : 主营业务收入同比,
    :param float main_cost_grow_rate_yoy : 主营业务成本同比,
    :param float gross_profit_yoy : 毛利同比,
    :param float gross_profit_per : 毛利占比,
    :param float main_oper_income_rate : 主营业务收入占比,
    :param float main_oper_cost_rate : 主营业务成本占比,

    """    
    
    headers = get_headers()
    url = base_url + 'get_stock_main_composition'

    param = {'secu_code': secu_code, 'start_date': start_date, 'end_date': end_date, 'classification': classification, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_main_business_total(secu_code = None, classification = None, fields = None):
    """

    输入参数：
    :param str secu_code : 证券代码
    :param str classification : 分类
    :param str fields : 字段集合

    输出参数：
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str report_date : 申报日期,
    :param str industry : 项目名称,
    :param float main_oper_income : 主营业务收入金额,
    :param float main_oper_income_rate : 主营业务收入所占比率,
    :param float main_oper_cost : 主营业务成本金额,
    :param float main_oper_cost_rate : 主营业务成本所占比率,
    :param float main_oper_profit : 主营业务利润金额,
    :param float main_oper_profit_rate : 主营业务利润所占比率,
    :param float gross_profit_rate : 毛利率,
    :param float main_income_grow_rate_yoy : 收入同比增长,

    """    
    
    headers = get_headers()
    url = base_url + 'get_stock_main_business_total'

    param = {'secu_code': secu_code, 'classification': classification, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_stock_main_business_indurstry(en_prod_code = None):
    """
    输入参数：
    :param str en_prod_code : 产品代码集

    输出参数：
    :param str report_date : 申报日期,
    :param str industry : 行业名称,
    :param float main_oper_income : 主营业务收入金额,
    :param float main_oper_income_rate : 主营业务收入所占比率,
    :param float main_oper_cost : 主营业务成本金额,
    :param float main_oper_cost_rate : 主营业务成本所占比率,
    :param float main_oper_profit : 主营业务利润金额,
    :param float main_oper_profit_rate : 主营业务利润所占比率,
    :param float gross_profit_rate : 毛利率,
    :param float main_income_grow_rate_yoy : 收入同比增长,

    """
    
    headers = get_headers()
    url = base_url + 'get_stock_main_business_indurstry'

    param = {'en_prod_code': en_prod_code}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_star_ipodeclare(report_status = None, fields = None):
    """

    输入参数：
    :param str report_status : 申报状态，默认"1"
    :param str fields : 字段集合

    输出参数：
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str accept_date : 受理日期,
    :param str report_status : 申报状态,
    :param str industry_code_csrc : 所属证监会行业代码,
    :param str industry_name_csrc : 所属证监会行业名称,
    :param str sponsor_institution : 保荐机构,
    :param str accounting_firm : 会计师事务所,
    :param str law_firm : 律师事务所,

    """
    
    headers = get_headers()
    url = base_url + 'get_star_ipodeclare'

    param = {'report_status': report_status, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_star_companyprofile(secu_code = None, fields = None):
    """

    输入参数：
    :param str secu_code : 证券代码，默认"X21398"
    :param str fields : 字段集合

    输出参数：
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str chi_name : 公司名称,
    :param str eng_name : 英文名称,
    :param str establishment_date : 成立日期,
    :param str uniform_social_credit_code : 统一社会信用代码,
    :param str legal_repr : 法人代表,
    :param float regcapital : 注册资本(元),
    :param str reg_addr : 注册地址,
    :param str province : 注册地省份,
    :param str general_manager : 总经理,
    :param str secretary : 董事会秘书,
    :param str contact_tel : 联系电话,
    :param str email : 公司邮箱,
    :param str website : 网址,
    :param str brief_intro : 公司简介,
    :param str industry_name_csrc : 所属证监会行业名称,

    """
    
    headers = get_headers()
    url = base_url + 'get_star_companyprofile'

    param = {'secu_code': secu_code, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_neeq_basic(en_prod_code = None, fields = None):
    """

    输入参数：
    :param str en_prod_code : 证劵代码，默认"400002.OC"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 产品代码,
    :param str secu_code : 证券代码,
    :param str secu_abbr : 证券简称,
    :param str secu_category : 证券类别,
    :param str listed_date : 挂牌日期,
    :param str trans_type : 交易类型,
    :param str listed_state : 上市状态,
    :param str secu_market : 证券市场,
    :param str listed_sector : 上市板块,
    :param str isin_code : ISIN代码,

    """
    
    headers = get_headers()
    url = base_url + 'get_neeq_basic'

    param = {'en_prod_code': en_prod_code, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_neeq_company(en_prod_code = None, fields = None):
    """

    输入参数：
    :param str en_prod_code : 证劵代码，默认"400002.OC"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 产品代码,
    :param str chi_name : 公司中文名称,
    :param str eng_name : 公司英文名称,
    :param str establishment_date : 公司成立日期,
    :param str regcapital : 注册资本,
    :param str legal_repr : 法人代表,
    :param str major_business : 主营业务,
    :param str minor_business : 经营范围-兼营,
    :param str state : 省份,
    :param str city_code : 地级行政区,
    :param str reg_addr : 公司注册地址 公司注册地址,
    :param str reg_zip_code : 公司注册地址邮编,
    :param str offece_addr : 公司办公地址,
    :param str office_zip : 公司办公地址邮编,
    :param str tel : 联系电话,
    :param str fax : 传真,
    :param str email : 电子邮件,
    :param str website : 公司网址,
    :param str disclosure_web : 信息披露网址,
    :param str disclosure_paper : 信息披露报纸,
    :param str business_reg_number : 工商登记号,
    :param str economic_nature : 经济性质,
    :param str company_nature : 企业性质,
    :param str company_cval : 企业属性,
    :param str company_type : 公司类型,
    :param str brief_intro : 公司介绍,
    :param str reg_org : 登记机关,

    """
    
    headers = get_headers()
    url = base_url + 'get_neeq_company'

    param = {'en_prod_code': en_prod_code, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_neeq_leader(en_prod_code = None, fields = None):
    """

    输入参数：
    :param str en_prod_code : 证劵代码，默认"400002.OC"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 产品代码,
    :param str chairman_current : 董事长(现任),
    :param str chairman_former : 董事长(历任),
    :param str general_manager_current : 总经理(现任),
    :param str general_manager_former : 总经理(历任),
    :param str chief_financial_officer_current : 财务总监(现任),
    :param str chief_financial_officer_former : 财务总监(历任),
    :param str secretary_current : 董事会秘书(现任),
    :param str secretary_former : 董事会秘书(历任),

    """
    
    headers = get_headers()
    url = base_url + 'get_neeq_leader'

    param = {'en_prod_code': en_prod_code, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_neeq_leader_num(en_prod_code = None, end_date = None, fields = None):
    """

    输入参数：
    :param str en_prod_code : 证劵代码，默认"400005.OC"
    :param str end_date : 截止日期，默认"2015-12-31"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 产品代码,
    :param str end_date : 截止日期,
    :param float bd_number : 董事会成员数量,
    :param float bs_number : 监事会成员数量,
    :param float manager_number : 高级管理人员数量,

    """
    
    headers = get_headers()
    url = base_url + 'get_neeq_leader_num'

    param = {'en_prod_code': en_prod_code, 'end_date': end_date, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_neeq_industry(en_prod_code = None, level = None, fields = None):
    """

    输入参数：
    :param str en_prod_code : 证劵代码，默认"400001.OC"
    :param str level : 等级，默认"0"
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 产品代码,
    :param float level : 等级,
    :param str industry_code_csrc : 所属证监会行业代码,
    :param str industry_name_csrc : 所属证监会行业名称,
    :param str industry_code : 行业类,
    :param str industry_name : 行业类名称,
    :param str industry_code_neeq_management : 所属三板管理型行业代码,
    :param str industry_name_neeq_management : 所属三板管理型行业名称,
    :param str industry_code_neeq_investment : 所属三板投资型行业代码,
    :param str industry_name_neeq_investment : 所属三板投资型行业名称,

    """
    
    headers = get_headers()
    url = base_url + 'get_neeq_industry'

    param = {'en_prod_code': en_prod_code, 'level': level, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_neeq_perform_fore(en_prod_code = None, report_date = None, unit = None, fields = None):
    """

    输入参数：
    :param str en_prod_code : 证劵代码
    :param str report_date : 申报日期
    :param str unit : 单位
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 产品代码,
    :param str report_date : 申报日期,
    :param str forcast_type : 报告类型,
    :param float eprofit_floor : 预计净利润下限,
    :param float eprofit_ceiling : 预计净利润上限,
    :param float eprofit_range_floor : 预计利润幅度下限,
    :param float eprofit_range_ceiling : 预计利润幅度上限,
    :param float eearning_floor : 预计收入下限,
    :param float eearning_ceiling : 预计收入上限,
    :param float eearning_range_floor : 预计收入幅度下限,
    :param float eearning_range_ceiling : 预计收入幅度上限,
    :param float eeps_floor : 预计每股收益下限,
    :param float eeps_ceiling : 预计每股收益上限,
    :param float eeps_range_ceiling : 预计每股收益幅度上限,
    :param float eeps_range_floor : 预计每股收益幅度下限,
    :param str result_statement : 业绩预计结果说明,
    :param str forcast_content : 业绩预计内容描述,

    """
    
    headers = get_headers()
    url = base_url + 'get_neeq_perform_fore'

    param = {'en_prod_code': en_prod_code, 'report_date': report_date, 'unit': unit, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_neeq_dupont_analysis(en_prod_code = None, report_date = None, unit = None, fields = None):
    """

    输入参数：
    :param str en_prod_code : 证劵代码
    :param str report_date : 申报日期
    :param str unit : 单位
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 产品代码,
    :param str report_date : 申报日期,
    :param float roe_avg : 净资产收益率(ROE)-平均,
    :param float roa : 资产净利率,
    :param float equity_multipler : 权益乘数-期末,
    :param float equity_multipler_avg : 权益乘数-平均,
    :param float net_profit_ratio : 净利润/营业总收入（销售净利率）,
    :param float total_asset_turnover_rate : 总资产周转率,
    :param float np_parent_company_owners_ratio : 归属母公司股东的净利润/净利润,
    :param float operating_ni_to_tp : 净利润/利润总额,
    :param float total_profit_ebit : 利润总额/息税前利润,
    :param float ebit_to_tor : 息税前利润／营业总收入,
    :param float debt_assets_ratio : 资产负债率,
    :param float net_profit : 净利润,
    :param float total_operating_revenue : 营业总收入,
    :param float total_assets_avg : 平均资产总额,
    :param float total_debit : 负债总额,
    :param float total_assets : 资产总额,

    """
    
    headers = get_headers()
    url = base_url + 'get_neeq_dupont_analysis'

    param = {'en_prod_code': en_prod_code, 'report_date': report_date, 'unit': unit, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_neeq_share_stru(en_prod_code = None, end_date = None, unit = None, fields = None):
    """

    输入参数：
    :param str en_prod_code : 证劵代码
    :param str end_date : 截止日期
    :param str unit : 单位
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 产品代码,
    :param str end_date : 截止日期,
    :param float total_shares : 总股本,
    :param float unlimited_shares : 无限售股份总数,
    :param float unlimited_proportion : 无限售股份比例,
    :param float unlimited_number_a : 无限售:控股股东和实际制人数量,
    :param float unlimited_ratio_a : 无限售:控股股东和实际制人比例,
    :param float unlimited_number_b : 无限售:董事、监事、高管数量,
    :param float unlimited_ratio_b : 无限售:董事、监事、高管比例,
    :param float unlimited_number_c : 无限售:核心员工数量,
    :param float unlimited_ratio_c : 无限售:核心员工比例,
    :param float unlimited_number_d : 其它无限售数量,
    :param float unlimited_ratio_d : 其它无限售比例,
    :param float restricted_number_e : 有限售股份总数,
    :param float restricted_ratio_e : 有限售股份比例,
    :param float restricted_number_f : 有限售:控股股东和实际制人数量,
    :param float restricted_ratio_f : 有限售:控股股东和实际制人比例,
    :param float restricted_number_g : 有限售:董事、监事、高管数量,
    :param float restricted_ratio_g : 有限售:董事、监事、高管比例,
    :param float restricted_number_h : 有限售:核心员工数量,
    :param float restricted_ratio_h : 有限售:核心员工比例,
    :param float restricted_number_i : 其它有限售数量,
    :param float restricted_ratio_i : 其它有限售比例,

    """
    
    headers = get_headers()
    url = base_url + 'get_neeq_share_stru'

    param = {'en_prod_code': en_prod_code, 'end_date': end_date, 'unit': unit, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_neeq_per_share_index(en_prod_code = None, report_date = None, unit = None, fields = None):
    """

    输入参数：
    :param str en_prod_code : 证劵代码
    :param str report_date : 申报日期
    :param str unit : 单位
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 产品代码,
    :param str report_date : 申报日期,
    :param float basic_eps : 每股收益EPS-基本,
    :param float diluted_eps : 每股收益EPS-稀释,
    :param float np_parent_company_owners_t : 每股收益EPS-期末股本摊薄,
    :param float net_profit_cut_t : 每股收益EPS-扣除/期末股本摊薄,
    :param float new_np_parent_company_owners_t : 每股收益EPS-最新股本摊薄,
    :param float naps : 每股净资产BPS,
    :param float se_without_mi_t : 每股净资产BPS-最新股本摊薄,
    :param float total_operating_revenue_ps : 每股营业总收入,
    :param float operating_revenue_ps : 每股营业收入,
    :param float operating_revenue_ps_ttm : 每股营业收入_TTM,
    :param float oper_profit_ps : 每股营业利润,
    :param float capital_surplus_fund_ps : 每股资本公积金,
    :param float surplus_reserve_fund_ps : 每股盈余公积,
    :param float undivided_profit : 每股未分配利润,
    :param float retained_earnings_ps : 每股留存收益,
    :param float net_operate_cash_flow_ps : 每股经营活动产生的现金流量净额,
    :param float net_operate_cash_flow_ps_ttm : 每股经营活动产生的现金流量净额_TTM,
    :param float cash_flowps : 每股现金流量净额,
    :param float cash_flowps_ttm : 每股现金流量净额_TTM,

    """    
    
    headers = get_headers()
    url = base_url + 'get_neeq_per_share_index'

    param = {'en_prod_code': en_prod_code, 'report_date': report_date, 'unit': unit, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_neeq_issue_count(en_prod_code = None, date_range = None, date_type = None, unit = None, fields = None):
    """

    输入参数：
    :param str en_prod_code : 证劵代码
    :param str date_range : 统计区间
    :param str date_type : 日期类型
    :param str unit : 单位
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 产品代码,
    :param str date_range : 统计区间,
    :param str date_type : 日期类型,
    :param float issued_plan_number : 增发预案次数,
    :param float issued_impl_number : 增发实施次数,
    :param float accu_ipo_proceeds : 增发累计募集资金总额,
    :param float acc_issue_vol : 增发股份数量,

    """
    
    headers = get_headers()
    url = base_url + 'get_neeq_issue_count'

    param = {'en_prod_code': en_prod_code, 'date_range': date_range, 'date_type': date_type, 'unit': unit, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_neeq_holder_num(en_prod_code = None, report_date = None, query_direction = None, unit = None, fields = None):
    """

    输入参数：
    :param str en_prod_code : 证劵代码
    :param str report_date : 申报日期
    :param str query_direction : 查询方向
    :param str unit : 单位
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 产品代码,
    :param str report_date : 申报日期,
    :param str query_direction : 查询方向,
    :param str sh_num : 股东总户数,
    :param float average_hold_sum : 户均持股数量,
    :param float average_hold_sum_proportion : 户均持股比例,
    :param float proportion_change : 相对上一报告期户均持股比例差值,
    :param float avg_hold_sum_gr_half_a_year : 户均持股数年增长率,
    :param float proportion_gr_half_a_year : 户均持股比例年增长率,

    """
    
    headers = get_headers()
    url = base_url + 'get_neeq_holder_num'

    param = {'en_prod_code': en_prod_code, 'report_date': report_date, 'query_direction': query_direction, 'unit': unit, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text

def get_neeq_holder_info(en_prod_code = None, end_date = None, serial_number = None, share_query_type = None, unit = None, fields = None):
    """

    输入参数：
    :param str en_prod_code : 证劵代码
    :param str end_date : 截止日期
    :param str serial_number : 股东序号
    :param str share_query_type : 证券类别
    :param str unit : 单位
    :param str fields : 字段集合

    输出参数：
    :param str prod_code : 产品代码,
    :param str end_date : 截止日期,
    :param str serial_number : 股东序号,
    :param str share_query_type : 证券类别,
    :param str stock_holder_name : 股东名称,
    :param str hold_vol : 持流通股总数（万股）,
    :param float pct_of_total_shares : 占总股本比例（%）,
    :param str share_character_statement : 股本性质,
    :param float hold_vols_top10_stockholders : 十大股东持股数量,
    :param float hold_vols_top10_fstockholders : 前十大流通股股东持股数量合计,
    :param float total_prop_top10_fstockholders : 前十大流通股股东持股比例合计,
    :param float total_prop_top10_stockholders : 十大股东持股比例,

    """
    
    headers = get_headers()
    url = base_url + 'get_neeq_holder_info'

    param = {'en_prod_code': en_prod_code, 'end_date': end_date, 'serial_number': serial_number, 'share_query_type': share_query_type, 'unit': unit, 'fields': fields}

    res = requests.post(url=url, headers=headers, data=json.dumps(param))

    if res.ok:
        return pickle.loads(res.content)

    return res.text


if __name__ == '__main__':
    set_token('abc')

    data = get_neeq_holder_info()
    # data = get_neeq_holder_num()
    # data = get_neeq_issue_count()
    # data = get_neeq_per_share_index()
    # data = get_neeq_share_stru()
    # data = get_neeq_dupont_analysis()
    # data = get_neeq_industry()
    # data = get_neeq_leader_num()
    # data = get_neeq_leader()
    # data = get_neeq_company()
    # data = get_neeq_basic()
    # data = get_star_companyprofile()
    # data = get_star_ipodeclare()
    # data = get_stock_main_business_indurstry()
    # data = get_stock_main_business_total()
    # data = get_stock_main_composition()
    # data = get_corporation_value()
    # data = get_q_financial_indicator()
    # data = get_deri_fin_indicators()
    # data = get_du_pont_analysis()
    # data = get_growth_capacity()
    # data = get_profitability()
    # data = get_per_share_index()
    # data = get_audit_opinion()
    # data = get_trading_parties()
    # data = get_main_composition()
    # data = get_performance_letters_q()
    # data = get_performance_letters()
    # data = get_performance_forecast()
    # data = get_financial_insu_qcashflow()
    # data = get_financial_secu_qcashflow()
    # data = get_financial_bank_qcashflow()
    # data = get_financial_gene_qcashflow()
    # data = get_financial_insu_qincome()
    # data = get_financial_secu_qincome()
    # data = get_financial_bank_qincome()
    # data = get_financial_gene_qincome()
    # data = get_financial_income()
    # data = get_accounting_data()
    # data = get_stock_key_indicator()
    # data = get_schedule_disclosure()
    # data = get_stock_industry_region_list()
    # data = get_stock_industry_compare()
    # data = get_stock_financial_industry_list()
    # data = get_stock_investor_detail()
    # data = get_stock_investor_statistics()
    # data = get_stock_org_rate()
    # data = get_stock_special_tradedate()
    # data = get_stock_share_holders(en_prod_code = '000001.SZ')
    # data = get_stock_asrighttransfer()
    # data = get_stock_asforecastabb()
    # data = get_stock_allotment(en_prod_code = '000001.SZ')
    # data = get_stock_additional_all(en_prod_code = '000001.SZ')
    # data = get_stock_additional(en_prod_code = '000001.SZ')
    # data = get_stock_dividend(en_prod_code = '000001.SZ')
    # data = get_margin_trade_total()
    # data = get_margin_trade_detail()
    # data = get_interval_margin_trading(en_prod_code = '000001.SZ')
    # data = get_margin_trading()
    # data = get_block_trade(start_date='2022-01-01', end_date='2023-02-01')
    # data = get_stock_pledge()
    # data = get_pledge_repo()
    # data = get_holder_increase(symbols = '000001.SZ')
    # data = get_holder_pledge(en_prod_code = '000001.SZ', trading_date='2023-02-01')
    # data = get_holder_num(en_prod_code = '000001.SZ', report_date='2023-02-01')
    # data = get_org_hold()
    # data = get_index_constituent()
    # data = get_industry_category(en_prod_code = '000001.SZ')
    # data = get_index_quote(en_prod_code = '000001.SZ', trading_date='2023-02-01')
    # data = get_stock_quote_daily_list(en_prod_code = '000001.SZ', begin_date='2023-02-01', end_date='2023-02-01')
    # data = get_quote_stocklist()
    # data = get_shszhk_change_top10()
    # data = get_shszhk_distribution(start_date='2023-02-01', end_date='2023-02-01')
    # data = get_shszhk_deal_top10(start_date='2023-02-01', end_date='2023-02-01')
    # data = get_shszhk_capitalflow(start_date='2023-02-01', end_date='2023-02-01')
    # data = get_stock_quote_minutes(en_prod_code = '000001.SZ', begin_date='2023-02-01', end_date='2023-02-01')
    # data = get_lh_stock()
    # data = get_lh_daily()
    # data = get_float_shareholder_top10(secu_code = '000001.SZ')
    # data = get_shareholder_top10(secu_code = '000001.SZ')
    # data = get_suspension_list(en_prod_code = '000001.SZ')
    # data = get_money_flow(en_prod_code = '000001.SZ')
    # data = get_stock_quote_yearly(en_prod_code = '000001.SZ')
    # data = get_stock_quote_monthly(en_prod_code = '000001.SZ')
    # data = get_stock_quote_weekly()
    # data = get_stock_quote_daily()
    # data = get_shszhk_stock_list()
    # data = get_st_stock_list()
    # data = get_stock_Info()
    # data = get_stock_list()
    # data = get_trading_calendar()
    # data = get_ipo_list()
    # data = get_company_profile()

    print(data)