import xml.etree.ElementTree as etree
CURRENCY_CODES = {'доллар сша': 'R01235', 'курс доллара': 'R01235', 'usd': 'R01235', 'доллар': 'R01235', 'dollar': 'R01235',
                  'евро': 'R01239', 'курс евро': 'R01239', 'eur': 'R01239', 'евро': 'R01239', 'euro': 'R01239',
                  'юань': 'R01375', 'курс юаня': 'R01375', 'cny': 'R01375',
                  'гривна': 'R01720', 'курс гривны': 'R01720', 'uah': 'R01720',
                  'фунт': 'R01035', 'курс фунта': 'R01035', 'gbp': 'R01035'}
CURRENCY_NAMES = {'R01235': 'Доллар США',
                  'R01239': 'Евро',
                  'R01375': 'Китайский юань',
                  'R01720': 'Украинская гривна',
                  'R01035': 'Фунт стерлингов'}


def get_currency_rates(currency, today):
    with open("data/xml_tod.xml", 'rb') as currency_rates_tod:
        tree_tod = etree.parse(currency_rates_tod)
        date_tod = tree_tod.getroot().attrib['Date']
        # currency_name = CURRENCY_NAMES[CURRENCY_CODES[str.lower(currency)]]
        exchange_rate_tod = tree_tod.getroot().findtext('.//Valute[@ID="{}"]/Value'.format(CURRENCY_CODES[str.lower(currency)]))
        exchange_nominal = tree_tod.getroot().findtext('.//Valute[@ID="{}"]/Nominal'.format(CURRENCY_CODES[str.lower(currency)]))
        exchange_char_code = tree_tod.getroot().findtext('.//Valute[@ID="{}"]/CharCode'.format(CURRENCY_CODES[str.lower(currency)]))
        result = 'Сегодня: {}\n\nКурс ЦБ РФ на {}:\n\r{} {} = {} RUB'.format(
            today, date_tod, exchange_nominal, exchange_char_code, exchange_rate_tod)

    with open("data/xml_tom.xml", 'rb') as currency_rates_tom:
        tree_tom = etree.parse(currency_rates_tom)
        date_tom = tree_tom.getroot().attrib['Date']
        if date_tom != date_tod:
            exchange_rate = tree_tom.getroot().findtext('.//Valute[@ID="{}"]/Value'.format(CURRENCY_CODES[str.lower(currency)]))
            result = result + '\n\nКурс ЦБ РФ на {}:\n\r{} {} = {} RUB'.format(
                date_tom, exchange_nominal, exchange_char_code, exchange_rate)

    return result


if __name__ == '__main__':
    pass
    # print(CURRENCY_CODES['Евро'])
