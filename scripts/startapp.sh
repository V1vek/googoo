#!/bin/sh
set -e
APPNAME=$1
source djenv/bin/activate
APPDIR=/var/www/$APPNAME
cd $APPDIR
pip install -r requirements.pip
export PYTHONPATH=$PYTHONPATH:$APPDIR
export DJANGO_SETTINGS_MODULE=main.settings.production
python common/util/run_scheduler.py
# python manage.py collectstatic --noinput
# python manage.py makemigrations --noinput
# python manage.py migrate
djenv/bin/gunicorn -c scripts/gunicorn.py main.wsgi --reload
