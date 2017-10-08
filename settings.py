# Добавляем открытые настройки. Секьюрные храним в settings_local

try:
    from settings_local import *
except ImportError:
    pass