from abc import ABCMeta, abstractmethod

class Base(metaclass=ABCMeta):
    @property
    def aa(self):
        print('aa')

    def __init__(self,df,start_date='', end_date=''):

        if start_date == '':
            start_date = df.index[0]  # 设置为df第一个日期
        if end_date == '':
            end_date = df.index[-1]  # 设置为df最后一个日期
        df = df.loc[start_date:end_date]

        self.df = df
        self.O = df['open']
        self.H = df['high']
        self.L = df['low']
        self.C = df['close']


    @abstractmethod
    def run(self):
        pass
