# Добавляем открытые настройки. Секьюрные храним в settings_local

SOURCES_LIST = [{'title': 'РБК',
                 'min_news': 5,
                 'source_link': 'http://static.feed.rbc.ru/rbc/logical/footer/news.rss',
                 'check_links': [None, None, None, None, None],
                 },
                {'title': 'Коммерсант',
                 'min_news': 1,
                 'source_link': 'https://www.kommersant.ru/RSS/main.xml',
                 'check_links': [None, None, None, None, None],
                 },
                ]

MAX_NEWS = 5

try:
    from settings_local import *
except ImportError:
    pass
