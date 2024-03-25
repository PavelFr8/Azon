from . import db_session
from flask import g

# Функция для получения сессии базы данных
def get_db_session():
    if 'db_session' not in g:
        g.db_session = db_session.create_session()
    return g.db_session