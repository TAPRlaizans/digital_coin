import os
import sys
from loguru import logger
from enum import Enum
from enum import Enum
from common.time_helper import TimeHelper

class LogLevel(str, Enum):
    Debug = 'DEBUG'
    Info = 'INFO'
    Warn = 'WARNING'
    Error = 'ERROR'

class Logger:
    PATH_LOG_FOLDER = '.'
    FILENAME_LOG = 'app'

    @staticmethod
    def init(
        path_folder, 
        filename, 
        level = LogLevel.Debug,
        rotation = '00:00',# 日志分片: 按 时间段/文件大小 切分日志. 例如 ["500 MB" | "12:00" | "1 week"]
        retention = '30 days'# 日志保留的时间
        ):
        if not os.path.exists(path_folder):
            os.mkdir(path_folder)
        Logger.PATH_LOG_FOLDER = path_folder
        Logger.FILENAME_LOG = filename
        log_file = os.path.join(Logger.PATH_LOG_FOLDER, Logger.FILENAME_LOG + '.log')

        # ref: https://github.com/Delgan/loguru#ready-to-use-out-of-the-box-without-boilerplate
        logger.remove(handler_id=None) 
        level_str = level
        if isinstance(level, LogLevel):
            level_str = level.value
        logger.add(
            log_file,
            level=level_str,
            encoding='utf-8',
            rotation=rotation,#'16 MB',#00:00
            retention=retention,#"7 days",
            enqueue=True,
            backtrace=True,
            diagnose=True,
            format="[{time:YYYY-MM-DD HH:mm:ss}] [{level}] {message} [{module}.{function}]({file}:{line})"
        )
        logger.add(
            sys.stdout,
            level=level_str,
            colorize=True,
            enqueue=True,
            backtrace=True,
            diagnose=True,
            format="<green>[{time:YYYY-MM-DD HH:mm:ss}]</green> <level>[{level}]</level> {message} <blue>[{module}.{function}]({file}:{line})</blue>"
        )
        logger.info('=================----------------app start----------------=================')

def funcRecorder(func):
    def wrapper(*args,**kwargs):
        logger.info(f"{func.__name__} F-ENTER")
        t_enter = TimeUntil.getTimestamp()
        ret = func(*args,**kwargs)
        logger.info(f"{func.__name__} F-EXIT, span {TimeUntil.getTimestamp() - t_enter} ms")
        return ret
    return wrapper


if __name__ == '__main__':
    @logger.catch()
    def testCrash():
        logger.info('hey')
        a = 1/0
    @funcRecorder
    def testFunc():
        print('test')

    testFunc()
    testCrash()