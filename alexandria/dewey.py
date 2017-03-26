import os
import sys
import pandas as pd

sys.path.append('%s/../' % os.path.dirname(__file__))

from utils.date import date_ymd
from utils.fileSys import makeDir

HEADERS = ['Publisher', 'UPC', 'DCD', 'ISBN', 'Issue', 'Date', 'Copies']
INDICES = ['Publisher', 'UPC', 'Issue']


def cold_store(date, df):
    path = get_day_csv(day)
    df.to_csv(path)


def get_day_csv(date):
    year, month, day = date_ymd
    path =  os.path.join(
        os.path.dirname(__file__),
        'storage',
        year,
        month,
        day + '.csv')
    makeDir(path)
    return path


def start_today():
    path = get_today_csv()
    if os.path.exists(path):
        raise Exception('Today file still exists! Someone needs to export!')
    with open(path, 'w') as fo:
        pass
    return


def get_today_csv():
    return os.path.join(os.path.dirname(__file__), 'today.csv')


def append_today(df):
    path = get_today_csv()
    df_str = df.to_csv(None, header=False)
    with open(path, 'a') as fa:
        fa.write(df_str)


def today_store():
    pass
