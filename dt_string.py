import locale
from datetime import datetime

# Use current system locale
locale.setlocale(locale.LC_TIME, '')

now = datetime.now()

# Locale-formatted date, but replace slashes with dashes
date_locale = now.strftime('%x').replace('/', '-').replace('\\', '-')
time_locale = now.strftime('%H-%M')

dt_string = f"{date_locale}_{time_locale}"