from .utils import get_wsgi_time
from django.http import JsonResponse


def wsgitime(request):
    return JsonResponse({"wt": get_wsgi_time()})