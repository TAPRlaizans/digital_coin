from datetime import datetime
import time

class Time_module:
    def get_current_timestamp():
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d-%H-%M")
        return timestamp

if __name__ == "__main__":
    print(Time_module.get_current_timestamp())