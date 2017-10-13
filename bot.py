import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime
import telegram
import currency
import feedparser
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
    first_name = user_chat.first_name
    last_name = user_chat.last_name
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
    logging.info('Пользователь {}: {}'.format(update.message.chat.username, text))
    if text == 'В главное меню':
        default_keyboards(bot, chat_id)
    elif text == 'Подписки':
        keyboards_menu(bot, chat_id, '1')
    elif text == 'Курсы валют':
        keyboards_menu(bot, chat_id, '2')
    elif text == 'РБК':
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
            keyboard = {'menu': [['РБК', 'Трэш', 'В главное меню']], 'text': 'Подписки'}
        elif str(keyboard_id) == '2':
            keyboard = {'menu': [['Доллар', 'Евро', 'В главное меню']], 'text': 'Курсы валют'}
        elif str(keyboard_id) == '3on':
            keyboard = {'menu': [['Включить РБК', 'В главное меню']], 'text': 'Управление подпиской на РБК'}
        elif str(keyboard_id) == '3off':
            keyboard = {'menu': [['Выключить РБК', 'В главное меню']], 'text': 'Управление подпиской на РБК'}
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


def callback_news_minute(bot, job):
    parse_from_rss = feedparser.parse(settings.RBC_RSS)
    news_in_text = 5
    news = list()
    for news_counter in range(0, news_in_text):
        news.append(parse_from_rss.entries[news_counter].link)

    if (settings.check_parse_links[0] not in news) and (settings.check_parse_links[1] not in news):
        settings.check_parse_links[0] = news[0]
        settings.check_parse_links[1] = news[1]
        text = ''
        subscribers = work.subscribers_list('РБК')
        subscribers.append('@rbknews1')
        for news_counter in range(0, news_in_text):
            text = text + parse_from_rss.entries[news_counter].title + '\n' + news[news_counter] + '\n'
        for sub in subscribers:
            bot.send_message(chat_id=sub,
                             text=text)

    with open('logs/sendnews.txt', "a") as local_file:
        local_file.write('{}: link1: {}\n'.format(datetime.now().strftime('%Y.%m.%d %H.%M.%S'), settings.check_parse_links[0]))
        local_file.write('{}: link2: {}\n'.format(datetime.now().strftime('%Y.%m.%d %H.%M.%S'), settings.check_parse_links[1]))
        local_file.write('{}: {}\n'.format(datetime.now().strftime('%Y.%m.%d %H.%M.%S'), 'repeat'))

def main():
    updater = Updater(settings.TELEGRAM_API_KEY)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, chat_bot))
    dp.add_handler(CommandHandler("start", command_start))

    j = updater.job_queue
    job_minute = j.run_repeating(callback_news_minute, interval=60, first=0)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logging.info('Bot started')
    main()
