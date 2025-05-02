import locale
from datetime import datetime

def get_safe_dt_string():

    # Use current system locale
    locale.setlocale(locale.LC_TIME, '')
    now = datetime.now()
    date_locale = now.strftime('%x').replace('/', '-').replace('\\', '-')
    time_locale = now.strftime('%H-%M')
    return f"{date_locale}_{time_locale}"