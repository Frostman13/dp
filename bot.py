import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from time import mktime
from datetime import datetime
from pytz import timezone
import telegram
import currency
from bot_keyboards import keyboards_menu_buttons, keyboard_sub_switch
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
    logging.info('Попытка добавления пользователя {}: {}'
                 .format(chat_id, add_user))
    update.message.reply_text('Привет')
    logging.info('Пользователь {} {} ({} {}) нажал /start'
                 .format(chat_id, first_name, last_name, username))
    keyboards_menu(bot, chat_id)


def google_short_url(url):
    post_url = ('https://www.googleapis.com/urlshortener/v1/url?key={}'
                .format(settings.GOOGLE_SHORTENER_API_KEY))
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
    chat_id = update.message.chat.id
    text = update.message.text
    today = datetime.now(timezone('Europe/Moscow')).replace(tzinfo=None).strftime("%d.%m.%Y")
    logging.info('Пользователь {}: {}'.format(update.message.chat.username, text))

    if text == 'В главное меню':
        keyboards_menu(bot, chat_id)
    elif text in ['Подписки', 'В подписки']:
        keyboards_menu(bot, chat_id, '1')
    elif text == 'Курсы валют':
        keyboards_menu(bot, chat_id, '2')
    elif text == 'Мои подписки':
        bot.send_message(chat_id=chat_id,
                         text=work.user_subscriptions(chat_id),
                         parse_mode='HTML',)
    elif text in ['РБК', 'Коммерсант']:
        if work.subscription_check(chat_id, text) is False:
            keyboards_menu(bot, chat_id, keyboard_sub_switch(text)[1])
        else:
            keyboards_menu(bot, chat_id, keyboard_sub_switch(text)[0])
    elif text == 'Последние новости РБК':
        send_last_news(bot, 5, chat_id, 'РБК')
    elif text == 'Последние новости Коммерсант':
        send_last_news(bot, 3, chat_id, 'Коммерсант')
    elif text in ['Включить РБК', 'Включить Коммерсант']:
        title_name = text.split()[1]
        add_sub = work.subscriptions_db_add_sub(chat_id, title_name, True)
        update.message.reply_text('Подписка включена')
        keyboards_menu(bot, chat_id, keyboard_sub_switch(title_name)[0])
    elif text in ['Выключить РБК', 'Выключить Коммерсант']:
        title_name = text.split()[1]
        add_sub = work.subscriptions_db_add_sub(chat_id, title_name, False)
        update.message.reply_text('Подписка включена')
        keyboards_menu(bot, chat_id, keyboard_sub_switch(title_name)[1])
    elif text.lower() in currency.CURRENCY_CODES:
        update.message.reply_text(currency.get_currency_rates(text, today))
    else:
        update.message.reply_text(text)


def keyboards_menu(bot, chat_id, keyboard_id=0):
        menu = keyboards_menu_buttons(keyboard_id).get('menu')
        text = keyboards_menu_buttons(keyboard_id).get('text')
        reply_markup = telegram.ReplyKeyboardMarkup(menu, resize_keyboard=True)
        bot.send_message(chat_id=chat_id,
                         text=text,
                         reply_markup=reply_markup)


def date_time_converter(pub_struct_time, timezone):
    result = dict()
    try:
        news_time = datetime.fromtimestamp(mktime(pub_struct_time)) + get_time_diff(timezone)
        result['date'] = '{}-{:02d}-{:02d}'.format(news_time.year, news_time.month, news_time.day)
        result['time'] = '{:02d}:{:02d}'.format(news_time.hour, news_time.minute)
    except TypeError:
        result['date'] = None
        result['time'] = None
    return result


def callback_collect_news(bot, job):
    for title in settings.SOURCES_LIST:
        title_name = title['title']
        parse_from_rss = feedparser.parse(title['source_link'])
        for news_counter in reversed(range(0, 5)):
            news = parse_from_rss.entries[news_counter]
            news_link = news.link
            if news_link not in title['check_links']:
                pub_time = date_time_converter(news.published_parsed, 'Europe/Moscow')
                news_title = news.title
                news_short_link = google_short_url(news_link)
                add_news = work.news_db_add_news(title_name, pub_time.get('date'),
                                                 pub_time.get('time'), news_title,
                                                 news_link, news_short_link)
            title['check_links'][news_counter] = news_link


def send_last_news(bot, counter, chat_id, title):
    text = ''
    last_news = work.last_news(counter, title)
    for news in last_news:
        text = text + news.news_title + '\n' + news.news_short_link + '\n'
    if text != '':
        text = '<b>' + title + ':</b>' + '\n' + text
        bot.send_message(chat_id=chat_id,
                         text=text,
                         parse_mode='HTML',
                         disable_web_page_preview=True)


def send_news(bot, job):
    for title in settings.SOURCES_LIST:
        title_name = title['title']
        min_news = title['min_news']
        unsent_news = work.unsent_news_list(title_name)
        news_counter = len(unsent_news)
        now_time = datetime.now().strftime('%Y.%m.%d %H.%M.%S')
        if news_counter > settings.MAX_NEWS:
            unsent_news = unsent_news[0:settings.MAX_NEWS]
        if news_counter >= min_news:
            text = ''
            subscribers = work.subscribers_list(title_name)
            if title_name == 'РБК':
                pass
                # subscribers.append('@rbknews1')  #включаем на сервере
            for news in unsent_news:
                text = text + news.news_title + '\n' + news.news_short_link + '\n'
            text = '<b>' + title_name + ':</b>' + '\n' + text
            for sub in subscribers:
                bot.send_message(chat_id=sub,
                                 text=text,
                                 parse_mode='HTML',
                                 disable_web_page_preview=True)
            work.mark_sent_news(unsent_news)
            with open('logs/sendnews.txt', "a") as local_file:
                local_file.write('{}: {} News sent to {}\n'
                                 .format(now_time, title_name, subscribers))
        else:
            with open('logs/sendnews.txt', "a") as local_file:
                local_file.write('{}: {} Not enough news\n{}\n'
                                 .format(now_time, title_name, unsent_news))


def main():
    updater = Updater(settings.TELEGRAM_API_KEY)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, chat_bot))
    dp.add_handler(CommandHandler("start", command_start))

    j = updater.job_queue
    job_collect_news = j.run_repeating(callback_collect_news, interval=180, first=0)
    job_send_news = j.run_repeating(send_news, interval=180, first=0)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logging.info('Bot started')
    main()
