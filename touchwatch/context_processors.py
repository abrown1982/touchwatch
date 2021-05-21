from .utils import get_wsgi_time
from django.conf import settings

def wsgitime(request):
    if settings.DEBUG:
        return {'wt': get_wsgi_time(), 'wtcolour': settings.TOUCHWATCH_COLOUR, 'wtdelay':settings.TOUCHWATCH_POLLING_DELAY }
