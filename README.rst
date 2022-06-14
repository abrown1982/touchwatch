==========
Touchwatch
==========

Touchwatch is a small Django app to watch a directory for changes
and if any found, touch a file (to trigger a server restart).

Quick start
-----------

1. Add "touchwatch" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'touchwatch',
    ]

2. Include the polls URLconf in your project urls.py like this::

    from touchwatch.views import wsgitime
    if settings.DEBUG:
        urlpatterns += path('wt/', wsgitime, name='wsgitime'),

3. Include the template at the bottom of your base.html file

    {% include "touchwatch/js.html" %}

4.. Set the path of the file you want to touch in your settings file OR set the command you want to be run

    TOUCHWATCH_PATH = "%s/uwsgi.ini" % APP_DIR

    TOUCHWATCH_COMMAND = "ps -ef | grep 'gunicorn' | grep -v grep | awk '{print $2}' | xargs -r kill -HUP 2> /dev/null"

5.. Set the path of the folder you want to watch in your settings file

    TOUCHWATCH_FOLDER = APP_DIR

============
How it works
============

From the commandline run the management command 'touchwatch':

    python manage.py touchwatch

This will then sit and watch for changes to the file defined in TOUCHWATCH_FOLDER, when changes are seen
then the file defined in TOUCHWATCH_PATH will be touched.  A small piece of JS runs on all pages on the
browser which looks for a change to the touched time of the defined file.  When the time changes,
the JS flashes the background colour and refreshes the page.