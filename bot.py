import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from time import mktime
from datetime import datetime
from pytz import timezone
import telegram
import currency
import feedparser
import requests
import json
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

    add_user = work.users_db_add_user(chat_id, first_name, last_name, username)
    logging.info('Попытка добавления пользователя {}: {}'.format(chat_id, add_user))
    update.message.reply_text('Привет')
    logging.info('Пользователь {} {} ({} {}) нажал /start'.format(chat_id, first_name, last_name, username))
    default_keyboards(bot, chat_id)


def google_short_url(url):
    post_url = 'https://www.googleapis.com/urlshortener/v1/url?key={}'.format(settings.GOOGLE_SHORTENER_API_KEY)
    input_url = {'longUrl': url}
    headers = {'content-type': 'application/json'}
    response = requests.post(post_url, data=json.dumps(input_url), headers=headers)
    short_url = response.json()['id']
    return short_url


def get_time_diff(local_timezone):
    now = datetime.utcnow()
    local_tz = timezone(local_timezone)
    utc_tz = timezone('UTC')
    delta = utc_tz.localize(now) - local_tz.localize(now)
    return delta


def chat_bot(bot, update):
    # print(update)
    chat_id = update.message.chat.id
    text = update.message.text
    today = datetime.now(timezone('Europe/Moscow')).replace(tzinfo=None).strftime("%d.%m.%Y")
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
    elif text == 'Последние новости РБК':
        rbc_last_news(bot, 5, chat_id)
    elif text == 'Включить РБК':
        add_sub = work.subscriptions_db_add_sub(chat_id, 'РБК', True)
        update.message.reply_text('Подписка включена')
        keyboards_menu(bot, chat_id, '3off')
    elif text == 'Выключить РБК':
        add_sub = work.subscriptions_db_add_sub(chat_id, 'РБК', False)
        update.message.reply_text('Подписка выключена')
        keyboards_menu(bot, chat_id, '3on')
    elif str.lower(text) in currency.CURRENCY_CODES:
        update.message.reply_text(currency.get_currency_rates(text, today))
    else:
        update.message.reply_text(text)


def keyboards_menu(bot, chat_id, keyboard_id=0):
    if str(keyboard_id) != '0':
        if str(keyboard_id) == '1':
            keyboard = {'menu': [['РБК', 'Трэш', 'В главное меню']], 'text': 'Подписки'}
        elif str(keyboard_id) == '2':
            keyboard = {'menu': [['Доллар', 'Евро', 'В главное меню']], 'text': 'Курсы валют'}
        elif str(keyboard_id) == '3on':
            keyboard = {'menu': [['Включить РБК', 'Последние новости РБК', 'В главное меню']], 'text': 'Управление подпиской на РБК'}
        elif str(keyboard_id) == '3off':
            keyboard = {'menu': [['Выключить РБК', 'Последние новости РБК', 'В главное меню']], 'text': 'Управление подпиской на РБК'}
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


def callback_collect_news(bot, job):
    parse_from_rss = feedparser.parse(settings.RBC_RSS)
    for news_counter in reversed(range(0, 5)):
        news_link = parse_from_rss.entries[news_counter].link
        if news_link not in settings.check_rbc_links:
            title = 'РБК'
            news_time = datetime.fromtimestamp(mktime(parse_from_rss.entries[news_counter].published_parsed)) + get_time_diff('Europe/Moscow')
            date = '{}-{:02d}-{:02d}'.format(news_time.year, news_time.month, news_time.day)
            time = '{:02d}:{:02d}'.format(news_time.hour, news_time.minute)
            news_title = parse_from_rss.entries[news_counter].title
            news_short_link = google_short_url(news_link)
            add_news = work.news_db_add_news(title, date, time, news_title, news_link, news_short_link)
        settings.check_rbc_links[news_counter] = news_link


def rbc_last_news(bot, counter, chat_id):
    text = ''
    last_news = work.last_news(5, 'РБК')
    for news in last_news:
        text = text + news.news_title + '\n' + news.news_short_link + '\n'
    if text != '':
        bot.send_message(chat_id=chat_id,
                         text=text, disable_web_page_preview=True)


def sent_news(bot, job):
    unsent_news = work.unsent_news_list('РБК')
    news_counter = len(unsent_news)
    now_time = datetime.now().strftime('%Y.%m.%d %H.%M.%S')
    if news_counter > 5:
        unsent_news = unsent_news[0:5]
    if news_counter > 4:
        text = ''
        subscribers = work.subscribers_list('РБК')
        subscribers.append('@rbknews1')
        for news in unsent_news:
            text = text + news.news_title + '\n' + news.news_short_link + '\n'
        for sub in subscribers:
            bot.send_message(chat_id=sub,
                             text=text, disable_web_page_preview=True)
        work.mark_sent_news(unsent_news)
        with open('logs/sendnews.txt', "a") as local_file:
            local_file.write('{}: News sent to {}\n'.format(now_time, subscribers))
    else:
        with open('logs/sendnews.txt', "a") as local_file:
            local_file.write('{}: Not enough news\n{}\n'.format(now_time, unsent_news))


def main():
    updater = Updater(settings.TELEGRAM_API_KEY)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, chat_bot))
    dp.add_handler(CommandHandler("start", command_start))

    j = updater.job_queue
    job_collect_news = j.run_repeating(callback_collect_news, interval=180, first=0)
    job_sent_news = j.run_repeating(sent_news, interval=180, first=0)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logging.info('Bot started')
    main()
