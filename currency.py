import xml.etree.ElementTree as etree
from datetime import datetime
CURRENCY_CODES = {'доллар сша': 'R01235', 'курс доллара': 'R01235', 'usd': 'R01235',
                  'доллар': 'R01235', 'dollar': 'R01235',
                  'евро': 'R01239', 'курс евро': 'R01239', 'eur': 'R01239',
                  'euro': 'R01239',
                  'юань': 'R01375', 'курс юаня': 'R01375', 'cny': 'R01375',
                  'гривна': 'R01720', 'курс гривны': 'R01720', 'uah': 'R01720',
                  'фунт': 'R01035', 'курс фунта': 'R01035', 'gbp': 'R01035'}
CURRENCY_NAMES = {'R01235': 'Доллар США',
                  'R01239': 'Евро',
                  'R01375': 'Китайский юань',
                  'R01720': 'Украинская гривна',
                  'R01035': 'Фунт стерлингов'}


def get_currency_rates(currency, today):
    result = 'Сегодня: {}'.format(today)
    currency_code = CURRENCY_CODES[currency.lower()]
    with open("data/xml_tod.xml", 'rb') as currency_rates_tod:
        tree_tod = etree.parse(currency_rates_tod)
        date_tod = tree_tod.getroot().attrib['Date']
        exchange_nominal = tree_tod.getroot().findtext('.//Valute[@ID="{}"]/Nominal'.format(currency_code))
        exchange_char_code = tree_tod.getroot().findtext('.//Valute[@ID="{}"]/CharCode'.format(currency_code))
        exchange_rate_tod = tree_tod.getroot().findtext('.//Valute[@ID="{}"]/Value'.format(currency_code))
        result_tod = '\n\nКурс ЦБ РФ на {}:\n\r{} {} = {} RUB'.format(
            date_tod, exchange_nominal, exchange_char_code, exchange_rate_tod)

    with open("data/xml_tom.xml", 'rb') as currency_rates_tom:
        tree_tom = etree.parse(currency_rates_tom)
        date_tom = tree_tom.getroot().attrib['Date']
        exchange_rate_tom = tree_tom.getroot().findtext('.//Valute[@ID="{}"]/Value'.format(currency_code))
        result_tom = '\n\nКурс ЦБ РФ на {}:\n\r{} {} = {} RUB'.format(
            date_tom, exchange_nominal, exchange_char_code, exchange_rate_tom)

    # today_ = datetime.strptime(today, '%d.%m.%Y')
    # date_tom = datetime.strptime(date_tom, '%d.%m.%Y')
    # print(today)
    # print(date_tom)
    # print(type(today))
    # print(type(date_tom))
    if datetime.strptime(today, '%d.%m.%Y') > datetime.strptime(date_tom, '%d.%m.%Y'):
        result += result_tom
    else:
        if date_tod != date_tom:
            result = result + result_tod + result_tom
        else:
            result += result_tod
    return result


if __name__ == '__main__':
    pass
    # print(CURRENCY_CODES['Евро'])
    # currency_name = CURRENCY_NAMES[currency_code]
