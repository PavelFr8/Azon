# Azon

Проект "Azon" представляет собой веб-приложение интернет-магазина, разработанное с использованием Flask. Основная цель 
приложения - обеспечить пользователям удобный и безопасный 
опыт онлайн-шопинга, предоставив возможность как покупать 
товары, так и продавать их.

## Использованные технологии
* Python 3.9;
* HTML, CSS;
* Flask (Web application framework);
* PostgreSQL (database);
* SQLAlchemy (working with database from Python);
* Jinja2 (Templating engine);
* [Yandex Maps API](https://yandex.ru/maps-api/) (finding places);

## Требования

Для запуска проекта вам понадобится Python версии 3.9+ 

Установите необходимые библиотеки, выполнив команду:

pip install -r requirements.txt

Вставьте ключи от API Yandex Maps в файл **.env**


## Структура проекта

- **app.py**: Главный файл приложения, содержащий основной код Flask.
- **.env**: Хранилище переменных виртуального окружения.
- **templates**: Шаблоны HTML-страниц.
- **static/**: Статические файлы, такие как CSS, изображения и т.д.
- **requirements.txt**: Список зависимостей проекта.
- **data**: Функции для работы с базой данных.
- **func**: Вспомогательные функции.


## Запуск
source venv/bin/activate

flask db init

flask db migrate -m "Initial migration."

flask db upgrade

flask category_load

flask run
