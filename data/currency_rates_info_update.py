import urllib.request
import xml.etree.ElementTree as etree
from datetime import datetime, date, time, timedelta

CURRENCY_URL = 'https://www.cbr.ru/scripts/XML_daily.asp'
FOLDER_PATH = '/home/ubuntu/diplom_project/data/' # если запускается локально, обнулить
# FOLDER_PATH = '' 
TIME_DELTA = timedelta(hours=3)

def get_xml_file_name(url):
    url_split = url.split("/")[-1]
    ext_split = url_split.split(".")[1]
    xml_file_name = url_split.replace(ext_split, "xml")
    return str.lower(xml_file_name)

xml_file_name = get_xml_file_name(CURRENCY_URL)
local_time = datetime.now()+TIME_DELTA

def get_day():
    with open(FOLDER_PATH+xml_file_name, 'rb') as f:
        tree = etree.parse(f)
        root = tree.getroot()
        return root.attrib['Date']

def get_currency_info():
    web_file = urllib.request.urlopen(CURRENCY_URL, timeout = 10)
    web_data = web_file.read()
    with open(FOLDER_PATH+xml_file_name, "wb") as local_file:
        local_file.write(web_data)
    with open(FOLDER_PATH+'currency_data_log.txt', "a") as currency_data_log:
        currency_data_log.write('{};информация обновлена (файл теперь от {})\n'.format(local_time,get_day()))

try:    
    if get_day() > datetime.date(datetime.now()+TIME_DELTA).strftime('%d.%m.%Y'):
        with open(FOLDER_PATH+'currency_data_log.txt', "a") as currency_data_log:
            currency_data_log.write('{};информация актуальна (файл теперь от {})\n'.format(local_time,get_day()))
    else:
        get_currency_info()
except FileNotFoundError:
        get_currency_info()
