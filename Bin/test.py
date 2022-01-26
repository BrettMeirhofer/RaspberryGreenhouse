import datetime
import pytz

now = datetime.datetime.now()
aware = datetime.datetime.now(tz=pytz.UTC)
unware = pytz.utc.localize(now)

print(now)
print(aware)
print(unware)
