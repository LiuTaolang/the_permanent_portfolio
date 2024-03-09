import akshare as ak
import pandas as pd

import tools_method as tm

class FundList():
    """基金清单类"""
    
    def __init__(self) -> None:
        """初始化 ETF,LOF,开放式,货币基金清单"""
        self.__update_flag = False
        self.__load_local_fund_list()

    def __load_local_fund_list(self):
        """加载本地基金清单"""
        self.__check_fund_list_update()
        if self.__update_flag:
            self.__update_fund_list()
        try:
            self.etf = pd.read_json('cache/etf.json', 
                                    dtype={'代码': str, '基金代码': str})
            self.lof = pd.read_json('cache/lof.json', 
                                    dtype={'代码': str, '基金代码': str})
            self.open = pd.read_json('cache/open.json', 
                                    dtype={'代码': str, '基金代码': str})
            self.money = pd.read_json('cache/money.json', 
                                    dtype={'代码': str, '基金代码': str})
        except:
            self.__update_fund_list()
            
    def __check_fund_list_update(self):
        """检查本地基金清单的最后修改日期是否为今天"""
        try:
            flag_etf = tm.check_update('cache/etf.json')
            flag_lof = tm.check_update('cache/lof.json')
            flag_open = tm.check_update('cache/open.json')
            flag_money = tm.check_update('cache/money.json')
        except FileNotFoundError:
            self.__update_flag = True
        else:
            self.__update_flag = max([flag_etf, flag_lof, flag_open, flag_money])

    def __update_fund_list(self):
        """通过 akshare 更新数据"""
        self.etf = ak.fund_etf_spot_em()          # ETF基金实时行情-东财，作ETF清单
        self.lof = ak.fund_lof_spot_em()          # LOF基金实时行情-东财，作LOF清单
        self.open = ak.fund_open_fund_daily_em()  # 开放式基金实时数据-东财，作开放式清单
        self.money = ak.fund_money_fund_daily_em()# 货币基金实时数据-东财，作货基清单
        self.__save_fund_list()

    def __save_fund_list(self):
        """保存数据到本地"""
        self.etf.to_json('cache/etf.json')
        self.lof.to_json('cache/lof.json')
        self.open.to_json('cache/open.json')
        self.money.to_json('cache/money.json')
        
if __name__=='__main__':
    fl = FundList()