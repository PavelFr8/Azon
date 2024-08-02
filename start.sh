#!/bin/bash

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

echo "Start running Azon!"

flask category_load

flask db init

flask db migrate -m "Initial migration."

flask db upgrade

flask run