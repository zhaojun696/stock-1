from xuangubao.base import session_factory
from sqlalchemy import text
import datetime
from xuangubao.kline_week import kline_week

if __name__ == '__main__':

    start_date = datetime.datetime(2020, 1, 1)
    end_date = datetime.datetime.now()

    session = session_factory()
    stock_list = session.execute(text("SELECT * FROM stock"))
    for stock in stock_list:
        lines = session.query(kline_week).filter(
            kline_week.code == stock['code'],
            kline_week.week <= start_date,
            kline_week.week <= end_date

        ).order_by(kline_week.week.desc()).all()

        if not lines:
            continue;

        for i in range(5):
            print(lines[i])

