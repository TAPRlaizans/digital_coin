import telegram
from telegram.ext import Application,Updater, MessageHandler, filters

# 替换为你的Telegram API凭证
TOKEN = '6797078510:AAF8COUltk3dhnZBIUOlDYbOGnQeViVULqs'

# 定义消息处理函数
def message_handler(update, context):
    message = update.message
    chat_id = message.chat_id
    text = message.text
    # 在这里编写你的逻辑，处理接收到的消息内容
    print(f"Received message in chat {chat_id}: {text}")

def main():
    # updater = Updater(token=TOKEN, use_context=True)
    updater = Application.builder().token(TOKEN).build()
    # dispatcher = updater.dispatcher

    # 添加消息处理程序
    message_handler_callback = MessageHandler(filters.TEXT  & filters.ChatType.GROUPS, message_handler)
    updater.add_handler(message_handler_callback)

    # 开始接收消息
    updater.run_polling()
    updater.idle()

if __name__ == '__main__':
    main() 