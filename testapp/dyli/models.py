from django.db import models

from hyperdjango.models import HyperModel


class Thing(HyperModel):
    name = models.CharField(max_length=256)
