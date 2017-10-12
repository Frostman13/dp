# Добавляем открытые настройки. Секьюрные храним в settings_local

try:
    from settings_local import *
except ImportError:
    pass

parse_link = None
RBC_RSS = 'http://static.feed.rbc.ru/rbc/logical/footer/news.rss'