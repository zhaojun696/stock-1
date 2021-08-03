from .base_strategey import Base
from .func_TDX import *
class WeekConsecutiveCross(Base):
    def run(self):
        pass
        # O = self.df['open']
        # H = self.df['high']
        # L = self.df['low']
        # C = self.df['close']
        # N=10,
        #
        #
        # print(self.df)
        #
        # a=REF(((HHV(H,N)-LLV(L,N))/LLV(L,N)),1)<=(n1/100) and REF(v,1)
        #
        # # a=COUNT(C > MA(C, 10), 1)
        # print(a)