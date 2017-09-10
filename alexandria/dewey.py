import os
import sys
import pandas as pd

sys.path.append('%s/../' % os.path.dirname(__file__))

from utils.date import date_ymd, today
from utils.fileSys import makeDir
from utils.pandas_util import condense

HEADERS = ['UPC', 'Issue', 'Publisher', 'Date', 'Copies']  # 'DCD', 'ISBN'
INDICES = ['UPC', 'Issue', 'Publisher']


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


def export_today():
    """ Condense duplicates over the day, and save to cold store. """
    df = condense(pd.read_csv(get_today_csv()), 'Copies')
    path = get_day_csv(today())
    if os.path.exists(path):
        raise Exception("This day was already exported! Delete the old one, or don't run this.")
    df.to_csv(path)
