import time 
import datetime

class TimeUntil:
    @staticmethod
    def get_time_stamp_format():
        current_time = time.localtime()
        timestamp = time.strftime("%Y-%m-%d_%H_%M_%S", current_time)
        return timestamp
    
    @staticmethod
    def sleep_s(seconds):
        time.sleep(seconds)

    @staticmethod
    def get_time_stamp():
        return int(round(time.time() * 1000))
    
    @staticmethod
    def get_format_time(timestamp):
        dt_object = datetime.datetime.fromtimestamp(timestamp)
        return str(dt_object.strftime('%Y-%m-%d %H:%M:%S'))