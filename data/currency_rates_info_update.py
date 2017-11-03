import urllib.request
import xml.etree.ElementTree as etree
import pytz
import os
from datetime import datetime, date, timedelta

CURRENCY_URL = 'https://www.cbr.ru/scripts/XML_daily.asp'
FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))


def get_day(filename):
    with open(filename, 'rb') as f:
        tree = etree.parse(f)
        root = tree.getroot()
        return root.attrib['Date']


def tom_to_tod(tom_filename, tod_filename, logname):
    try:
        with open(tom_filename, 'rb') as tom_file:
            file_data = tom_file.read()
        with open(tod_filename, "wb") as tod_file:
            tod_file.write(file_data)
    except FileNotFoundError:
        pass


def get_currency_info(filename, logname):
    web_file = urllib.request.urlopen(CURRENCY_URL, timeout=10)
    web_data = web_file.read()
    with open(filename, "wb") as local_file:
        local_file.write(web_data)
    with open(logname, "a") as currency_data_log:
        currency_data_log.write('{};информация обновлена (последние курсы от {})\n'
                                .format(local_time, get_day(filename)))


if __name__ == '__main__':
    xml_tod_file_name = 'xml_tod.xml'
    xml_tom_file_name = 'xml_tom.xml'
    tod_file_fullname = os.path.join(FOLDER_PATH, xml_tod_file_name)
    tom_file_fullname = os.path.join(FOLDER_PATH, xml_tom_file_name)
    log_fullname = os.path.join(FOLDER_PATH, 'currency_data_log.txt')
    local_time = datetime.now(pytz.timezone('Europe/Moscow')).replace(tzinfo=None)
    try:
        check_time = datetime.strptime(get_day(tom_file_fullname), '%d.%m.%Y')
        if check_time > local_time:
            with open(log_fullname, "a") as currency_data_log:
                currency_data_log.write('{};информация актуальна (есть курсы на следующий день: {})\n'
                                        .format(local_time, get_day(tom_file_fullname)))
        else:
            tom_to_tod(tom_file_fullname, tod_file_fullname, log_fullname)
            get_currency_info(tom_file_fullname, log_fullname)
    except FileNotFoundError:
            tom_to_tod(tom_file_fullname, tod_file_fullname, log_fullname)
            get_currency_info(tom_file_fullname, log_fullname)
