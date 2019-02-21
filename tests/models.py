import django
import hyperdjango


class Thing(hyperdjango.models.HyperModel):
    name = django.db.models.CharField(max_length=256)
