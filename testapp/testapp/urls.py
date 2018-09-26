"""testapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

import hyperdjango
import rdflib

from contacts import models


def model2graph(model, base_url):
    base = rdflib.Namespace(base_url)
    g = rdflib.Graph()

    for obj in model.objects.all():
        uri = base['/people' + '/' + str(obj.pk)]
        g.add((uri, rdflib.RDF.type, base['/' + model.__name__]))

        for prop in obj.__dict__:
            if prop not in ['_state', 'id']:
                g.add((uri, base['/' + prop], rdflib.Literal(getattr(obj, prop))))

    return g


def graph_factory(base_url):
    return model2graph(models.Person, base_url)


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('.*', hyperdjango.HyperView.as_view(models=models)),
]
