import datetime as dt

def date_ymd(date):
    date = str(date)
    return date[:4], date[4:6], date[6:]

def today():
    fmt_str = "{}{:02d}{:02d}"
    t = dt.date.today()
    return fmt_str.format(t.year, t.month, t.day)
