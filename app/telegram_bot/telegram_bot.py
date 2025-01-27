import re
import os
import sys
import json
import time
import shutil
import pprint
from loguru import logger
# from googletrans import Translator
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
PARENT_PARENT_DIR = os.path.dirname(PARENT_DIR)
PARENT_PARENT_PARENT_DIR = os.path.dirname(PARENT_PARENT_DIR)
sys.path.append(BASE_DIR)
sys.path.append(PARENT_DIR)
sys.path.append(PARENT_PARENT_DIR)
sys.path.append(PARENT_PARENT_PARENT_DIR)

from common.time_helper import TimeHelper as th
from common.json_helper import JsonHelper as jh
from common.logger import Logger, LogLevel 
from common.file_helper import FileHelper as fh
from common.math_helper import MathHelper as mh
from common.excle_helper import ExcleHelper as eh
from common.request_helper import RequestHelper as rh


if __name__ == "__main__":
    obj_key_bot_api_token = jh.read_json_file_to_object("./key_bot_api_token.json")
    obj_key_command = jh.read_json_file_to_object("./key_command.json")

    logger.info(obj_key_bot_api_token)
    logger.info(obj_key_command)

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = '你好~我是一个bot'
        await context.bot.send_message(chat_id=update.effective_chat.id,text=text)

    async def do_sexy(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = '哥哥，你可真好，太喜欢你啦，今天想要那种风格的呢？'
        await context.bot.send_message(chat_id=update.effective_chat.id,text=text)

    #设置回调函数
    start_handler = CommandHandler('start', start)
    start_handler = CommandHandler('do_sexy', do_sexy)

    TOKEN=obj_key_bot_api_token["info_monitoringBot"]
    application = ApplicationBuilder().token(TOKEN).build()
    # 注册 handler
    application.add_handler(start_handler)
    # run!
    application.run_polling()
    pass