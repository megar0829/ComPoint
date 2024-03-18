from datetime import datetime
import pytz

print(datetime.today().strftime('%d'))
print(datetime.now(pytz.utc).strftime('%d'))