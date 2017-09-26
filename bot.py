import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram

def command_start(bot, update):
    chat_id = update.message.chat.id
    start_text = 'Привет'
    update.message.reply_text(start_text)
    default_keyboards(bot, chat_id)

def chat_bot(bot, update):
    chat_id = update.message.chat.id
    text = update.message.text
    if text == 'В главное меню':
        defaul_keyboards(bot, chat_id)
    elif text == 'Подписки':
        keyboards_menu(bot, chat_id, '1')
    elif text == 'Курсы валют':
        keyboards_menu(bot, chat_id, '2')
    else:
        update.message.reply_text(text)

def keyboards_menu(bot, chat_id, keyboard_id=0):
    if str(keyboard_id) != '0':
        if str(keyboard_id) == '1':
            keyboard = {'menu':[['РБК', 'Трэш', 'В главное меню']], 'text':'Подписки'}
        elif str(keyboard_id) == '2':
            keyboard = {'menu':[['Доллар', 'Евро', 'В главное меню']], 'text':'Курсы валют'}
        reply_markup = telegram.ReplyKeyboardMarkup(keyboard['menu'], resize_keyboard=True)
        bot.send_message(chat_id=chat_id, 
                    text=keyboard['text'], 
                    reply_markup=reply_markup)
    else:
        keyboard = [['Подписки', 'Курсы валют']]
        return keyboard

def default_keyboards(bot, chat_id):
    reply_markup = telegram.ReplyKeyboardMarkup(keyboards_menu(bot, chat_id), resize_keyboard=True)
    bot.send_message(chat_id=chat_id,
                    text='Вы в главном меню',
                    reply_markup=reply_markup)

def main():
    updater = Updater(settings.TELEGRAM_API_KEY)    
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, chat_bot))
    dp.add_handler(CommandHandler("start", command_start))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':  
    main()
