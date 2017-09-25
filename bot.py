import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def command_start(bot, update):
    start_text = 'Привет'
    update.message.reply_text(start_text) 

def chat_bot(bot, update):
    chat_id = update.message.chat.id
    text = update.message.text
    update.message.reply_text(text)

def main():
    updater = Updater(settings.TELEGRAM_API_KEY)    
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, chat_bot))
    dp.add_handler(CommandHandler("start", command_start))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':  
    main()