import re
from django.db import models


class Person(models.Model):
    uri_pattern = re.compile('/people/(.+)')
    name = models.CharField(max_length=256)

    def fields(self):
        return {'name',}
