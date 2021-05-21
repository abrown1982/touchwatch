from django.conf import settings
import os

def get_wsgi_time():
    return int(round(os.path.getmtime(settings.TOUCHWATCH_PATH)))
