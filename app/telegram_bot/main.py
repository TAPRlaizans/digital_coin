# from telethon.sync import TelegramClient
# from telethon.tl.functions.messages import GetHistoryRequest
# from telethon.tl.types import PeerChannel

# # 输入你的API ID和Hash
# api_id = 'YOUR_API_ID'
# api_hash = 'YOUR_API_HASH'

# # 输入你的手机号码（带国际区号）
# phone_number = 'YOUR_PHONE_NUMBER'

# client = TelegramClient(phone_number, api_id, api_hash)

# async def main():
#     await client.start()
    
#     # 输入你想要导出消息的群组的用户名或ID
#     group = 'GROUP_USERNAME_OR_ID'
    
#     # 获取群组实体
#     group_entity = await client.get_entity(group)
    
#     # 获取群组消息
#     messages = []
#     offset_id = 0
#     limit = 100
    
#     while True:
#         history = await client(GetHistoryRequest(
#             peer=group_entity,
#             offset_id=offset_id,
#             offset_date=None,
#             add_offset=0,
#             limit=limit,
#             max_id=0,
#             min_id=0,
#             hash=0
#         ))
        
#         if not history.messages:
#             break
        
#         messages.extend(history.messages)
#         offset_id = history.messages[-1].id
        
#     # 将消息写入文件
#     with open('messages.txt', 'w', encoding='utf-8') as f:
#         for message in messages:
#             f.write(f'{message.date} - {message.sender_id}: {message.message}\n')
    
#     print(f'Total messages exported: {len(messages)}')

# with client:
#     client.loop.run_until_complete(main())

# import datetime
# import time
# import telebot
# import ccxt
# import pandas as pd
# import pandas_ta as ta

# exchange = ccxt.poloniex({'enableRateLimit': True})
# exchange.load_markets()

# API_KEY = "6797078510:AAF8COUltk3dhnZBIUOlDYbOGnQeViVULqs"
# bot = telebot.TeleBot(API_KEY)

# @bot.message_handler(commands=['start', 'help'])
# def handle_start_help(message):
#     print(message.chat.id)
#     bot.reply_to(message, "What's up")

# bot.polling()

import telebot

API_KEY = "6797078510:AAF8COUltk3dhnZBIUOlDYbOGnQeViVULqs"
GROUP_CHAT_ID = "BlockBeats"  # 替换为你的群组ID
SPECIFIC_USER_ID = "6292438463"  # 替换为你想记录的用户ID
bot = telebot.TeleBot(API_KEY)

# 处理 /start 和 /help 命令
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.reply_to(message, "What's up")

# 处理所有消息
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    with open('messages.txt', 'a', encoding='utf-8') as f:
        f.write(f'{message.date} - {message.chat.id} - {message.from_user.username}: {message.text}\n')
    print(f'Message from {message.chat.id} - {message.from_user.username}: {message.text}')

@bot.message_handler(func=lambda message: message.chat.id == int(GROUP_CHAT_ID))
def handle_group_messages(message):
    if message.content_type == 'text' and "通知" in message.text:  # 根据具体通知内容调整条件
        with open('group_notifications.txt', 'a', encoding='utf-8') as f:
            f.write(f'{message.date} - {message.chat.id} - {message.from_user.username}: {message.text}\n')
        print(f'Notification from {message.chat.id} - {message.from_user.username}: {message.text}')

@bot.message_handler(func=lambda message: message.from_user.id == int(SPECIFIC_USER_ID))
def handle_user_messages(message):
    with open('user_messages.txt', 'a', encoding='utf-8') as f:
        f.write(f'{message.date} - {message.chat.id} - {message.from_user.username} ({message.from_user.id}): {message.text}\n')
    print(f'Message from {message.chat.id} - {message.from_user.username} ({message.from_user.id}): {message.text}')

bot.polling()

