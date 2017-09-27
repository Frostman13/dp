import xml.etree.ElementTree as etree
CURRENCY_CODES = {'доллар сша':'R01235','курс доллара':'R01235','usd':'R01235','доллар':'R01235','dollar':'R01235',
                'евро':'R01239','курс евро':'R01239','eur':'R01239','евро':'R01239','euro':'R01239',
                'юань':'R01375','курс юаня':'R01375','cny':'R01375',
                'гривна':'R01720','курс гривны':'R01720','uah':'R01720',
                'фунт':'R01035','курс фунта':'R01035','gbp':'R01035'}
CURRENCY_NAMES = {'R01235':'Доллар США',
                'R01239':'Евро',
                'R01375':'Китайский юань',
                'R01720':'Украинская гривна',
                'R01035':'Фунт стерлингов'}


def get_currency_rates(currency):
    with open("data/xml_daily.xml", 'rb') as currency_rates:
        tree = etree.parse(currency_rates)
        date = tree.getroot().attrib['Date']
        # currency_name = CURRENCY_NAMES[CURRENCY_CODES[str.lower(currency)]]
        exchange_rate = tree.getroot().findtext('.//Valute[@ID="{}"]/Value'.format(CURRENCY_CODES[str.lower(currency)]))
        exchange_nominal = tree.getroot().findtext('.//Valute[@ID="{}"]/Nominal'.format(CURRENCY_CODES[str.lower(currency)]))
        exchange_char_code = tree.getroot().findtext('.//Valute[@ID="{}"]/CharCode'.format(CURRENCY_CODES[str.lower(currency)]))
        result = 'Курс ЦБ РФ на {}:\n\r{} {} = {} RUB'.format(
            date, exchange_nominal, exchange_char_code, exchange_rate)
    return(result)


if __name__ == '__main__':
    pass
    # print(CURRENCY_CODES['Евро'])
