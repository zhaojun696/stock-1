import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, Integer, Numeric

Base = declarative_base()


class zixuan(Base):
    __tablename__ = "zixuan"
    id = Column(Integer, primary_key=True)
    code = Column(String(45))
    weight = Column(Numeric)
    hot_rel_percent = Column(Numeric)
