import datetime

from functools import reduce
import pandas as pd

from fund_list import FundList
from fund import Fund
import tools_method as tm

fl = FundList()
portfolio_path = 'cache/portfolio.json'
portfolio_code = tm.init_portfolio_code(portfolio_path)

try:
    stock_fund = Fund(code=portfolio_code['股票基金'], fund_list=fl)
    gold_fund = Fund(code=portfolio_code['黄金基金'], fund_list=fl)
    bond_fund = Fund(code=portfolio_code['长债基金'], fund_list=fl)
    cash_fund = Fund(code=portfolio_code['货币基金'], fund_list=fl)
except:
    raise Exception(f"请检查({portfolio_path})里的基金代码是否正确({portfolio_code})")

dfs = [stock_fund, gold_fund, bond_fund, cash_fund]

start_date = tm.set_start_date(dfs)
end_date = datetime.datetime.today()
