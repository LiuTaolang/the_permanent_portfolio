import os
import datetime
import json

import akshare as ak

def __get_last_modified_time(filename):
    mtime = os.stat(filename).st_mtime
    mtime_dt = datetime.date.fromtimestamp(mtime)
    return mtime_dt

def check_update(filename):
    mtime_dt = __get_last_modified_time(filename)
    return True if mtime_dt < datetime.date.today() else False

def __get_fund_establishment_date(portfolio_list):
    """获取四个基金的最晚成立时间"""
    date_list = []
    for i in portfolio_list:
        date_list.append(i.creation_date)
    return max(date_list)

def set_start_date(portfolio_list):
    """让用户设置回测组合起始日"""
    est_date = __get_fund_establishment_date(portfolio_list)
    temp_date = input(f"请输入组合开始日期(晚于默认值{est_date}, yyyy-mm-dd):")
    try:
        datetime.datetime.strptime(temp_date, '%Y-%m-%d')
    except ValueError:
        print(f"输入的日期格式不正确, 以基金创建日期{est_date}为起始日进行回测。")
        return est_date
    if temp_date < est_date:
        print(f"输入日期早于基金创建日期{est_date}, 以基金创建日期进行回测。")
        return est_date
    else:
        print(f"以{temp_date}为起始日，创建组合回测。")
        return temp_date
    
def init_portfolio_code(portfolio_path):
    """初始化永久组合中各类基金的代码"""
    try:
        with open(portfolio_path, 'r') as f:
            portfolio_code = json.load(f)
    except FileNotFoundError:
        portfolio_code = {'股票基金': '', '黄金基金': '', '长债基金': '', '货币基金': ''}
        with open(portfolio_path, 'w') as f:
            json.dump(portfolio_code, f)  
    return portfolio_code
                      