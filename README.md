# Azon

The "Azon" project is an online store web application developed using Flask. The main goal of the application is to provide users with a convenient and safe online shopping experience, providing the opportunity to both buy and sell products.

## Used technologies
* Python 3.9;
* Flask (Web application framework);
* PostgreSQL (database);
* SQLAlchemy (working with database from Python);
* HTML, CSS, JS;
* Bootstrap (CSS and JS framework);
* Jinja2 (Templating engine);
* [Yandex Maps API](https://yandex.ru/maps-api/) (finding places);
* Flask-RESTful (Creating Azon API);


## How to run

Run **start.sh**
```commandline
./start.sh
```

**OR**

1. ```python -m venv venv```
2. ```source venv/bin/activate```
3. Init database
4. ```flask category_load```
5. ```flask run```