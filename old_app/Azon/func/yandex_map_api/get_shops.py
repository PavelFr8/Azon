from .geocoder import get_coords
from .find_business import find_bis
from .get_api_keys import get_api_keys


def find_shops(text):
    key1, key2 = get_api_keys()
    toponym_to_find = text
    if toponym_to_find:
        try:
            lat, lon = get_coords(toponym_to_find, key1)
        except Exception:
            return 'Некорректные введённые данные'
        res_find = find_bis(','.join((lat, lon)),
                            '0.01',
                            'Ozon', key2)

        anw = []
        for item in res_find:
            res = []
            res.append(item[1]['address'])
            try:
                res.append(item[1]['Phones'][0]['formatted'])
            except Exception:
                res.append('Телефон не указан')
            res.append(item[1]['Hours']['text'])
            anw.append(res)
        return anw



