import re

import inflect
from django.db import models

p = inflect.engine()


class classproperty:
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


class HyperModel(models.Model):
    class Meta:
        abstract = True

    @classproperty
    def uri_pattern(cls):
        return re.compile(
            "^/{}/([^/]+)$".format(p.plural(cls.__name__.lower()))
        )
