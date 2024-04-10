import requests


def geocode(address, key):
    server = 'https://geocode-maps.yandex.ru/1.x/'
    params = {'apikey': key,
              'geocode': address,
              'format': 'json'}
    resp = requests.get(server, params=params)
    if resp:
        resp = resp.json()
    else:
        raise RuntimeError('Ошибка выполнения запроса')
    return resp['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']


def get_coords(address, key):
    toponym = geocode(address, key)
    if not toponym:
        return None, None
    coords = toponym['Point']['pos'].split()
    return coords[0], coords[1]

