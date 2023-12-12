from datetime import datetime
import pytz

def convert(time_string: str):
    try:
        utc_time = datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        utc_time = datetime.strptime(time_string, "%Y-%m-%d %H:%M")
    swedish_time_zone = pytz.timezone("Europe/Stockholm")
    swedish_time = utc_time.replace(tzinfo=pytz.utc).astimezone(swedish_time_zone)
    return swedish_time.strftime("%Y-%m-%d %H:%M")
