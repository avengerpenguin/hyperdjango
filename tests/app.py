from django.core.wsgi import get_wsgi_application
from django.urls import re_path

import hyperdjango

from . import models

urlpatterns = (re_path(".*", hyperdjango.HyperView.as_view(models=models)),)


application = get_wsgi_application()
