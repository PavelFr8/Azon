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
    return [[tuple(map(str, response['features'][0]['geometry']['coordinates'])),
             response['features'][0]['properties']['CompanyMetaData']],
            [tuple(map(str, response['features'][1]['geometry']['coordinates'])),
             response['features'][1]['properties']['CompanyMetaData']],
            [tuple(map(str, response['features'][2]['geometry']['coordinates'])),
             response['features'][2]['properties']['CompanyMetaData']],
            [tuple(map(str, response['features'][3]['geometry']['coordinates'])),
             response['features'][3]['properties']['CompanyMetaData']],
            [tuple(map(str, response['features'][4]['geometry']['coordinates'])),
             response['features'][4]['properties']['CompanyMetaData']],
            [tuple(map(str, response['features'][5]['geometry']['coordinates'])),
             response['features'][5]['properties']['CompanyMetaData']],
            [tuple(map(str, response['features'][6]['geometry']['coordinates'])),
             response['features'][6]['properties']['CompanyMetaData']],
            [tuple(map(str, response['features'][7]['geometry']['coordinates'])),
             response['features'][7]['properties']['CompanyMetaData']],
            [tuple(map(str, response['features'][8]['geometry']['coordinates'])),
             response['features'][8]['properties']['CompanyMetaData']],
            [tuple(map(str, response['features'][9]['geometry']['coordinates'])),
             response['features'][9]['properties']['CompanyMetaData']],
            ]
