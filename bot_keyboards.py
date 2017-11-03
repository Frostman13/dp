def keyboard_sub_switch(title):
    keyboard_title_ids = {
                         'РБК': ['3off', '3on'],
                         'Коммерсант': ['4off', '4on'],
                         }
    result = keyboard_title_ids.get(title)
    return result


def keyboards_menu_buttons(keyboard_id=0):
    if str(keyboard_id) != '0':
        if str(keyboard_id) == '1':
            keyboard = {'menu': [['РБК', 'Коммерсант'], ['Мои подписки', 'В главное меню']],
                        'text': 'Подписки',
                        }
        elif str(keyboard_id) == '2':
            keyboard = {'menu': [['Доллар', 'Евро', 'В главное меню']],
                        'text': 'Курсы валют',
                        }
        elif str(keyboard_id) == '3on':
            keyboard = {'menu': [['Включить РБК', 'Последние новости РБК', 'В подписки']],
                        'text': 'Управление подпиской на РБК',
                        }
        elif str(keyboard_id) == '3off':
            keyboard = {'menu': [['Выключить РБК', 'Последние новости РБК', 'В подписки']],
                        'text': 'Управление подпиской на РБК',
                        }
        elif str(keyboard_id) == '4on':
            keyboard = {'menu': [['Включить Коммерсант', 'Последние новости Коммерсант', 'В подписки']],
                        'text': 'Управление подпиской на Коммерсант',
                        }
        elif str(keyboard_id) == '4off':
            keyboard = {'menu': [['Выключить Коммерсант', 'Последние новости Коммерсант', 'В подписки']],
                        'text': 'Управление подпиской на Коммерсант',
                        }
    else:
        keyboard = {'menu': [['Подписки', 'Курсы валют']],
                    'text': 'Вы в главном меню',
                    }
    return keyboard


if __name__ == '__main__':
    # pass
    print(keyboard_sub_ids('РБК'))
