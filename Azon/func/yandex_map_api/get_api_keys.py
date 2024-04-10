import os
from dotenv import load_dotenv


def get_api_keys():
    path = os.path.join(os.path.dirname('Azon'), '../../.env')
    if os.path.exists(path):
        load_dotenv(path)

        GEOCODE_KEY = os.environ.get('GEOCODE_KEY')
        ORG_KEY = os.environ.get('ORG_KEY')

        return [GEOCODE_KEY, ORG_KEY]