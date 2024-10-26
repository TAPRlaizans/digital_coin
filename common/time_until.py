import time 
import datetime

class TimeUntil:
    @staticmethod
    def getTimestamp():
        return int(round(time.time() * 1000))
    
    @staticmethod
    def get_format_time(timestamp):
        dt_object = datetime.datetime.fromtimestamp(timestamp)
        return str(dt_object.strftime('%Y-%m-%d %H:%M:%S'))