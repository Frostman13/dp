import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import currency
from user_db import work
# Подключаем лог
import logging
logging.basicConfig(format='%(name)s - %(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='logs/bot.log'
                    )


def command_start(bot, update):
    user_chat = update.message.chat
    chat_id = user_chat.id
    first_name =  user_chat.first_name
    last_name =  user_chat.last_name
    username = user_chat.username

    add_user = work.user_db_add_user(chat_id, first_name, last_name, username)
    logging.info('Попытка добавления пользователя {}: {}'.format(chat_id, add_user))
    update.message.reply_text('Привет')
    logging.info('Пользователь {} {} ({} {}) нажал /start'.format(chat_id, first_name, last_name, username))
    default_keyboards(bot, chat_id)

def chat_bot(bot, update):
    # print(update)
    chat_id = update.message.chat.id
    text = update.message.text
    logging.info('Пользователь {}: {}'.format(update.message.chat.username,text))
    if text == 'В главное меню':
        default_keyboards(bot, chat_id)
    elif text == 'Подписки':
        keyboards_menu(bot, chat_id, '1')
    elif text == 'Курсы валют':
        keyboards_menu(bot, chat_id, '2')
    elif text == 'РБК':  # дописать if на наличие подписки
        if work.subscription_check(chat_id, 'РБК') is False:
            keyboards_menu(bot, chat_id, '3on')
        else:
            keyboards_menu(bot, chat_id, '3off')
    elif text == 'Включить РБК':
        add_sub = work.subscriptions_db_add_sub(chat_id, 'РБК', True)
        update.message.reply_text('Подписка включена')
        keyboards_menu(bot, chat_id, '3off')
    elif text == 'Выключить РБК':
        add_sub = work.subscriptions_db_add_sub(chat_id, 'РБК', False)
        update.message.reply_text('Подписка выключена')
        keyboards_menu(bot, chat_id, '3on')
    elif str.lower(text) in currency.CURRENCY_CODES:
        update.message.reply_text(currency.get_currency_rates(text))
    else:
        update.message.reply_text(text)

def keyboards_menu(bot, chat_id, keyboard_id=0):
    if str(keyboard_id) != '0':
        if str(keyboard_id) == '1':
            keyboard = {'menu':[['РБК', 'Трэш', 'В главное меню']], 'text':'Подписки'}
        elif str(keyboard_id) == '2':
            keyboard = {'menu':[['Доллар', 'Евро', 'В главное меню']], 'text':'Курсы валют'}
        elif str(keyboard_id) == '3on':
            keyboard = {'menu':[['Включить РБК', 'В главное меню']], 'text':'Управление подпиской на РБК'}
        elif str(keyboard_id) == '3off':
            keyboard = {'menu':[['Выключить РБК', 'В главное меню']], 'text':'Управление подпиской на РБК'}
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
    logging.info('Bot started')
    main()
