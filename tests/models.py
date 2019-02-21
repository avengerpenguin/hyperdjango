import django
import hyperdjango


class Thing(hyperdjango.models.HyperModel):
    #class Meta:
    #    app_label = 'hyperdjangotests'
    name = django.db.models.CharField(max_length=256)
