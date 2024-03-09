import datetime
import json

from fund_list import FundList
from fund import Fund
import tools_method as tm

fl = FundList()
portfolio_path = 'cache/portfolio.json'
try:
    with open(portfolio_path, 'r') as f:
        portfolio_code = json.load(f)
except FileNotFoundError:
    portfolio_code = {'股票基金': '', '黄金基金': '', '长债基金': '', '货币基金': ''}
    with open(portfolio_path, 'w') as f:
        json.dump(portfolio_code, f)

try:
    stock_fund = Fund(code=portfolio_code['股票基金'], fund_list=fl)
    gold_fund = Fund(code=portfolio_code['黄金基金'], fund_list=fl)
    bond_fund = Fund(code=portfolio_code['长债基金'], fund_list=fl)
    cash_fund = Fund(code=portfolio_code['货币基金'], fund_list=fl)
except:
    raise Exception(f"请检查({portfolio_path})里的基金代码是否正确({portfolio_code})")

start_date = tm.set_start_date([stock_fund, gold_fund, bond_fund, cash_fund])
end_date = datetime.datetime.today()
