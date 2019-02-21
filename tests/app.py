import django
from django.conf.urls import url, re_path
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
import hyperdjango


from . import models
    
urlpatterns = (
    re_path('.*', hyperdjango.HyperView.as_view(models=models)),
)


application = get_wsgi_application()
