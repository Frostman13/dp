import urllib.request
import xml.etree.ElementTree as etree
import pytz
from datetime import datetime, date, timedelta

CURRENCY_URL = 'https://www.cbr.ru/scripts/XML_daily.asp'
FOLDER_PATH = '/home/ubuntu/diplom_project/data/' # если запускается локально, обнулить
# FOLDER_PATH = '' 

def get_xml_file_name(url):
    url_split = url.split("/")[-1]
    ext_split = url_split.split(".")[1]
    xml_file_name = url_split.replace(ext_split, "xml")
    return str.lower(xml_file_name)

def get_day(filename):
    with open(filename, 'rb') as f:
        tree = etree.parse(f)
        root = tree.getroot()
        return root.attrib['Date']

def get_currency_info(filename, logname):
    web_file = urllib.request.urlopen(CURRENCY_URL, timeout = 10)
    web_data = web_file.read()
    with open(filename, "wb") as local_file:
        local_file.write(web_data)
    with open(logname, "a") as currency_data_log:
        currency_data_log.write('{};информация обновлена (курсы теперь от {})\n'.format(local_time, get_day(filename)))

if __name__ == '__main__':
    xml_file_name = get_xml_file_name(CURRENCY_URL)
    file_fullname = FOLDER_PATH + xml_file_name
    log_fullname = FOLDER_PATH + 'currency_data_log.txt'
    local_time = datetime.now(pytz.timezone('Europe/Moscow')).replace(tzinfo=None)

    try:
        file_date = datetime.strptime(get_day(file_fullname),'%d.%m.%Y')
        if file_date > local_time:
            with open(log_fullname, "a") as currency_data_log:
                currency_data_log.write('{};информация актуальна (курсы от {})\n' \
                    .format(local_time, get_day(file_fullname)))
        else:
            get_currency_info(file_fullname, log_fullname)
    except FileNotFoundError:
            get_currency_info(file_fullname, log_fullname)

