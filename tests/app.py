import os
import sys


from django.conf import settings
import django12factor


settings.configure(
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
    **django12factor.factorise()
)


from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse



def index(request):
    return HttpResponse('Hello World')


urlpatterns = (
    url(r'^$', index),
)


application = get_wsgi_application()
