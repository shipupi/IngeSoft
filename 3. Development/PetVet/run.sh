#!/bin/bash
rm -f db.sqlite3
python3 manage.py makemigrations
python3 manage.py migrate
python3 ./manage.py loaddata auth
# python3 ./manage.py loaddata categories
# python3 ./manage.py loaddata products
python3 manage.py runserver
