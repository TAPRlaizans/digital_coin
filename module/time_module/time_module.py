from datetime import datetime
import time

class Time_module:
    def get_current_timestamp():
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d-%H-%M")
        return timestamp
    
    def get_diff_time(time_start, time_end, uint="s"):
        diff_time = time_end - time_start
        if uint == "s":
            diff_time = diff_time  # 秒
        elif uint == "m":
            diff_time = diff_time / 60  # 分钟  
        elif uint == "h":
            diff_time = diff_time / 60 / 60  # 小时
            
if __name__ == "__main__":
    print(Time_module.get_current_timestamp())