if __name__ == '__main__':
    pass

    # job_old_minute = j.run_repeating(callback_news1_minute, interval=60, first=0)
    # def callback_news1_minute(bot, job):
    #     parse_from_rss = feedparser.parse(settings.RBC_RSS)
    #     news_in_text = 5
    #     news = list()
    #     for news_counter in range(0, news_in_text):
    #         news.append(parse_from_rss.entries[news_counter].link)

    #     if (settings.check_parse_links[0] not in news) and (settings.check_parse_links[1] not in news):
    #         settings.check_parse_links[0] = news[0]
    #         settings.check_parse_links[1] = news[1]
    #         text = ''
    #         subscribers = work.subscribers_list('РБК')
    #         # \subscribers.append('@rbknews1')
    #         for news_counter in range(0, news_in_text):
    #             text = text + parse_from_rss.entries[news_counter].title + '\n' + news[news_counter] + '\n'
    #         for sub in subscribers:
    #             bot.send_message(chat_id=sub,
    #                              text=text)

    #     with open('logs/sendnews.txt', "a") as local_file:
    #         now_time = datetime.now().strftime('%Y.%m.%d %H.%M.%S')
    #         local_file.write('{}: link1: {}\n'.format(now_time, settings.check_parse_links[0]))
    #         local_file.write('{}: link2: {}\n'.format(now_time, settings.check_parse_links[1]))
    #         local_file.write('{}: {}\n'.format(now_time, 'repeat'))