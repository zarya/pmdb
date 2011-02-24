import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

DOCUMENT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DOCUMENT_ROOT)
sys.path.append(os.path.dirname(DOCUMENT_ROOT))

def application(environ, start_response):
    import django.core.handlers.wsgi
    _application = django.core.handlers.wsgi.WSGIHandler()
    return _application(environ, start_response)

