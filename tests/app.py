from django.conf.urls import re_path
from django.core.wsgi import get_wsgi_application
import hyperdjango
from . import models


urlpatterns = (
    re_path('.*', hyperdjango.HyperView.as_view(models=models)),
)


application = get_wsgi_application()
