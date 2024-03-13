import akshare as ak
import pandas as pd

import tools_method as tm

class Fund():
    """基金类"""
    def __init__(self, code:str, fund_list:object) -> None:
        """初始化属性 code, update_flag"""
        self.code = code
        self.__update_flag = False
        self.__set_name_type(fund_list)
        self.__set_cls_index()
        self.__set_hfq_history()
        self.__set_bfq_history()
        self.__set_creation_date()

    def __set_name_type(self, fund_list):
        """设置基金类别"""
        code_index = {'etf': '代码', 'lof': '代码', 'open': '基金代码', 'money': '基金代码'}
        name_index = {'etf': '名称', 'lof': '名称', 'open': '基金简称', 'money': '基金简称'}
        query_data = {'etf': fund_list.etf, 'lof': fund_list.lof, 
                      'open': fund_list.open, 'money': fund_list.money}
        for k,v in query_data.items():
            try:
                self.name = v.loc[v[code_index[k]]==self.code, name_index[k]].iloc[0]
                self.type = k
                break
            except:
                continue
    
    def __reset_date_column_format(self, df):
        """重置日期列格式"""
        temp = {'etf': '日期', 'lof': '日期', 
                    'open': '净值日期', 'money': '净值日期'}
        dt_index = temp[self.type]
        df[dt_index] = pd.to_datetime(df[dt_index], format='%Y-%m-%d')
        df[dt_index] = df[dt_index].dt.strftime('%Y-%m-%d')
        return df

    def __reset_date_column_name(self, df):
        """重置日期列名"""
        if self.type in ['open', 'money']:
            return df.rename(columns={'净值日期': '日期'})
        else:
            return df

    def __set_cls_index(self):
        """设置历史数据中的收盘价索引"""
        cls_index = {'etf': '收盘', 'lof': '收盘', 
                     'open': '累计净值', 'money':'累计净值'}
        self.cls_index = cls_index[self.type]

    def __set_hfq_history(self):
        """获取基金后复权历史数据"""
        filename = f"cache/{self.code}_hfq.json"
        self.__check_update_status(filename)
        if self.__update_flag:
            self.__update_hfq_history(filename)
        else:
            self.hfq_hist = pd.read_json(filename)
            self.hfq_hist = self.__reset_date_column_name(self.hfq_hist)

    def __check_update_status(self, filename):
        try:
            self.__update_flag = tm.check_update(filename)
        except FileNotFoundError:
            self.__update_flag = True

    def __update_hfq_history(self, filename):
        """更新基金后复权历史数据"""
        if self.type=='etf':
            self.hfq_hist = ak.fund_etf_hist_em(symbol=self.code, 
                                                period="daily", adjust="hfq")
        elif self.type=='lof':
            self.hfq_hist = ak.fund_lof_hist_em(symbol=self.code, 
                                                period="daily", adjust="hfq")
        elif self.type=='open':
            self.hfq_hist = ak.fund_open_fund_info_em(symbol=self.code, 
                                                      indicator="累计净值走势")
        elif self.type=='money':
            self.hfq_hist = ak.fund_money_fund_info_em(fund=self.code)
        else:
            raise Exception(f"could not handle this type {self.type}!")
        self.hfq_hist = self.__reset_date_column_format(self.hfq_hist)
        self.hfq_hist.to_json(filename)
        self.hfq_hist = self.__reset_date_column_name(self.hfq_hist)

    def __set_bfq_history(self):
        """获取基金不复权历史数据"""
        filename = f"cache/{self.code}_bfq.json"
        self.__check_update_status(filename)
        if self.__update_flag:
            self.__update_bfq_history(filename)
        else:
            self.bfq_hist = pd.read_json(filename)
            self.bfq_hist = self.__reset_date_column_name(self.bfq_hist)

    def __update_bfq_history(self, filename):
        """更新基金不复权历史数据"""
        if self.type=='etf':
            self.bfq_hist = ak.fund_etf_hist_em(symbol=self.code, 
                                                period="daily", adjust="")
        elif self.type=='lof':
            self.bfq_hist = ak.fund_lof_hist_em(symbol=self.code, 
                                                period="daily", adjust="")
        elif self.type=='open':
            self.bfq_hist = ak.fund_open_fund_info_em(symbol=self.code, 
                                                      indicator="累计净值走势")
        elif self.type=='money':
            self.bfq_hist = ak.fund_money_fund_info_em(fund=self.code)
        else:
            raise Exception(f"could not handle this type {self.type}!")
        self.bfq_hist = self.__reset_date_column_format(self.bfq_hist)
        self.bfq_hist.to_json(filename)
        self.bfq_hist = self.__reset_date_column_name(self.bfq_hist)

    def __set_creation_date(self):
        """获取基金的成立日期"""
        self.creation_date = self.hfq_hist['日期'].iloc[0]
    
