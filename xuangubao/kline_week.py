import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, Integer, Numeric

Base = declarative_base()


class kline_week(Base):
    __tablename__ = "kline_week"
    id = Column(Integer, primary_key=True)
    code = Column(String(45))
    open = Column(Numeric)
    close = Column(Numeric)
    high = Column(Numeric)
    low = Column(Numeric)
    turnover_volume = Column(Numeric)
    turnover_ratio = Column(Numeric)
    ma5 = Column(Numeric)
    ma10 = Column(Numeric)
    ma20 = Column(Numeric)
    ma60 = Column(Numeric)
    week = Column(Date)
