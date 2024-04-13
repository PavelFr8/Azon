import requests


def find_bis(ll, spn, request, key, locale="ru_RU"):
    server = 'http://search-maps.yandex.ru/v1/'
    params = {'apikey': key,
              'text': request,
              'lang': locale,
              'll': ll,
              'spn': ','.join((spn, spn)),
              'type': 'biz'}
    response = requests.get(server, params=params).json()
    anw = []
    if len(response['features']) >= 10:
        counter = 9
    else:
        counter = len(response['features'])
    for i in range(counter):
        anw.append([tuple(map(str, response['features'][i]['geometry']['coordinates'])),
             response['features'][i]['properties']['CompanyMetaData']])
    return anw
