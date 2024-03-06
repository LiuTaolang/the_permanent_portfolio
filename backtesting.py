import akshare as ak
import pandas as pd
import datetime

def get_fund_info(type):
    """获取用户选定的基金信息"""
    find_code = input(f"输入你选择的({type})代码：").strip(' ')
    index_diff = {'etf':['代码', '名称'], 'lof': ['代码', '名称'], 
                  'open': ['基金代码', '基金简称'], 'money': ['基金代码', '基金简称']}
    for k,v in fund_list.items():
        try:
            choice = v.loc[v[index_diff[k][0]]==find_code, index_diff[k][1]].iloc[0]
            fund_type, choice = confirm_fund(choice, type, k)
            break
        except:
            continue
    while choice=='':
        find_code, choice, fund_type = get_fund_info(type)
    return [find_code, choice, fund_type]

def confirm_fund(choice, type, k):
    """让用户确认查询到的基金是否准确"""
    flag = input(f"({choice})是您选中的({type})吗？Y/N:")
    if flag=='y' or flag=='Y':
        return k, choice
    else:
        return '', ''

def get_history_data(symbol, type):
    """获取用户选定基金的历史数据"""
    if type=='etf':
        return ak.fund_etf_hist_em(symbol=symbol, period="daily", 
                                   start_date="20000101", end_date=yesterday, adjust="hfq")
    elif type=='lof':
        return ak.fund_lof_hist_em(symbol=symbol, period="daily", 
                                   start_date="20000101", end_date=yesterday, adjust="hfq")
    elif type=='open':
        return ak.fund_open_fund_info_em(symbol=symbol, indicator="累计净值走势")
    elif type=='money':
        return ak.fund_money_fund_info_em(fund=symbol)
    else:
        raise Exception(f"could not handle this type {type}!")

def get_yesterday():
    """获取昨天的日期"""
    today = datetime.date.today()
    return today + datetime.timedelta(-1)

yesterday = str(get_yesterday()).replace('-', '')
portfolio = {'股票基金': {}, '黄金基金': {}, '长债基金': {}, '货币基金': {}}
fund_list = {'etf':'', 'lof':'', 'open':'', 'money':''}

fund_list['etf'] = ak.fund_etf_spot_em()  # ETF基金实时行情-东财，作ETF清单
fund_list['lof'] = ak.fund_lof_spot_em() # LOF基金实时行情-东财，作LOF清单
fund_list['open'] = ak.fund_open_fund_daily_em() # 开放式基金实时数据-东财，作开放式清单
fund_list['money'] = ak.fund_money_fund_daily_em() # 货币基金实时数据-东财，作货基清单

for k,v in portfolio.items():
    v['code'], v['name'], v['type'] = get_fund_info(k)
    v['history_hfq'] = get_history_data(v['code'], v['type'])
    print(f"code {v['code']}")
    print(f"name {v['name']}")
    print(f"type {v['type']}")
    print(v['history_hfq'])

# for k,v in portfolio.items():