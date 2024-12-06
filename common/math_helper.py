
from loguru import logger
from common.logger import Logger, LogLevel 

class MathHelper():
    @staticmethod
    def check_update(arr):
        if len(arr) < 2:
            logger.info(f"最新的数据: {arr[-1]} ")
            return
        
        new_element = arr[-1]  
        previous_elements = arr[:-1]  
        last_element = previous_elements[-1]  
        
        if new_element > last_element:
            logger.info(f"数据元素个数增加: {new_element}, 请检查! last element is {last_element}, 增加个数是 {new_element - last_element}")
        elif new_element < last_element:
            logger.info(f"数据元素个数减少: {new_element}, 请检查! last element is {last_element}, 减少个数是 {last_element - new_element}")

    