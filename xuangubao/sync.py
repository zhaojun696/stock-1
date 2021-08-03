import datetime

from xuangubao.api import get_kline
from xuangubao.base import session_factory
from xuangubao.kline import kline
from xuangubao.kline_week import kline_week
from sqlalchemy.sql import text


def sync_day():

    session = session_factory()
    stock_list = session.execute(text("select * from stock where code "))

    for stock in stock_list:

        a=session.execute(text("select max(day) from kline_day where code={code}".format(code=stock['code'])))
        print(a)
        code = stock['code'] + '.' + stock['sse']
        data = get_kline(code)

        for item in data[code]['lines']:
            kline_entity = kline(
                open=item[0], code=stock['code'],
                close=item[1], high=item[2], low=item[3], turnover_volume=item[7],
                turnover_ratio=item[15], ma5=item[11], ma10=item[12], ma20=item[13], ma60=item[14],
                week=datetime.datetime.fromtimestamp(item[9])
            )
            session.add(kline_entity)
            session.commit()
            print(data)



pass


def sync_week():
    pass


if __name__ == '__main__':
    sync_day()